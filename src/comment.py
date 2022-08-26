from channel import Channel
from datetime import datetime, timezone

class Comment:
    def __init__(self, content: str, channel: Channel, likes: int, date: str):
        self.content = content
        self.channel = channel
        self.likes = likes

        comment_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        time_ago = current_time - comment_time

        years = time_ago.days // 365
        months = time_ago.days // 30
        days = time_ago.days
        hours = time_ago.seconds // 3600
        minutes = (time_ago.seconds // 60) % 60
        seconds = time_ago.seconds

        times = [("years", years), ("months", months), ("days", days),
                ("hours", hours), ("minutes", minutes), ("seconds", seconds)]
        times = [(time_type, time) for (time_type, time) in times
                if time != 0] + [("seconds", seconds)]
        self.time_ago = f"{times[0][1]} {times[0][0]} ago"

    def __eq__(self, other: object):
        if isinstance(other, Comment):
            return (self.content == other.content
                    and self.channel == other.channel)
        return False

    def __str__(self):
        return f"{self.content}"

    def __hash__(self):
        return hash((self.content, self.channel))