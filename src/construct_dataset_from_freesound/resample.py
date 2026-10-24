from scipy.signal import resample_poly

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def calc_factor(sample_rate, resample_rate):
    g = gcd(sample_rate, resample_rate)
    up, down = resample_rate // g, sample_rate // g
    return [up, down]

def resampler(waveform, sample_rate, resample_rate):
    g = gcd(sample_rate, resample_rate)
    up, down = resample_rate // g, sample_rate // g
    return resample_poly(waveform, up, down, axis=0)

def resample_example(example, audio="audio", resample_rate=16000):
    samples = example[audio].get_all_samples()
    waveform = samples.data.t().numpy()
    sample_rate = samples.sample_rate
    waveform = resampler(waveform, sample_rate, resample_rate)
    return {"waveform": waveform, "freesound_id": example["freesound_id"]}