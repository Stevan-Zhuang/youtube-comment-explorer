from channel import Channel
from datetime import datetime

class Comment:
    def __init__(self, content: str, channel: Channel, likes: int, date: str):
        self.content = content
        self.channel = channel
        self.likes = likes

        comment_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.today()
        time_ago = current_time - comment_time

    def __eq__(self, other: object):
        if isinstance(other, Comment):
            return (self.content == other.content
                    and self.channel == other.channel)
        return False

    def __str__(self):
        return f"{self.content}"

    def __hash__(self):
        return hash((self.content, self.channel))