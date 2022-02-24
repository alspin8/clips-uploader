from itertools import zip_longest, islice
import requests, time, urllib.request, logging
from utils import FileUtils, date_format
from Constants import Constant

class Clips:

    def __init__(self, logger, nb_streamer=50, nb_clips=100):

        self.logger = logger
        self.logger.debug("Clips class init")
        self.nb_streamer = nb_streamer
        self.nb_clips_per_streamer = nb_clips

        self.__streamers = FileUtils.get_dict_from_jsonfile(Constant.REL_STREAMERS_PATH)
        self.__streamers = dict(islice(self.__streamers.items(), self.nb_streamer + 1))

        self.__client_id = FileUtils.get_dict_from_jsonfile(Constant.REL_CONF_PATH)["twitch"]["client_id"]
        self.__client_secret = FileUtils.get_dict_from_jsonfile(Constant.REL_CONF_PATH)["twitch"]["secret_id"]

        self.__headers = {}

        rfc_3339_nosecfrac = "%Y-%m-%dT%H:%M:%SZ"
        self.start = time.strftime(rfc_3339_nosecfrac, time.gmtime(time.time() - 86400))



    def __convert_thumb_mp4(self, url):
        self.logger.debug("Download url génération")
        to_replace_start_index = url.find('-preview')
        str_to_replace = url[to_replace_start_index:len(url)]
        return url.replace(str_to_replace, '.mp4')

    def __add_clip_to_dict(self, clip, name, dict):
        self.logger.debug(f"Add {name} clip to dictionary")
        new_dict = dict.copy()
        new_dict[f"{name}-{clip[Constant.CREATED_AT_KEY]}"] = {
            Constant.RANK_KEY: None,
            Constant.NAME_KEY: name,
            Constant.TITLE_KEY: clip[Constant.TITLE_KEY],
            Constant.CREATED_AT_KEY: clip[Constant.CREATED_AT_KEY],
            Constant.DURATION_KEY: clip[Constant.DURATION_KEY],
            Constant.VIEW_COUNT_KEY: clip[Constant.VIEW_COUNT_KEY],
            Constant.CLIP_URL_KEY: clip[Constant.CLIP_URL_KEY],
            Constant.CLIP_DOWNLOAD_URL_KEY: self.__convert_thumb_mp4(clip[Constant.THUMB_URL_KEY])
        }
        return new_dict

    def __get_user(self, streamer): return requests.get(f'{Constant.USER_URL}{streamer}', headers=self.__headers).json()

    def __get_clip(self, user_id): return requests.get(f'{Constant.CLIP_URL}{user_id}&started_at={self.start}&frist={self.nb_clips_per_streamer}',
                                           headers=self.__headers)

    def __get_dict_sorting_and_ranking(self, dict):
        self.logger.debug("Dictionary sorting")
        sorted_dict = {}
        clips_tuple = sorted(dict.items(), key=lambda item: item[1][Constant.VIEW_COUNT_KEY], reverse=True)[0:48]
        for (k, v), rk in zip_longest(clips_tuple, range(1, len(clips_tuple) + 1)):
            sorted_dict[k] = v
            sorted_dict[k][Constant.RANK_KEY] = rk
        return sorted_dict 

    def __set_metadata(self, dict):
        self.logger.debug("Clip metadata init")
        metadata = {
            Constant.TITLE_KEY: f"{dict[Constant.NAME_KEY]} - {dict[Constant.TITLE_KEY]}",
            Constant.DESCRIPTION_KEY: {
                '0': Constant.MAIN_DESCRIPTION,
                '1': ' ',
                '2': "Crédits :",
                '3': f" Streamer : {dict[Constant.NAME_KEY]}",
                '4': f" Date du clip : {date_format(dict[Constant.CREATED_AT_KEY])}",
                '5': f" Lien du clip : {dict[Constant.CLIP_URL_KEY]}",
                '6': ' ',
                '7': f"#{dict[Constant.NAME_KEY]} {Constant.TAGS}"
            },
        }
        return metadata

    def get_token(self):
        self.logger.info("Getting token...")
        bearer_token = requests.post(f"https://id.twitch.tv/oauth2/token"
                        f"?client_id={self.__client_id}"
                        f"&client_secret={self.__client_secret}"
                        "&grant_type=client_credentials").json()['access_token']

        self.logger.debug(bearer_token)

        self.__headers = { 
            'Client-ID': self.__client_id, 
            'Authorization': f'Bearer {bearer_token}' 
        }

    def get_clips(self):
        self.logger.info("Start request...")

        clips_dict = {}
        sorted_clips = {}

        for key, streamer in self.__streamers.items():
            user = self.__get_user(streamer)
            user_id = user[Constant.DATA_KEY][0][Constant.ID_KEY]
            if user_id:
                self.logger.debug(f'{streamer}...')
                clips = self.__get_clip(user_id)
                if clips:
                    for clip in clips.json()[Constant.DATA_KEY]:
                        clips_dict = self.__add_clip_to_dict(clip, streamer, clips_dict)

        self.logger.info("Data get success !")

        self.logger.info("Writing data on json file...")

        sorted_clips['total_clips'] = {"number": 48}
        
        sorted_clips = self.__get_dict_sorting_and_ranking(clips_dict)

        FileUtils.write_jsonfile_from_dict(Constant.REL_CLIPS_PATH, sorted_clips)

        self.logger.info("Successfully write !")

    def download_by_rank(self, rank):
        clips_dict = FileUtils.get_dict_from_jsonfile(Constant.REL_CLIPS_PATH)
        for key, value in clips_dict.items():
            if value[Constant.RANK_KEY] == rank:
                self.logger.info(f"Starting download clip {rank}...")
                # urllib.request.urlretrieve(value[Constant.CLIP_DOWNLOAD_URL_KEY], f'{Constant.REL_VIDEO_DIRECTORY_PATH}{Constant.VIDEO_NAME}')
                metadata = self.__set_metadata(value)
                FileUtils.write_jsonfile_from_dict(Constant.METADATA_PATH, metadata)
                self.logger.info("Successfully downloaded !")
                return
        raise ValueError('Rank not found')




