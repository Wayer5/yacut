from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import LENGTH_CUSTOM_LINK, LETTERS
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import generate_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    url = data.get('url', None)

    custom_id = data.get('custom_id', None)

    if custom_id is not None:
        if len(custom_id) > LENGTH_CUSTOM_LINK:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

        if not all(char in LETTERS for char in custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

    if custom_id is None or custom_id == '':
        custom_id = generate_unique_short_id(url)

    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')

    urlmap = URLMap(original=url, short=custom_id)
    db.session.add(urlmap)
    db.session.commit()

    return jsonify(
        {
            'url': url,
            'short_link': url_for(
                'get_url', short_id=custom_id, _external=True)
        }
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage('Указанный id не найден',
                              status_code=HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK