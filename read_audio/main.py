import torchaudio
import torchaudio.transforms as transforms
import matplotlib.pyplot as plt

waveform, sample_rate = torchaudio.load("8ad0ff35595c30d76741ca181b83dc826ebabe346fb8f1799cd0d6f0830eb709.wav")

mfcc_transform = transforms.MFCC(
    sample_rate=sample_rate,
    n_mfcc=13, 
)

mfcc = mfcc_transform(waveform)

plt.figure(figsize=(10, 4))
plt.imshow(mfcc[0].detach().numpy(), cmap='viridis', origin='lower', aspect='auto')
plt.xlabel('Time')
plt.ylabel('MFCC Coefficients')
plt.title('MFCC Spectrogram')
plt.colorbar(label='Intensity')
plt.tight_layout()
plt.show()
