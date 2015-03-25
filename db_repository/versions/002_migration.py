from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
events = Table('events', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('eventId', Integer),
    Column('riderId', String(length=64)),
    Column('speed', Integer),
    Column('eventName', String(length=120)),
    Column('createTime', DateTime),
    Column('updateTime', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['events'].columns['eventName'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['events'].columns['eventName'].drop()
