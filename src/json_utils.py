import requests
import json

from typing import List
from channel import Channel
from comment import Comment

API_URL = "https://youtube.googleapis.com/youtube/v3"
MAX_RESULTS = 100

def write_json(resource: str, params: dict, file_path: str) -> None:
    """
    Make a http request with params and write the returned data to a JSON file.
    """
    uri = f"{API_URL}/{resource}"
    with open(file_path, "wb") as jsonfile:
        jsonfile.write(requests.get(uri, params).content)

def write_top_comments(video_id: str, auth_key: str, file_path: int,
                       max_comments: int=MAX_RESULTS) -> None:
    """
    Write the comment IDs of at most max_comments to a JSON file.
    """
    params = {
        "maxResults": max_comments,
        "textFormat": "plainText",
        "videoId": video_id,
        "key": auth_key,
        "order": "relevance"
    }
    write_json("commentThreads", params, file_path)

def write_replies(comment_id: str, video_id: str, auth_key: str,
                  file_path: str) -> None:
    """
    Write the comment data of replies to a top level comment to a JSON file.
    """
    params = {
        "part": "snippet",
        "textFormat": "plainText",
        "parentId": comment_id,
        "videoId": video_id,
        "maxResults": MAX_RESULTS,
        "key": auth_key
    }
    write_json("comments", params, file_path)

def write_relevant_video(query: str, auth_key: str, file_path: str) -> None:
    """
    Write the most relevant video to query to a JSON file.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": auth_key
    }
    write_json("search", params, file_path)

def read_json(file_path: str) -> dict:
    """
    Return the JSON file found at file_path as a dict.
    """
    with open(file_path, "r", encoding="utf8") as jsonfile:
        return json.load(jsonfile)

def get_replies(video_id: str, auth_key: str, data_dir: str,
                comments_sampled: int=MAX_RESULTS) -> List[Comment]:
    """
    Return a list of replies to top comments by saving them to a JSON file and
    reading it.
    """
    top_comments_path = f"{data_dir}/top_comments.json"
    write_top_comments(video_id, auth_key, top_comments_path, comments_sampled)
    top_comments_data = read_json(top_comments_path)
    comment_ids = [
        comment_data["id"] for comment_data in top_comments_data["items"]
    ]
    replies = []
    replies_path = f"{data_dir}/replies.json"
    for comment_id in comment_ids:
        write_replies(comment_id, video_id, auth_key, replies_path)
        replies_data = read_json(replies_path)

        for reply_data in replies_data["items"]:
            snippet = reply_data["snippet"]
            channel = Channel(snippet["authorChannelId"]["value"],
                              snippet["authorDisplayName"],
                              snippet["authorProfileImageUrl"])
            reply = Comment(snippet["textDisplay"], channel,
                            snippet["likeCount"], snippet["publishedAt"])
            replies.append(reply)
    return replies

def serialize_top_filtered_replies(replies: List[Comment]) -> str:
    """
    Serialize the data of top filtered comments to a JSON string.
    """
    json_data = {}
    if len(replies) != 0:
        json_data["items"] = []
        last_idx = len(replies) - 1

        channel_replies = []
        for idx in range(len(replies)):
            channel_replies.append({
                "content": replies[idx].content,
                "likes": replies[idx].likes,
                "time_ago": replies[idx].time_ago
            })

            if (idx != last_idx
                    and replies[idx + 1].channel != replies[idx].channel):
                json_data["items"].append({
                    "channel_name": replies[idx].channel.name,
                    "image_url": replies[idx].channel.image_url,
                    "comments": channel_replies
                })
                channel_replies = []
                
        json_data["items"].append({
            "channel_name": replies[last_idx].channel.name,
            "image_url": replies[idx].channel.image_url,
            "comments": channel_replies
        })

    return json.dumps(json_data)

def get_relevant_video(query: str, auth_key: str, data_dir: str) -> str:
    """
    Return the video ID the most relevant video to query by saving it to a
    JSON file and reading it.
    """
    relevant_video_path = f"{data_dir}/relevant_video.json"
    write_relevant_video(query, auth_key, relevant_video_path)

    relevant_video_data = read_json(relevant_video_path)
    return relevant_video_data["items"][0]["id"]["videoId"]
