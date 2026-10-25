from construct_dataset_from_freesound.resample import safe_resample_example
from datasets import load_dataset
import soundfile as sf

def download(repo_id, split, license_column, licenses, audio_column, audio_id_column, resample_rate, download_path, ACCESS_TOKEN):

    columns = ["waveform", audio_id_column]

    dataset = load_dataset(repo_id,
                    split=split,
                    streaming=True,
                    token=ACCESS_TOKEN
                    ).filter(lambda x: x[license_column] in licenses
                            ).map(lambda x: safe_resample_example(x, audio_column, audio_id_column, resample_rate)
                                    ).filter(lambda x: not x["_skip"]
                                            ).remove_columns(["_skip"]
                                                            ).select_columns(columns)

    for example in dataset:
            file_path = download_path / f"{example[audio_id_column]}.flac"
            if file_path.exists():
                continue
            sf.write(file_path, example["waveform"], resample_rate, subtype="PCM_16", )
