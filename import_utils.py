import os
from dotenv import load_dotenv
import shutil
from video_archive_db_tools import DBMapper
from sqlalchemy.orm import Session
import sqlalchemy as sa
from datetime import datetime


def batch_import(config_vals):

    supported_containers = ['mp4','mod']

    import_dir=config_vals['IMPORT_DIR']

    db_mapper = DBMapper(config_vals)
    session = Session(db_mapper.engine)

    files = [f for f in os.listdir(import_dir) if os.path.isfile(os.path.join(import_dir, f))]
    for file in files:

        format = file.lower().split(".")[-1]
        if format not in supported_containers:
            continue

        # TODO: If mod, run ffmpeg to convert. Set file to new filename
        if format == "mod":
            pass

        # Create base Video record
        vid = db_mapper.Video()

        timestamp = datetime.strptime(file.split(".")[0], "%Y%m%d_%H%M%S")

        #Old id generating system was random, limited, and stupid. Just get max id and increment to get new one
        conn = db_mapper.engine.connect()
        max_id = conn.execute(sa.text("SELECT max(ID) FROM videos_main")).first()[0]

        vid.id = max_id + 1
        vid.videoName = vid.id
        vid.theDate = timestamp
        vid.addDate = datetime.now()
        vid.userName = 'bsimpkins'
        vid.originalFile = file

        vid.link = f"videos/{vid.id}.{format}"

        session.add(vid)
        session.commit()

        # Copy to videos dir
        shutil.copyfile(os.path.join(import_dir, file), f"static/videos/{vid.id}.{format}")

        #Create and save thumbnail
        ffmpeg_call = f"ffmpeg -i static/{vid.link} -ss 00:00:02.000 -vframes 1 static/thumbnails/{vid.id}.jpg"
        os.system(ffmpeg_call)

        #Remove video from import dir
        os.remove(os.path.join(import_dir, file))


    session.close()


if __name__ == '__main__':
    load_dotenv(override=False)
    #load_dotenv(dotenv_path="/home/bsimpkins/PycharmProjects/video_archive/.env")

    config_vals = {
        "DB_HOST": os.getenv('DB_HOST'),
        "DB_NAME": os.getenv('DB_NAME'),
        "DB_USER": os.getenv('DB_USER'),
        "DB_PASS": os.getenv('DB_PASS'),
        "IMPORT_DIR": os.getenv('IMPORT_DIR')

    }

    batch_import(config_vals)