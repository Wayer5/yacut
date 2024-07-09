from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from yacut.constants import LENGTH_CUSTOM_LINK, LENGTH_ORIGINAL_LINK


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, LENGTH_ORIGINAL_LINK),
                    URL(message='Некорректный URL-адрес')
                    ]
    )
    custom_id = StringField(
        'Короткий идентификатор',
        validators=[Length(1, LENGTH_CUSTOM_LINK),
                    Optional(),
                    Regexp('[0-9A-Za-z]+')
                    ]
    )
    submit = SubmitField('Создать')
