from rtlsdr import RtlSdr

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 99.5e6  # Hz
sdr.freq_correction = 0  # PPM
sdr.gain = "auto"

a = sdr.read_samples(512)
print(a)
