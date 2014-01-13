from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
DateTime,
Boolean,
ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class SureRoute(Base):
    __tablename__ = 'sureroutes'
    id = Column(Integer, primary_key=True)
    customer_name = Column(Text)
    hostname = Column(Text)
    object_path = Column(Text)
    email = Column(Text)

class SureRouteResult(Base):
    __tablename__ = 'sureroutes_results'
    id = Column(Integer, primary_key=True)
    sureroute_id = Column(Integer, ForeignKey('sureroutes.id'))
    time = Column(DateTime)
    success = Column(Boolean)
    status_code = Column(Text)

class QuickFix(Base):
    __tablename__ = 'quickfixes'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    spidering_depth = Column(Integer)
    spidering_breadth = Column(Integer)
    email = Column(Text)


def trigger_object_path(mapper, connection, target):
    from .tasks import check_object
    check_object.delay(target)


event.listen(SureRoute, 'after_insert', trigger_object_path)
