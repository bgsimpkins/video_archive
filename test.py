import os
from video_archive_db_tools import DBMapper
from pathlib import Path
import sqlalchemy as sa

from dotenv import load_dotenv

dotenv_path = Path('/home/bsimpkins/PycharmProjects/video_archive/.env')
load_dotenv(dotenv_path=dotenv_path)


def test_query_engine(
        db_mapper,
        videoname_contains=None,
        tag_contains=None,
        description_contains=None,
        date_between=None,
        sort_var1=None,
        sort_var2=None
):
    # videoName (contains), type/tag (contains), description (contains), date (between)

    conn = db_mapper.engine.connect()

    # Build select statement and append filters if used
    stmt = sa.select(db_mapper.Video)

    if videoname_contains is not None:
        videoName_contains = videoname_contains.replace(' ', "%")
        stmt = stmt.where(db_mapper.Video.videoName.like(f"%{videoname_contains}%"))
    if tag_contains is not None:
        tag_contains = tag_contains.replace(' ', "%")
        stmt = stmt.where(db_mapper.Video.type.like(f"%{tag_contains}%"))
    if description_contains is not None:
        description_contains = description_contains.replace(' ', "%")
        stmt = stmt.where(db_mapper.Video.description.like(f"%{description_contains}%"))
    if date_between is not None:
        stmt = stmt.filter(db_mapper.Video.theDate.between(date_between[0], date_between[1]))

    if sort_var1 is not None:
        stmt = stmt.order_by(sa.text(sort_var1))

    if sort_var2 is not None:
        stmt = stmt.order_by(sa.text(sort_var2))

    #return conn.execute(stmt).first()
    return conn.execute(stmt)



config_vals = {
    "DB_HOST": os.getenv('DB_HOST'),
    "DB_NAME": os.getenv('DB_NAME'),
    "DB_USER": os.getenv('DB_USER'),
    "DB_PASS": os.getenv('DB_PASS')

}

db_mapper = DBMapper(config_vals)

## Test Query Engine
# res = test_query_engine(db_mapper,
#     #videoname_contains = "Baby Benny",
#     tag_contains = None,
#     description_contains = "Benny Play",
#     #date_between = ['2008-01-01','2010-01-01'],
#
#     sort_var1 = "theDate"
#                   )

res = db_mapper.get_videos_filter_and_sort(
    videoname_contains = "Thomas",
    tag_contains = None,
    description_contains = "Benny Play",
    #date_between = ['2008-01-01','2010-01-01'],

    sort_var1 = "theDate"
                  )

for r in res:
    print(r)