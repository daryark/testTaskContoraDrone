import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys
matplotlib.use('TkAgg')
def visual_sig(data):
    # Step 2: Visualize the Signal in Time Domain
    plt.figure(figsize=(10, 5))
    plt.plot(data[:5000])
    plt.title("Signal in Time Domain")
    plt.xlabel("Samples") 
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

def visual_frequency(data):
    # Step 3: Visualize Frequency Domain
    freq_data = np.fft.fft(data)
    frequencies = np.fft.fftfreq(len(freq_data), 1 / sampling_rate)
    plt.figure(figsize=(10, 4))
    plt.plot(frequencies[:len(frequencies)//2], np.abs(freq_data[:len(freq_data)//2]))
    plt.title("Signal in Frequency Domain")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("add exactly one file to read from")
        sys.exit(1)

    file_path = sys.argv[1];
    if not file_path.endswith('.wav'):
        print("not valid file argument")
        sys.exit(1)

    sampling_rate, data = wavfile.read(file_path)
    print(f"Sampling Rate: {sampling_rate} Hz") #*number of samples per second
    print(f"Data Shape: {data.shape}") #*NumPy array containing the samples of the audio signal
    #*.shape - gives dimentions of the arr. ex: single dimention(n,), double dimention (n, 2) - where n is the number of samples, and the second dimension corresponds to the left and right audio channels.
    if data.ndim > 2:
        print("Unexpected data shape. Ensure the file contains valid audio.")
        sys.exit(1)
    if len(data) == 0:
        print("Audio file is empty or corrupted")
        sys.exit(1)

    try:
        visual_sig(data)
        visual_frequency(data)
        plt.savefig("signal_plot.png")
        print("Signal plot saved into 'signal_plot.png'")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error occured: {e}")

if __name__ == "__main__":
    main()
