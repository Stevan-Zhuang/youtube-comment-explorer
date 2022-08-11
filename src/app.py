from json_utils import get_replies
from utils import get_top_filtered_replies, format_replies
from flask import Flask, render_template, request, abort
import re
import os
from dotenv import load_dotenv

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
        print(search)
        replies = get_replies(search, auth_key, "data")
        parameters = {
            "n_reply": len(replies),
            "replies": format_replies(get_top_filtered_replies(replies))
        }
        return render_template("results.html", params=parameters)
    except:
        # Do video search instead
        abort(400, description="Invalid search (temporary error)")


if __name__ == "__main__":
    app.run()