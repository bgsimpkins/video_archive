import os
import sys
from flask import Flask, render_template, request, redirect, url_for
from video_archive_db_tools import DBMapper
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import datetime

load_dotenv(override=False)

config_vals = {
    "DB_HOST": os.getenv('DB_HOST'),
    "DB_NAME": os.getenv('DB_NAME'),
    "DB_USER": os.getenv('DB_USER'),
    "DB_PASS": os.getenv('DB_PASS'),
    "TESTING": os.getenv('TESTING')

}

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def video_archive():
    db_mapper = DBMapper(config_vals)
    # videos = db_mapper.get_all_videos()

    alert_text = None

    if "deleted_id" in request.args:
        deleted_id = request.args.get("deleted_id")
        alert_text = f"Video id={deleted_id} deleted!"

    if 'new_video_file' in request.files:
        file = request.files['new_video_file']
        if file.filename == "":
            return 'No file selected, dummy!', 400
        else:
            format = file.filename.lower().split(".")[-1]

            if format != "mp4":
                alert_text = "Only mp4 files are supported!"
            filename = secure_filename(file.filename)
            file_id = db_mapper.add_new_video(filename)
            file.save(f"static/videos/{file_id}.{format}")

            # Create and save thumbnail
            ffmpeg_call = f"ffmpeg -i static/videos/{file_id}.{format} -ss 00:00:02.000 -vframes 1 static/thumbnails/{file_id}.jpg"
            os.system(ffmpeg_call)

            return redirect(f"{url_for('video_detail')}?id={file_id}&edit=true")

    # Special filter to show videos that need metadata added
    todo_filter = False

    videoname_contains = None
    description_contains = None
    location_contains = None
    tags_contains = None
    date_between = ['1970-01-01', '9999-12-31']

    # Filter options combo box. Remove items that are in POST
    filter_options = {
        "videoName": "Video Name",
        "description": "Video Description",
        "location": "Location",
        "tags": "Tags",
        "theDate": "Recorded Date"
    }

    # 3-element list-
    # 0: field name |  1: field label | 2: field value
    selected_filter_list = []

    # 0: Num records | 1: offset | 2: limit/range
    pagination_list = [30, 1, 30]

    if request.method == 'POST':
        # post = request.form
        # print('POST!')

        pagination_list[1] = int(request.form['pagination_offset'])

        if "todo_submit" in request.form:
            todo_filter = True
            pagination_list[1] = 1
        elif "todo" in request.form:
            todo_filter = True

        # TODO: This is pretty hard-coded. Could be handled more eloquently
        for x in request.form.items():

            if x[0] == "clear_filters":
                pagination_list[1] = 1
                videos, pagination_list[0] = db_mapper.get_videos_filter_and_sort(
                    pagination=[pagination_list[1], pagination_list[2]]
                )
                return render_template(
                    'video_archive.html',
                    filter_options=filter_options,
                    videos=videos,
                    pagination_list=pagination_list
                )
            elif x[0] == "next_page":
                pagination_list[1] = int(pagination_list[1]) + int(pagination_list[2])
            elif x[0] == "prev_page":
                pagination_list[1] = int(pagination_list[1]) - int(pagination_list[2])
            elif x[0] == "add_filter":
                pagination_list[1] = 1

            # Handle all filters
            if not todo_filter:
                if x[0] == 'videoName_input':
                    videoname_contains = request.form['videoName_input']
                    selected_filter_list.append(["videoName", "Video Name =", videoname_contains])
                    filter_options.pop('videoName')

                if x[0] == 'description_input':
                    description_contains = request.form['description_input']
                    selected_filter_list.append(["description", "Video Description =", description_contains])
                    filter_options.pop('description')

                if x[0] == 'location_input':
                    location_contains = request.form['location_input']
                    selected_filter_list.append(["location", "Location =", location_contains])
                    filter_options.pop('location')

                if x[0] == 'tags_input':
                    tags_contains = request.form['tags_input']
                    # Sort tags
                    tag_spl = tags_contains.split(" ")
                    tag_spl.sort()
                    tags_contains = " ".join(tag_spl)
                    selected_filter_list.append(["tags", "Tags =", tags_contains])
                    filter_options.pop('tags')

                if x[0] == "date_start_input":
                    date_between = [request.form['date_start_input'], request.form['date_end_input']]
                    selected_filter_list.append(["theDate", "Date Range =", f"{date_between[0]} to {date_between[1]}"])
                    filter_options.pop('theDate')

                if x[0] == 'theDate_input':
                    date_spl = request.form['theDate_input'].split("to")
                    date_between = [date_spl[0].strip(), date_spl[1].strip()]
                    selected_filter_list.append(
                        ["theDate", "Date Range =", f"{date_spl[0].strip()} to {date_between[1].strip()}"])
                    # filter_options.pop('theDate')

    # TODO: It would better if this function took the form input values in a collection instead of individually so can handle dynamically
    videos, pagination_list[0] = db_mapper.get_videos_filter_and_sort(
        todo=todo_filter,
        videoname_contains=videoname_contains,
        description_contains=description_contains,
        location_contains=location_contains,
        tags_contains=tags_contains,
        date_between=date_between,
        pagination=[pagination_list[1], pagination_list[2]]
    )

    return render_template(
        'video_archive.html',
        filter_options=filter_options,
        selected_filter_list=selected_filter_list,
        videos=videos,
        pagination_list=pagination_list,
        todo=todo_filter,
        alert_text=alert_text
    )


@app.route('/video_detail', methods=['GET', 'POST'])
def video_detail():
    id = request.args.get('id')
    edit = True if 'edit' in request.args else None
    db_mapper = DBMapper(config_vals)

    vid = db_mapper.get_one_video(id)

    alert_text = None

    if request.method == 'POST':

        if 'thumbnail_input' in request.form:
            thumbnail_time = str(datetime.timedelta(seconds=int(request.form["thumbnail_input"])))
            ffmpeg_call = f"ffmpeg -nostdin -y -i static/{vid.link} -ss {thumbnail_time} -vframes 1 static/thumbnails/{vid.id}.jpg"
            os.system(ffmpeg_call)
            alert_text = "Thumbnail updated!"

        elif 'delete_video_button_submit' in request.form:
            print(f"____Deleting video: {id}")
            db_mapper.delete_video(id)
            os.remove(f"static/videos/{vid.id}.mp4")
            os.remove(f"static/thumbnails/{vid.id}.jpg")
            return redirect(f"{url_for('video_archive')}?deleted_id={id}")

        else:
            print(f"updating video {id}")
            db_mapper.update_video(id, request.form)
            vid = db_mapper.get_one_video(id)



    return render_template(
        'video_detail.html',
        video=vid,
        alert_text=alert_text,
        edit=edit,
        location_list=db_mapper.get_locations(),
        tag_list=db_mapper.get_tags()
    )


@app.route('/video_tags', methods=['GET', 'POST'])
def video_tags():
    return render_template(
        'video_tags.html'
    )


@app.route('/get_tags', methods=['GET', 'POST'])
def get_tags():
    db_mapper = DBMapper(config_vals)

    return db_mapper.get_all_used_tags()


@app.route('/get_locations', methods=['GET', 'POST'])
def get_locations():
    db_mapper = DBMapper(config_vals)

    return db_mapper.get_locations()


if __name__ == '__main__':
    print('Starting web app..')

    # Start on 5004 for debugging. Command line argument <1> should be 5003 for prod.
    port = 5004 if len(sys.argv) == 1 else sys.argv[1]
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        use_reloader=False
    )
