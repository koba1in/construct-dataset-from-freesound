import sys
import os
from pathlib import Path
from construct_dataset_from_freesound.download import download
from construct_dataset_from_freesound.metadata import get_license_class

def main():
    ACCESS_TOKEN = os.environ["HF_TOKEN"]
    if not ACCESS_TOKEN:
        raise RuntimeError("環境変数 HF_TOKEN が設定されていません")

    split = sys.argv[1]
    download_path = Path(sys.argv[2])
    licenses = sys.argv[3:]


    repo_id = "benjamin-paine/freesound-laion-640k"
    license_column = "license"
    license_kinds = get_license_class(repo_id, license_column, ACCESS_TOKEN)
    licenses = [license_kinds[i] for i in licenses]


    audio_column = "audio"
    audio_id_column = "freesound_id"
    resample_rate = 16000
    download_path.mkdir(parents=True, exist_ok=True)
    download(repo_id, split, licenses, audio_column, audio_id_column, resample_rate, download_path, ACCESS_TOKEN)