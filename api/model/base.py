from model.database import db


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        response = {}
        fields = []
        if hasattr(self, "_default_fields"):
            fields.extend(self._default_fields)
        for col in self.__table__.columns:
            if col.name in fields:
                # else:
                response[col.name] = getattr(self, col.name)
        return response
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns
        #         if c.name in (hasattr(self, "_default_fields") and self._default_fields or ["id"])}
