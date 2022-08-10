from channel import Channel

class Comment:
    def __init__(self, content: str, channel: Channel, likes: int):
        self.content = content
        self.channel = channel
        self.likes = likes

    def __eq__(self, other: object):
        if isinstance(other, Comment):
            return (self.content == other.content
                    and self.channel == other.channel)
        return False

    def __str__(self):
        return f"{self.content}"

    def __hash__(self):
        return hash((self.content, self.channel))