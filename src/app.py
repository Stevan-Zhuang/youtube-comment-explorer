from json_utils import get_replies, serialize_top_filtered_replies
from json_utils import get_video, serialize_video
from utils import get_top_filtered_replies
from flask import Flask, render_template, request, abort
import re
import os
from dotenv import load_dotenv

CHANNELS_TO_LOAD = 5

load_dotenv()
auth_key = os.environ['AUTH_KEY']

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results")
def results():
    if not "search_query" in request.args:
        abort(400, description="No search query specified")
    
    search = request.args["search_query"]
    if search.startswith("https://www.youtube.com/watch"):
        # Take the video id out of the url
        try:
            search = re.search("\?v=[^&]+(&|$)", search).group()
            search = search[len("?v="):]
            if search.endswith("&"):
                search = search[:-1]
        except:
            pass

    try:
        video = get_video(search, True, auth_key, "data")
    except:
        video = get_video(search, False, auth_key, "data")
        search = video.id

    replies = get_replies(search, auth_key, "data")
    replies = get_top_filtered_replies(replies)

    replies_data = serialize_top_filtered_replies(replies)
    video_data = serialize_video(video)

    return render_template(
        "results.html", replies=replies_data, video=video_data,
        n_to_load_total=len(replies), n_to_load=CHANNELS_TO_LOAD
    )

if __name__ == "__main__":
    app.run()
