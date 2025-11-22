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
    videos = db_mapper.get_all_videos()

    for vid in videos:
        print(f"name={vid.videoName}")

    if request.method == 'POST':
        print('POST!')

    return render_template(
        'video_archive.html'
    )


if __name__ == '__main__':

    print('Starting web app..')
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True,
        use_reloader=False
    )
