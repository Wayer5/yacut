from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import generate_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    original_link = form.original_link.data
    custom_id = form.custom_id.data

    if custom_id and len(custom_id) > 16:
        flash('Слишком длинная ссылка.', 'error')
        return render_template('index.html', form=form), 200

    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first():
            flash(
                'Предложенный вариант короткой ссылки уже существует.',
                'error'
            )
            short_link = generate_unique_short_id(original_link)
        else:
            short_link = custom_id
    else:
        short_link = generate_unique_short_id(original_link)

    url_map = URLMap(original=original_link, short=short_link)
    db.session.add(url_map)
    db.session.commit()
    return render_template(
        'index.html',
        form=form,
        short_link=short_link
    )


@app.route('/<string:short_id>', methods=['GET'])
def get_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(link.original)