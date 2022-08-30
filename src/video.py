class Video:
    def __init__(self, video_id: str, name: str, thumbnail: str):
        self.id = video_id
        self.name = name
        self.thumbnail = thumbnail

    def __str__(self):
        return f"{self.id}, {self.name}, {self.thumbnail}"
