import requests
from configs.setting import config

audio_url = config.get("aigc", "audio_url")
threeD_url = config.get("aigc", "threeD_url")
video_sound_url = config.get("aigc", "video_sound_url")
host = config.get("aigc", "host")


def send_tts_request(content, vh_sex, mc_id):
    sound_type = "male" if vh_sex == 1 else "female"
    data = {
        "content": content,
        "sound_type": sound_type,
        "params": {"mc_id": mc_id},
        "method": "post",
        "host": host,
        "url": "/marketing_contents/market_minio_content"
    }
    print(audio_url, data)
    response = requests.post(audio_url, json=data)
    return response


def send_nerf_request(file_list, mo_id, file_type):
    data = {
        "file_list": file_list,
        "file_type": file_type,
        "params": {"mo_id": mo_id},
        "method": "post",
        "host": host,
        "url": "/meta_objs/meta_nerf_content"
    }
    print(threeD_url)
    requests.post(threeD_url, json=data)


def send_compose_request(video_uri, audio_uri, marketing_content_id):
    print("开始调度音视频合成")
    data = {
        "video_uri": video_uri,
        "audio_uri": audio_uri,
        "params": {"mc_id": marketing_content_id},
        "method": "post",
        "host": host,
        "url": "/marketing_contents/market_minio_content"
    }
    print(f"data: {data},video_sound_url: {video_sound_url}")
    requests.post(video_sound_url, json=data)


def send_tts_request_for_blueprint(content, vh_sex, mc_id):
    sound_type = "male" if vh_sex == 1 else "female"
    data = {
        "content": content,
        "sound_type": sound_type,
        "params": {"mc_id": mc_id},
        "method": "post",
        "host": host,
        "url": "/tts/tts_nfs_content"
    }
    print(audio_url, data)
    response = requests.post(audio_url, json=data)
    return response
