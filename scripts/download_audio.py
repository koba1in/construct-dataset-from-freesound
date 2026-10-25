import sys
import os
from construct_dataset_from_freesound.resample import resample_example
from construct_dataset_from_freesound.info import get_license_class
from datasets import load_dataset
import soundfile as sf
from pathlib import Path


ACCESS_TOKEN = os.environ["HF_TOKEN"]
if not ACCESS_TOKEN:
    raise RuntimeError("環境変数 HF_TOKEN が設定されていません")

split = sys.argv[1]
download_path = Path(sys.argv[2])
licenses = sys.argv[3:]

download_path.mkdir(parents=True, exist_ok=True)

repo_id = "benjamin-paine/freesound-laion-640k"

license_kinds = get_license_class(repo_id, ACCESS_TOKEN)
licenses = [license_kinds[i] for i in licenses]

resample_rate = 16000
columns = ["waveform", "freesound_id"]


dataset = load_dataset(repo_id,
                  split=split,
                  streaming=True,
                  token=ACCESS_TOKEN
                  ).filter(lambda x: x["license"] in licenses
                           ).map(lambda x: resample_example(x, "audio", resample_rate)
                                ).select_columns(columns
                                                 )

for example in dataset:
        file_path = download_path / f"{example['freesound_id']}.flac"
        if file_path.exists():
            continue
        sf.write(file_path, example["waveform"], resample_rate, subtype="PCM_16", )
