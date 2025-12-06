import os
import time
from flask import Flask, render_template, request, url_for
from video_archive_db_tools import DBMapper
from dotenv import load_dotenv

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
            elif x[0] == 'videoName_input':
                videoname_contains = request.form['videoName_input']
                selected_filter_list.append(["videoName", "Video Name =", videoname_contains])
                filter_options.pop('videoName')
            elif x[0] == 'description_input':
                description_contains = request.form['description_input']
                selected_filter_list.append(["description", "Video Description =", description_contains])
                filter_options.pop('description')

            # Handling in JS now
            # # If clicked filter x button remove from selected list
            # elif "_remove.x" in x[0]:
            #     # input of type image returns two vals. One for x and one for x of click.
            #     to_remove = x[0].replace("_remove.x","")

                # TODO: Repopulate dropdown with one that was removed


    # TODO: It would better if this function took the form input values in the request.form[] collection instead of individually
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


if __name__ == '__main__':

    print('Starting web app..')
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True,
        use_reloader=False
    )
