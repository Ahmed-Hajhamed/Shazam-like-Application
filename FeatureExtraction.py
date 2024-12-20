import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
    
def extract_features(file_path):
    audio, sampling_rate = load_audio(file_path)
    segments = split_audio(audio, sampling_rate)
    features = []
    for segment in segments:
        spectrogram = compute_spectrogram(segment, sr= sampling_rate)
        mfccs = compute_mfcc(segment, sampling_rate)
        chroma = compute_chroma(segment, sampling_rate)
        zcr = compute_zcr(segment)
        rmse = compute_rmse(segment)
        segment_features = [spectrogram, mfccs, chroma, zcr, rmse]
        features.append(segment_features)
    # save_features(features, save_path)
    return features

def load_audio(file_path, target_sr=22050):
    audio, sr = librosa.load(file_path, sr=target_sr)
    return audio, sr


def split_audio(audio, sr, segment_duration=2):
    segment_length = sr * segment_duration
    return [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]


def compute_spectrogram(audio, sr, n_fft=2048, hop_length=512):
    stft = np.abs(librosa.stft(audio, n_fft=n_fft, hop_length=hop_length))
    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    return spectrogram


def compute_mfcc(audio, sr, n_mfcc=13):
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return mfccs


def compute_chroma(audio, sr, hop_length=512):
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr, hop_length=hop_length)
    return chroma


def compute_zcr(audio):
    zcr = librosa.feature.zero_crossing_rate(y=audio)
    return zcr


def compute_rmse(audio, hop_length=512):
    rmse = librosa.feature.rms(y=audio, hop_length=hop_length)
    return rmse


def normalize_features(features):
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(features.T).T
    return normalized_features


def save_features(features, file_path):
    np.save(file_path, features)

features = extract_features("C:\\Users\VICTUS\Downloads\y2mate.com - Eminem  Stan Short Version ft Dido (1) [vocals].wav")
