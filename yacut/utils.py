import hashlib

from yacut.constants import LENGTH_LINK_DEAFULT
from yacut.models import URLMap


def get_unique_short_id(long_url):
    """
    Кодирует длинную ссылку в короткую вида  http://yacut.ru/X7NYIol.
    """
    hash_value = hashlib.sha256()
    hash_value.update(long_url.encode())
    hash_value.hexdigest()
    short_url = f'{hash_value.hexdigest()[:LENGTH_LINK_DEAFULT]}'
    return short_url


def generate_unique_short_id(original_link):
    """
    Генерирует уникальный короткий идентификатор для оригинальной ссылки.
    """
    while True:
        short_link = get_unique_short_id(original_link)
        if not URLMap.query.filter_by(short=short_link).first():
            return short_link