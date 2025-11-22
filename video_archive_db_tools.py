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
        self.Users = None
        self.Videos = None

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
        self.Videos = base.classes.videos_main
        self.Users = base.classes.users

    def get_all_videos(self) -> list:
        video_list = []
        with self.engine.connect() as conn:
            stmt = sa.select(self.Videos)
            for row in conn.execute(stmt):
                video_list.append(row)
        return video_list
