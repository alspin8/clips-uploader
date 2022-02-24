from youtube_uploader_selenium import YouTubeUploader
from Constants import Constant

class Video:

    RANK_TO_DOWNLOAD = 1

    def __init__(self, logger) -> None:
        self.logger = logger

    def youtube_upload(self):
        self.logger.info("Starting upload video on youtube...")
        uploader = YouTubeUploader(Constant.VIDEO_PATH, Constant.METADATA_PATH, logger=self.logger)
        was_video_uploaded, video_id = uploader.upload()
        assert was_video_uploaded
        self.logger.info("Succesfully upload !")
