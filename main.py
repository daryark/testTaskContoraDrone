import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys
matplotlib.use('TkAgg')
# import audioread
# import wave
# from mutagen.wave import WAVE
import struct

def visual_sig(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data[:5000])
    plt.title("Signal in Time Domain")
    plt.xlabel("Samples") 
    plt.ylabel("Amplitude")
    plt.grid()
    # plt.show(block=False)
    plt.savefig("signal_plot.png")
    print("Signal plot saved into 'signal_plot.png'")
    # plt.close()

def visual_frequency(data, sampling_rate):
    freq_data = np.fft.fft(data)
    frequencies = np.fft.fftfreq(len(freq_data), 1 / sampling_rate)
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies[:len(frequencies)//2], np.abs(freq_data[:len(freq_data)//2]))
    plt.title("Signal in Frequency Domain")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    # plt.show(block=False)
    plt.savefig("signal_freq_plot.png")
    print("Signal plot saved into 'signal_freq_plot.png'")
    # plt.close()

# def main():
#     if len(sys.argv) != 2:
#         print("add exactly one file to read from")
#         sys.exit(1)

#     file_path = sys.argv[1];
#     if not file_path.endswith('.wav'):
#         print("not valid file argument")
#         sys.exit(1)
    
#     with open(file_path, "rb") as f:
#         riff_header = f.read(12)  # First 12 bytes are RIFF header
#         print(f"RIFF Header: {riff_header}")

#         while True:
#             chunk_header = f.read(8)  # Each chunk has an 8-byte header
#             if len(chunk_header) < 8:
#                 break  # End of file
            
#             chunk_id, chunk_size = struct.unpack("<4sI", chunk_header)
#             chunk_data = f.read(chunk_size)  # Read the chunk content
            
#             print(f"Chunk ID: {chunk_id.decode()} | Size: {chunk_size}")

#             if chunk_id == b"auxi":
#                 print("📌 Extracting 'auxi' chunk data:")
#                 print(f"chunk_data: {chunk_data}")  # Print raw content

#             auxi_data = b'\xe8\x07\x0c\x00\x02\x00\x18\x00'  # First few bytes
#             print("AUXI DECODE" + auxi_data.decode(errors="ignore") + " END")  # Ignore non-text bytes
#             decoded_values = struct.unpack("<HHHH", auxi_data)  # Little-endian 4 unsigned shorts
#             print(f"decoded_values: {decoded_values}")

#     sampling_rate, data = wavfile.read(file_path)
#     print(f"Sampling Rate: {sampling_rate} Hz")
#     print(f"Data Shape: {data.shape}")
#     if data.ndim > 2:
#         print("Unexpected data shape. Ensure the file contains valid audio.")
#         sys.exit(1)
#     if len(data) == 0:
#         print("Audio file is empty or corrupted")
#         sys.exit(1)

#     try:
#         visual_sig(data)
#         visual_frequency(data, sampling_rate)

#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#     except ValueError as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"Unexpected error occured: {e}")

import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def visual_sig(data, file_path):
    """Plot signal waveform."""
    plt.figure(figsize=(30, 5))
    plt.plot(data[:4000])
    plt.title("Waveform")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.savefig(f"sig_time_{file_path.split('.')[0]}.png")

def visual_frequency(data, sampling_rate, file_path):
    """Plot frequency domain."""
    spectrum = np.fft.fft(data[:, 0])  # FFT on first channel
    freqs = np.fft.fftfreq(len(spectrum), 1/sampling_rate)

    plt.figure(figsize=(30, 5))
    plt.plot(freqs[:len(freqs)//2], np.abs(spectrum[:len(freqs)//2]))
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.savefig(f"sig_freq_{file_path.split('.')[0]}.png")

def decode_auxi(chunk_data):
    """Decode the 'auxi' chunk (if meaningful)."""
    if len(chunk_data) < 16:
        print("⚠️ auxi chunk too small to decode meaningfully.")
        return

    # Try interpreting first 8 bytes as 4 little-endian unsigned shorts
    decoded_values = struct.unpack("<HHHH", chunk_data[:8])
    print(f"🔍 Decoded 'auxi' values: {decoded_values}")

    # Extract possible string metadata
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
        riff_header = f.read(12)  # Read RIFF header
        print(f"🔷 RIFF Header: {riff_header}")

        while True:
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break  # End of file
            
            chunk_id, chunk_size = struct.unpack("<4sI", chunk_header)
            chunk_id = chunk_id.decode().strip()  # Decode chunk name
            print(f"🔹 Chunk ID: {chunk_id} | Size: {chunk_size}")

            chunk_data = f.read(chunk_size)

            if chunk_id == "auxi":
                print("📌 Extracting 'auxi' chunk data...")
                decode_auxi(chunk_data)  # Decode properly

    try:
        sampling_rate, data = wavfile.read(file_path)
        print(f"🎵 Sampling Rate: {sampling_rate} Hz")
        print(f"📊 Data Shape: {data.shape}")

        if data.ndim > 2 or len(data) == 0:
            print("⚠️ Unexpected or empty audio data.")
            sys.exit(1)

        visual_sig(data, file_path)
        visual_frequency(data, sampling_rate, file_path)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
