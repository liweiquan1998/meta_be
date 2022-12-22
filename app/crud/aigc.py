import threading
import time
from typing import List

import requests

from app import models, schemas
from sqlalchemy.orm import Session
from app.crud.basic import update_to_db
from app.common.validation import *

audio_url = os.getenv("aigc_audio_url", 'http://192.168.199.27:7090/aigc/tts')
threeD_url = os.getenv("aigc_threeD_url", 'http://192.168.199.249:11100/aigc/3d_reconstruction')
video_sound_url = os.getenv("aigc_video_sound_url", 'http://192.168.199.249:11100/aigc/video_with_sound')


def send_tts_request(content, vh_sex,  mc_id, db: Session):
    sound_type = "male" if vh_sex == 1 else "female"
    data = {
        "content": content,
        "sound_type": sound_type,
        "mc_id": mc_id
    }
    print(audio_url, data)
    requests.post(audio_url, json=data)


def send_nerf_request(file_list, mo_id, file_type):
    data = {
        "file_list": file_list,
        "file_type": file_type,
        "id": mo_id
    }
    requests.post(threeD_url, json=data)


def send_compose_request(video_uri, audio_uri, marketing_content_id):
    data = {
        "video_uri": video_uri,
        "audio_uri": audio_uri,
        "marketing_content_id": marketing_content_id
    }
    requests.post(video_sound_url, json=data)
