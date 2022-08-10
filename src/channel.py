class Channel:
    def __init__(self, channel_id: str, name: str, image_url: str):
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