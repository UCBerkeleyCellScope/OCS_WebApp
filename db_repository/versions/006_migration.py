from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
eye_image = Table('eye_image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image_date', DateTime),
    Column('technician', String(length=40)),
    Column('eye', Boolean),
    Column('imageURL', String(length=80)),
    Column('fixationLight', SmallInteger),
    Column('exam_id', Integer),
    Column('thumbnail', LargeBinary),
    Column('imageKey', String(length=80)),
    Column('uuid', String(length=80)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['eye_image'].columns['uuid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['eye_image'].columns['uuid'].drop()
