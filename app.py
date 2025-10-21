import os
import time
from flask import Flask, render_template, request, url_for

from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/video_archive', methods=['GET', 'POST'])
def video_archive():
    pass


if __name__ == '__main__':
    load_dotenv(override=False)
