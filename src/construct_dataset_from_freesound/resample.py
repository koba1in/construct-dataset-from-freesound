from scipy.signal import resample_poly
import logging
import io
import soundfile as sf

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def calc_factor(sample_rate, resample_rate):
    g = gcd(sample_rate, resample_rate)
    up, down = resample_rate // g, sample_rate // g
    return [up, down]

def decode_audio(audio):
    if audio["bytes"] is not None:
        return sf.read(io.BytesIO(audio["bytes"]), dtype="float32")
    return sf.read(audio["path"], dtype="float32")

def resampler(waveform, sample_rate, resample_rate):
    g = gcd(sample_rate, resample_rate)
    up, down = resample_rate // g, sample_rate // g
    return resample_poly(waveform, up, down, axis=0)

def resample_example(example, audio_column, audio_id_column, resample_rate):
    waveform, sample_rate = decode_audio(example[audio_column])
    waveform = resampler(waveform, sample_rate, resample_rate)
    return {"waveform": waveform, audio_id_column: example[audio_id_column]}

def safe_resample_example(example, audio_column, audio_id_column, resample_rate):
    try:
        result = resample_example(example, audio_column, audio_id_column, resample_rate)
        result["_skip"] = False
        return result
    except Exception as e:
        logging.warning(
            f"Skipping audio: "
            f"id={example.get(audio_id_column)}, "
            f"title={example.get('title')}, "
            f"error={e}"
        )
        result = dict(example)
        result["_skip"] = True
        return result