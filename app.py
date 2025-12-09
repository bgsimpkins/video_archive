import os
from flask import Flask, render_template, request
from video_archive_db_tools import DBMapper
from dotenv import load_dotenv
import datetime

load_dotenv(override=False)

config_vals = {
    "DB_HOST": os.getenv('DB_HOST'),
    "DB_NAME": os.getenv('DB_NAME'),
    "DB_USER": os.getenv('DB_USER'),
    "DB_PASS": os.getenv('DB_PASS')

}

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def video_archive():

    db_mapper = DBMapper(config_vals)
    # videos = db_mapper.get_all_videos()

    videoname_contains = None
    description_contains = None

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

    if request.method == 'POST':
        # post = request.form
        # print('POST!')

        # TODO: This is pretty hard-coded. Could be handled more eloquently
        for x in request.form.items():

            if x[0] == "clear_filters":
                return render_template(
                    'video_archive.html',
                    filter_options=filter_options,
                    videos=db_mapper.get_videos_filter_and_sort()
                )

            # Handle all filters
            if x[0] == 'videoName_input':
                videoname_contains = request.form['videoName_input']
                selected_filter_list.append(["videoName", "Video Name =", videoname_contains])
                filter_options.pop('videoName')
            if x[0] == 'description_input':
                description_contains = request.form['description_input']
                selected_filter_list.append(["description", "Video Description =", description_contains])
                filter_options.pop('description')

            # Handling in JS now
            # # If clicked filter x button remove from selected list
            # elif "_remove.x" in x[0]:
            #     # input of type image returns two vals. One for x and one for x of click.
            #     to_remove = x[0].replace("_remove.x","")

    # TODO: It would better if this function took the form input values in a collection instead of individually so can handle dynamically
    videos = db_mapper.get_videos_filter_and_sort(
        videoname_contains=videoname_contains,
        description_contains=description_contains
    )

    return render_template(
        'video_archive.html',
        filter_options=filter_options,
        selected_filter_list=selected_filter_list,
        videos=videos
    )


@app.route('/video_detail', methods=['GET', 'POST'])
def video_detail():

    id = request.args.get('id')
    db_mapper = DBMapper(config_vals)

    vid = db_mapper.get_one_video(id)

    alert_text = None

    if request.method == 'POST':

        if 'thumbnail_input' in request.form:
            thumbnail_time = str(datetime.timedelta(seconds=int(request.form["thumbnail_input"])))
            ffmpeg_call = f"ffmpeg -y -i static/{vid.link} -ss {thumbnail_time} -vframes 1 static/thumbnails/{vid.id}.jpg"
            os.system(ffmpeg_call)
            alert_text = "Thumbnail updated!"

        else:
            print(f"updating video {id}")
            db_mapper.update_video(id, request.form)



    return render_template(
        'video_detail.html',
        video=vid,
        alert_text=alert_text
    )


if __name__ == '__main__':

    print('Starting web app..')
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True,
        use_reloader=False
    )
