from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
exam = Table('exam', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('exam_date', DateTime),
    Column('firstName', String(length=20)),
    Column('lastName', String(length=20)),
    Column('status', SmallInteger, default=ColumnDefault(0)),
    Column('diagnosis', String(length=300)),
    Column('patientID', String(length=80)),
    Column('user_id', Integer),
    Column('bucket', String(length=80)),
    Column('uuid', String(length=80)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['exam'].columns['uuid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['exam'].columns['uuid'].drop()
