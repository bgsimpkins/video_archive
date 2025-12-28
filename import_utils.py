import os
import sys

from dotenv import load_dotenv
import shutil
from video_archive_db_tools import DBMapper
from sqlalchemy.orm import Session
import sqlalchemy as sa
from datetime import datetime


def batch_import(config_vals):

    print("____________Running batch import")
    supported_containers = ['mp4','mod']

    import_dir=config_vals['IMPORT_DIR']

    db_mapper = DBMapper(config_vals)
    session = Session(db_mapper.engine)

    files = [f for f in os.listdir(import_dir) if os.path.isfile(os.path.join(import_dir, f))]
    for file in files:
        print(f"processing file: {file}")
        format = file.lower().split(".")[-1]
        # if format not in supported_containers:
        #     continue

        # Create base Video record
        vid = db_mapper.Video()

        try:
            timestamp = datetime.strptime(file.split(".")[0], "%Y%m%d_%H%M%S")
        except ValueError:
            print("Couldn't parse time. Default to None")
            timestamp = None

        # Old id generating system was random, limited, and stupid. Just get max id and increment to get new one
        conn = db_mapper.engine.connect()
        max_id = conn.execute(sa.text("SELECT max(ID) FROM videos_main")).first()[0]
        new_id = max_id + 1

        # TODO: If mod, run ffmpeg to convert. Set file to new filename
        if format != "mp4":
            print(f"Attempting to covert file of type {format}!....")
            ffmpeg_call = f"ffmpeg -nostdin -y -i '{os.path.join(import_dir, file)}' -c:v libx264 -c:a aac -crf 10 -preset:v medium static/videos/{new_id}.mp4"
            os.system(ffmpeg_call)

        else:
            # Copy to videos dir
            shutil.copyfile(os.path.join(import_dir, file), f"static/videos/{new_id}.mp4")

        vid.id = new_id
        vid.videoName = vid.id
        vid.theDate = timestamp
        vid.addDate = datetime.now()
        vid.userName = 'bsimpkins'
        vid.originalFile = file

        vid.link = f"videos/{new_id}.mp4"

        session.add(vid)
        session.commit()



        # Create and save thumbnail
        ffmpeg_call = f"ffmpeg -nostdin -y -i static/{vid.link} -ss 00:00:02.000 -vframes 1 static/thumbnails/{new_id}.jpg"
        os.system(ffmpeg_call)

        # Remove video from import dir
        os.remove(os.path.join(import_dir, file))

    session.close()


def duplicate_check_bytes():
    print("____________Running duplicate check based on bytes!")

    filesize_dict = {}

    files = [f for f in os.listdir("static/videos") if os.path.isfile(os.path.join("static/videos", f))]
    for file in files:

        file_size = os.path.getsize(f"static/videos/{file}")

        # TODO: Catch key expection here to look for dups
        filesize_dict[file_size] = file

    print(filesize_dict)


def show_tags_used(config_vals):

    db_mapper = DBMapper(config_vals)
    tags_dict = db_mapper.get_all_used_tags()
    print(tags_dict)


def sort_tags(config_vals):
    db_mapper = DBMapper(config_vals)
    session = Session(db_mapper.engine)
    # stmt = session.query(db_mapper.Video)
    stmt = sa.select(db_mapper.Video)

    for vid in session.execute(stmt).scalars():
        if vid.type is not None:
            tag_spl = vid.type.split()
            tag_spl.sort()
            print(tag_spl)
            vid.type = " ".join(tag_spl)

    session.commit()
    session.close()


if __name__ == '__main__':
    load_dotenv(override=False)
    # load_dotenv(dotenv_path="/home/bsimpkins/PycharmProjects/video_archive/.env")

    config_vals = {
        "DB_HOST": os.getenv('DB_HOST'),
        "DB_NAME": os.getenv('DB_NAME'),
        "DB_USER": os.getenv('DB_USER'),
        "DB_PASS": os.getenv('DB_PASS'),
        "IMPORT_UTILS_PROCESSES": os.getenv("IMPORT_UTILS_PROCESSES"),
        "IMPORT_DIR": os.getenv('IMPORT_DIR'),
        "SORT_TAGS": os.getenv('SORT_TAGS')

    }

    process_list=config_vals["IMPORT_UTILS_PROCESSES"].split()

    if "BATCH_IMPORT" in process_list:
        batch_import(config_vals)
    if "DUPLICATE_CHECK_BYTES" in process_list:
        duplicate_check_bytes()
    if "SHOW_ALL_TAGS_USED" in process_list:
        show_tags_used(config_vals)
    if "SORT_TAGS" in process_list:
        sort_tags(config_vals)