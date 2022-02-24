class Constant:

    # GENERAL CONSTANTS
    VIDEO_DIRECTORY = "videos"

    # CLIP CONSTANTS
    REL_VIDEO_DIRECTORY_PATH = f"../{VIDEO_DIRECTORY}/"
    REL_CLIPS_PATH = "../data/clips.json"
    REL_CONF_PATH = "../data/conf.json"
    REL_STREAMERS_PATH = "../data/streamers.json"

    # DOWNLOADED CONTENT CONSTANTS
    VIDEO_NAME = "clips.mp4"
    THUMB_NAME = "thumb.jpg"
    METADATA_NAME = "metadata.json"

    # CLIPS JSON KEY CONSTANTS
    RANK_KEY = "rank"
    NAME_KEY = "name"
    TITLE_KEY = "title"
    CREATED_AT_KEY = "created_at"
    DURATION_KEY = "duration"
    VIEW_COUNT_KEY = "view_count"
    CLIP_URL_KEY = "url"
    THUMB_URL_KEY = "thumbnail_url"
    CLIP_DOWNLOAD_URL_KEY = "clip_download_url"

    # USER REQUEST KEY CONSTANTS
    DATA_KEY = 'data'
    ID_KEY = "id"

    # VIDEO CONSTANTS
    VIDEO_PATH = f"{VIDEO_DIRECTORY}/{VIDEO_NAME}"
    THUMNBNAIL_PATH = f"../{VIDEO_DIRECTORY}/{THUMB_NAME}"
    METADATA_PATH = f"../{VIDEO_DIRECTORY}/{METADATA_NAME}"

    # VIDEO METADATA
    DESCRIPTION_KEY = "description"
    TAGS_KEY = 'tags'
    TAGS = "#Twitch #TwitchFR #Clips #Clip #Streaming #Gaming #BestOfTwitch #BestOf #Drama"
    MAIN_DESCRIPTION = "Bonjour et bienvenue sur Best Of Twitch FR, cette chaine reposte les meilleurs clips journaliers." \
                            u'\ue007' \
                                "Cette chaîne n'a pas pour but de déranger les streamers mais simplement de pourvoir consulter les meilleurs clips de la journée sur youtube." \
                                    u'\ue007' \
                                        "Néamoins, si le streamer concerné par ce clip souhaite que la vidéo soit supprimée, il peut me contacter à l'adresse suivant :" \
                                        u'\ue007' \
                                            "twitchclips.acl@gmail.com" \
                                                u'\ue007' \
                                                    "La video sera supprimée dans les plus brefs délais."

    # Query urls
    USER_URL = 'https://api.twitch.tv/helix/users?login='
    CLIP_URL = 'https://api.twitch.tv/helix/clips?broadcaster_id='


    

