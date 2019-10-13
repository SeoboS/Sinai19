from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class Mouse(Base):
    __tablename__ = 'mouse'
    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    def __repr__(self):
        return "<Mouse(x='{}', y='{}')>" \
            .format(self.x, self.y)
