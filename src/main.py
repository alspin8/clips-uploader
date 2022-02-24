from clips import Clips
import sched, time
import sys
from clips import Clips
from video import Video
from logger import Logger
import logging

class MainClass():

    s = sched.scheduler(time.time, time.sleep)

    def __init__(self):

        if not len(sys.argv) == 1:
            try:
                arg = self.__gestion_level_logger("".join(sys.argv[1:2]))
                self.logger = Logger(arg).get_logger()
            except ValueError as err:
                self.logger = Logger().get_logger()
                self.logger.error(f"Exit application because of : {err}")
                sys.exit()
        else: 
            self.logger = Logger().get_logger()

        self.__clip = Clips(self.logger)
        self.__upload = Video(self.logger)
        self.rk = 0

    def __gestion_level_logger(self, arg):
        if arg == '--debug': return (logging.DEBUG)
        elif arg == '--info': return (logging.INFO)
        else: raise ValueError("Unvalid args")

    def __maj_clip(self, sc):
        self.rk = 1
        self.__clip.get_clips()

        sc.enter(86400, 1, self.__upload_clip, (sc, ))

    def __upload_clip(self, sc):
        try:
            self.__clip.download_by_rank(self.rk)
            self.__upload.youtube_upload()
            self.rk += 1
        except ValueError as err:
            self.logger.error(f"Exit application because of : {err}")
            sys.exit()
   
        sc.enter(1800, 1, self.__upload_clip, (sc, ))

    def run(self):
        self.logger.info("Starting application !")
        self.__clip.get_token()
        self.s.enter(0, 1, self.__maj_clip, (self.s, ))
        self.s.enter(0, 2, self.__upload_clip, (self.s, ))
        self.s.run()


if __name__ == '__main__':
    start = MainClass()
    start.run()
    start.logger.info("Exit application")
