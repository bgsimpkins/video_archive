import os
from typing import List

import mysql.connector
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class DBMapper:

    def __init__(self, config_vals):

        self.engine = None
        self.User = None
        self.Video = None

        self.conn = None
        self.create_engine(config_vals)
        self.map_to_classes()

    def create_engine(self, config_vals):
        self.engine = sa.create_engine(f"mysql+pymysql://{config_vals['DB_USER']}:{config_vals['DB_PASS']}@{config_vals['DB_HOST']}:3306/{config_vals['DB_NAME']}",
                                echo=True)

    def map_to_classes(self):

        base = automap_base()

        # reflect the tables
        base.prepare(self.engine, reflect=True)

        # mapped classes are now created with names by default
        # matching that of the table name.
        self.Video = base.classes.videos_main
        self.User = base.classes.users

    def get_all_videos(self) -> list:
        video_list = []
        with self.engine.connect() as conn:
            stmt = sa.select(self.Video)
            for row in conn.execute(stmt):
                video_list.append(row)
        return video_list

    def get_one_video(self, id):
        with self.engine.connect() as conn:
            stmt = sa.select(self.Video).where(self.Video.id == id)
            vid = conn.execute(stmt).first()

            if vid is None:
                print(f'Video with id {id} not found!!')

        return vid

    # TODO: fix to use list that in from POST
    def add_new_video(self, video):
        session = Session(self.engine)
        # video = self.Video(id=666, videoName = 'test insert')
        session.add(video)
        session.commit()
        session.close()

    def delete_video(self, id):
        pass

    # TODO: fix to use list that in from POST
    def update_video(self, id):
        session = Session(self.engine)
        session.commit()

