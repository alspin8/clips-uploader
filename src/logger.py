import logging

class Logger:

    def __init__(self, level=logging.INFO) -> None:
        logging.basicConfig(filename = "../logs/logs.log",      
                            filemode = "a",
                            format = "%(levelname)s %(asctime)s - %(message)s",
                            level = level)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(level)

    def get_logger(self): return self.__logger        