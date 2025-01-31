
import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import matplotlib
matplotlib.use('TkAgg')

def visual_sig(data, file_path):
    """Plot signal waveform."""
    plt.figure(figsize=(20, 5))
    plt.plot(data[:3000])
    plt.title("Waveform")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.savefig(f"sig_time_{file_path.split('.')[0]}.png")

def visual_frequency(data, sampling_rate, file_path):
    """Plot frequency domain."""
    downsample_factor = 2
    data_downsampled = data[::downsample_factor, 0]
    spectrum = np.fft.fft(data_downsampled)
    freqs = np.fft.fftfreq(len(data_downsampled), d=1/sampling_rate)
    plt.figure(figsize=(20, 5))
    plt.plot(freqs[:len(freqs)//2], np.abs(spectrum[:len(spectrum)//2]))
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.savefig(f"sig_freq_{file_path.split('.')[0]}.png")
    return freqs

def detect_video(freqs):
    video_freq_range = (1e6, 100e6)
    video_signal_present = np.any((freqs >= video_freq_range[0]) & (freqs <= video_freq_range[1]))
    if video_signal_present:
        print("Possible video signal detected!")
    else:
        print("No video signal detected.")

def decode_auxi(chunk_data):
    """Decode the 'auxi' chunk (if meaningful)."""
    if len(chunk_data) < 16:
        print("⚠️ auxi chunk too small to decode meaningfully.")
        return
    decoded_values = struct.unpack("<HHHH", chunk_data[:8])
    print(f"🔍 Decoded 'auxi' values: {decoded_values}")
    text_data = chunk_data[8:].decode(errors="ignore").strip("\x00")
    print(f"📜 Possible auxi metadata: {text_data}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <file.wav>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not file_path.endswith('.wav'):
        print("Error: Not a valid WAV file.")
        sys.exit(1)

    with open(file_path, "rb") as f:
        riff_header = f.read(12)
        print(f"🔷 RIFF Header: {riff_header}")

        while True:
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break
            
            chunk_id, chunk_size = struct.unpack("<4sI", chunk_header) #< - little-endian, 4s - 4 byte str, I - unsigned int
            chunk_id = chunk_id.decode().strip()
            print(f"🔹 Chunk ID: {chunk_id} | Size: {chunk_size}")

            chunk_data = f.read(chunk_size)

            if chunk_id == "auxi":
                print("📌 Extracting 'auxi' chunk data...")
                decode_auxi(chunk_data)

    try:
        sampling_rate, data = wavfile.read(file_path)
        print(f"🎵 Sampling Rate: {sampling_rate} Hz")
        print(f"📊 Data Shape: {data.shape}")

        if data.ndim > 2 or len(data) == 0:
            print("⚠️ Unexpected or empty audio data.")
            sys.exit(1)

        visual_sig(data, file_path)
        freqs = visual_frequency(data, sampling_rate, file_path)
        detect_video(freqs)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

