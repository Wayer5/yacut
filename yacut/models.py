from datetime import datetime, timezone

from yacut import db

from .constants import LENGTH_CUSTOM_LINK, LENGTH_ORIGINAL_LINK


def utc_now():
    return datetime.now(timezone.utc)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(db.String(LENGTH_CUSTOM_LINK),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
