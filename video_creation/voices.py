#!/usr/bin/env python3
import os

from rich.console import Console

from TTS.engine_wrapper import TTSEngine
from TTS.GTTS import GTTS
from TTS.streamlabs_polly import StreamlabsPolly
from TTS.aws_polly import AWSPolly
from TTS.TikTok import TikTok

from utils.console import print_table, print_step


console = Console()

TTSProviders = {
    "GoogleTranslate": GTTS,
    "AWSPolly": AWSPolly,
    "StreamlabsPolly": StreamlabsPolly,
    "TikTok": TikTok,
}

VIDEO_LENGTH: int = 40  # secs


def save_text_to_mp3(reddit_obj):
    """Saves Text to MP3 files.
    Args:
        reddit_obj : The reddit object you received from the reddit API in the askreddit.py file.
    """
    env = os.getenv("TTS_PROVIDER", "")
    if env in TTSProviders:
        text_to_mp3 = TTSEngine(get_case_insensitive_key_value(TTSProviders, env), reddit_obj)
    else:
        chosen = False
        choice = ""
        while not chosen:
            print_step("Please choose one of the following TTS providers: ")
            print_table(TTSProviders)
            choice = input("\n")
            if choice.casefold() not in map(lambda _: _.casefold(), TTSProviders):
                print("Unknown Choice")
            else:
                chosen = True
        text_to_mp3 = TTSEngine(
            get_case_insensitive_key_value(TTSProviders, choice), reddit_obj
        )

    return text_to_mp3.run()


def get_case_insensitive_key_value(input_dict, key):
    return next(
        (
            value
            for dict_key, value in input_dict.items()
            if dict_key.lower() == key.lower()
        ),
        None,
    )
