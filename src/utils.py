import requests
import json
from collections import Counter
from copy import deepcopy

from typing import List

API_URL = "https://youtube.googleapis.com/youtube/v3"
MAX_RESULTS = 100

class Comment:
    def __init__(self, content, channel, likes):
        self.content = content
        self.channel = channel
        self.likes = likes

    def __eq__(self, other):
        if isinstance(other, Comment):
            return (self.content == other.content
                    and self.channel == other.channel)
        return False

    def __str__(self):
        return f"{self.content}"

    def __hash__(self):
        return hash((self.content, self.channel))

class Channel:
    def __init__(self, channel_id, name, image_url):
        self.id = channel_id
        self.name = name
        self.image_url = image_url

    def __eq__(self, other):
        if isinstance(other, Channel):
            return self.id == other.id
        return False

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)

def write_json(resource, params, file_path):
    uri = f"{API_URL}/{resource}"
    with open(file_path, "wb") as jsonfile:
        jsonfile.write(requests.get(uri, params).content)

def write_top_comments(max_comments, video_id, auth_key, file_path):
    params = {
        "maxResults": max_comments,
        "textFormat": "plainText",
        "videoId": video_id,
        "key": auth_key,
        "order": "relevance"
    }
    write_json("commentThreads", params, file_path)

def write_replies(comment_id, video_id, auth_key, file_path):
    params = {
        "part": "snippet",
        "textFormat": "plainText",
        "parentId": comment_id,
        "videoId": video_id,
        "maxResults": MAX_RESULTS,
        "key": auth_key
    }
    write_json("comments", params, file_path)

def write_channel_info(channel_id, auth_key, file_path):
    params = {
        "part": ["snippet", "statistics"],
        "id": channel_id,
        "key": auth_key,
    }
    write_json("channels", params, file_path)

def read_json(file_path):
    with open(file_path, "r", encoding="utf8") as jsonfile:
        return json.load(jsonfile)

def get_replies(video_id: str, auth_key: str, data_dir: str,
                comments_sampled: int=MAX_RESULTS) -> List[Comment]:
    """
    Return a list of replies to top comments by saving them to JSON and
    reading it.
    """
    top_comments_path = f"{data_dir}/top_comments.json"
    write_top_comments(comments_sampled, video_id, auth_key, top_comments_path)
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
                            snippet["likeCount"])
            replies.append(reply)
    return replies

def aggregate_channels(replies: List[Comment]) -> List[Channel]:
    """
    Return a list of channels sorted by the number of replies made.
    """
    channel_count = Counter([reply.channel for reply in replies])
    return [data[0] for data in channel_count.most_common()]

def aggregate_replies(replies: List[Comment], minimum: int) -> List[Comment]:
    """
    Return a list of replies sorted by frequency that appear at least minimum
    times.
    """
    reply_count = Counter(replies)
    return [data[0] for data in reply_count.most_common()
            if data[1] >= minimum]

def filter_replies(replies: List[Comment], channels: List[Channel],
                   top: int=None, sample: int=None) -> List[Comment]:
    """
    Return a list of replies that are not replies to other comments and were
    made by one of the top channels.
    """
    filtered_replies = []
    filtered_channels = deepcopy(channels)
    for reply in replies:
        if "@" in reply.content:
            if reply.channel in filtered_channels:
                filtered_channels.remove(reply.channel)
        else:
            filtered_replies.append(reply)

    if top is None:
        top = len(filtered_channels)
    result = []
    for channel in filtered_channels[:top]:
        channel_replies = [
            reply for reply in filtered_replies if reply.channel == channel
        ]
        if sample is None:
            sample = len(channel_replies)
        result.extend(channel_replies[:sample])
    return result

def get_top_filtered_replies(replies: List[Comment], n_channels: int=5,
                             minimum: int=1, sample: int=3,
                             duplicates=False) -> List[Comment]:
    """
    Return a list of replies with sample replies from each of the top
    n_channels commenters that appear at least minimum times.
    """
    top_channels = aggregate_channels(replies)
    filtered_replies = filter_replies(replies, top_channels,
                                      top=n_channels, sample=sample)

    top_replies = aggregate_replies(filtered_replies, minimum)
    result = [reply for reply in filtered_replies if reply in top_replies]

    if duplicates:
        return result
    else:
        return list(dict.fromkeys(result))

def format_replies(replies: List[Comment]) -> str:
    result = (f"Channel: {replies[0].channel}\n"
                f"{replies[0]} 👍{replies[0].likes}\n")
    for idx in range(1, len(replies)):
        if replies[idx].channel != replies[idx - 1].channel:
            result += f"\nChannel: {replies[idx].channel}\n"

        result += f"{replies[idx]} 👍{replies[idx].likes}\n"
    return result
