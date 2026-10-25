import argparse
from dotenv import load_dotenv
import os
from pathlib import Path
from construct_dataset_from_freesound.download import download
from construct_dataset_from_freesound.metadata import get_license_class

def main():
    load_dotenv()
    ACCESS_TOKEN = os.environ["HF_TOKEN"]
    if not ACCESS_TOKEN:
        raise RuntimeError("環境変数 HF_TOKEN が設定されていません")

    parser = argparse.ArgumentParser(
        prog="freesound-downloader",
    )

    parser.add_argument("-s", "--split", nargs="+", required=True, help="choose split")
    parser.add_argument("-p", "--path", required=True, help="download directory")
    parser.add_argument("-l", "--license", nargs="+", required=True, help="choose license")
    args = parser.parse_args()

    splits = args.split
    path = Path(args.path)
    licenses = args.license

    repo_id = "benjamin-paine/freesound-laion-640k"
    license_column = "license"
    license_kinds = get_license_class(repo_id, license_column, ACCESS_TOKEN)
    for key in licenses:
        license_keys = [*license_kinds.keys()]
        if not (key in license_keys):
            print(f"choose license from {license_keys}")
            exit()
    licenses = [license_kinds[i] for i in licenses]


    audio_column = "audio"
    audio_id_column = "freesound_id"
    resample_rate = 16000

    for split in splits:
        download_path = path / split
        download_path.mkdir(parents=True, exist_ok=True)
        download(repo_id, split, license_column, licenses, audio_column, audio_id_column, resample_rate, download_path, ACCESS_TOKEN)