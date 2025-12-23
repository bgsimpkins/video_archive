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

    def get_todo_videos(self):
        with self.engine.connect() as conn:
            stmt = sa.select(self.Video).where(sa.or_(self.Video.id == self.Video.videoName, self.Video.videoName == None))



    # TODO: fix to use list that in from POST
    def add_new_video(self, video):
        session = Session(self.engine)
        # video = self.Video(id=666, videoName = 'test insert')
        session.add(video)
        session.commit()
        session.close()

    def delete_video(self, id):
        session = Session(self.engine)
        vid = session.query(self.Video).filter_by(id=id).first()

        session.delete(vid)
        session.commit()
        session.close()

    # TODO: fix to use list that in from POST
    def update_video(self, id, vid_data):
        session = Session(self.engine)

        vid = session.query(self.Video).filter_by(id=id).first()

        # Nulls are here as 'None' string
        vid.videoName = vid_data["videoName"] if vid_data["videoName"] != "None" else None
        vid.userName = vid_data["userName"] if vid_data["userName"] != "None" else None
        vid.type = self.sort_tags(vid_data["type"]) if vid_data["type"] != "None" else None
        vid.theDate = vid_data["theDate"] if vid_data["theDate"] != "None" else None
        vid.addDate = vid_data["addDate"] if vid_data["addDate"] != "None" else None
        vid.location = vid_data["location"] if vid_data["location"] != "None" else None
        vid.primaryActor = vid_data["primaryActor"] if vid_data["primaryActor"] != "None" else None
        vid.secondaryActor = vid_data["secondaryActor"] if vid_data["userName"] != "None" else None
        vid.description = vid_data["description"] if vid_data["description"] != "None" else None
        vid.link = vid_data["link"] if vid_data["link"] != "None" else None
        vid.originalFile = vid_data["originalFile"] if vid_data["originalFile"] != "None" else None

        session.commit()
        session.close()

    # TODO: Could be made more dynamic by passing in lists/dictionaries for contains, between, etc
    # and looping through them and processing dynamically
    def get_videos_filter_and_sort(
            self,
            todo=False,
            videoname_contains=None,
            tags_contains=None,
            location_contains=None,
            description_contains=None,
            date_between=None,
            sort_var1="theDate DESC",
            sort_var2=None,
            pagination=[1,30]
    ):
        # videoName (contains), type/tag (contains), description (contains), date (between)

        conn = self.engine.connect()

        # Build select statement and append filters if used
        stmt = sa.select(self.Video)

        #### Filters
        if todo:
            stmt = stmt.where(sa.or_(self.Video.id == self.Video.videoName, self.Video.videoName is None))

        else:
            if videoname_contains is not None:
                videoname_contains = videoname_contains.replace(' ', "%")
                stmt = stmt.where(self.Video.videoName.like(f"%{videoname_contains}%"))
            if tags_contains is not None:
                tag_contains = tags_contains.replace(' ', "%")
                stmt = stmt.where(self.Video.type.like(f"%{tag_contains}%"))
            if location_contains is not None:
                location_contains = location_contains.replace(' ', "%")
                stmt = stmt.where(self.Video.location.like(f"%{location_contains}%"))
            if description_contains is not None:
                description_contains = description_contains.replace(' ', "%")
                stmt = stmt.where(self.Video.description.like(f"%{description_contains}%"))
            if date_between is not None:
                stmt = stmt.filter(
                    sa.or_(
                        self.Video.theDate.between(date_between[0], date_between[1]),
                        self.Video.theDate == 0
                    )
                )

        #### Sorting
        if sort_var1 is not None:
            stmt = stmt.order_by(sa.text(sort_var1))

        if sort_var2 is not None:
            stmt = stmt.order_by(sa.text(sort_var2))

        #### Pagination
        # Get total pre-pagination count
        row_count = conn.execute(stmt).rowcount

        stmt = stmt.limit(pagination[1])

        # We've been handling offset as 1-based for display. It's 0-based in MySQL so decrement
        stmt = stmt.offset(pagination[0]-1)
        ####################################

        video_list = []

        # return conn.execute(stmt).first()
        for row in conn.execute(stmt):
            video_list.append(row)

        return video_list, row_count

    def get_all_tags(self):
        tag_dict = {}

        conn = self.engine.connect()
        stmt = sa.select(self.Video)
        for row in conn.execute(stmt):
            if row.type is None:
                continue
            tags = row.type.split()
            for tag in tags:
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1

        return tag_dict

    def get_locations(self):
        loc_list = []

        conn = self.engine.connect()
        stmt = sa.select(self.Video.location).distinct().order_by(self.Video.location)
        for row in conn.execute(stmt):
            loc_list.append(row.location)

        loc_list.remove("")
        loc_list.remove(None)
        return loc_list

    def sort_tags(self, tag_str):
        tag_spl = tag_str.split(" ")
        tag_spl.sort()
        return " ".join(tag_spl)
