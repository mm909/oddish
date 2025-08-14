import os
import yt_dlp
import whisper
import numpy as np
import pandas as pd
from resemblyzer import VoiceEncoder, preprocess_wav
from sklearn.cluster import AgglomerativeClustering
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from pytube import YouTube
from pydub import AudioSegment

# Load models once
encoder = VoiceEncoder()
whisper_model = whisper.load_model("base")  # Or use faster-whisper if preferred

def download_audio_with_ytdlp(url):
    """Downloads YouTube audio and returns a wav file path."""
    folder = "audio"
    os.makedirs(folder, exist_ok=True)
    url_name = url.split("v=")[-1].split("&")[0]
    temp_file = f'{folder}/{url_name}.mp3'
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]/bestaudio/best',
        'outtmpl': temp_file,
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt',  # Optional: use cookies for age-restricted content

    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error downloading audio: {e}")
        raise

    try:
        # Verify MP3 file integrity using ffmpeg
        ffmpeg_check_cmd = f'ffmpeg -v error -i "{temp_file}" -f null -'
        result = os.system(ffmpeg_check_cmd)
        if result != 0:
            raise ValueError("MP3 file is corrupted or unsupported.")

        # Convert to wav
        audio = AudioSegment.from_file(temp_file)
        wav_path = temp_file.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")
        os.remove(temp_file)
        raise

    os.remove(temp_file)
    return wav_path

def download_audio_fallback(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    temp_file = NamedTemporaryFile(delete=False, suffix=".mp4")
    audio_stream.download(filename=temp_file.name)

    # Convert to .wav
    audio = AudioSegment.from_file(temp_file.name)
    wav_path = temp_file.name.replace(".mp4", ".wav")
    audio.export(wav_path, format="wav")
    os.remove(temp_file.name)
    return wav_path

def segment_and_embed(wav_path, url):
    """Returns list of (embedding, start, end, video_url) for each segment and saves speaker audio samples."""
    audio = preprocess_wav(wav_path)
    segments = whisper_model.transcribe(wav_path, language="en", verbose=False)["segments"]
    
    data = []
    speaker_sample_folder = "speaker_samples"
    os.makedirs(speaker_sample_folder, exist_ok=True)

    for seg in segments:
        start, end = seg["start"], seg["end"]
        if end - start < 1.0:  # Skip very short segments
            continue
        wav_chunk = audio[int(start * 16000):int(end * 16000)]
        embed = encoder.embed_utterance(wav_chunk)
        data.append((embed, start, end, url))

        # Save audio sample for the segment
        sample_path = os.path.join(speaker_sample_folder, f"{url.split('v=')[-1]}_{start:.2f}_{end:.2f}.wav")
        AudioSegment(
            wav_chunk.tobytes(),
            frame_rate=16000,
            sample_width=wav_chunk.dtype.itemsize,
            channels=1
        ).export(sample_path, format="wav")
    
    return data

def cluster_speakers(all_embeddings, num_speakers=4):
    """Cluster across all videos, returns cluster IDs."""
    X = np.array([e[0] for e in all_embeddings])
    clustering = AgglomerativeClustering(n_clusters=num_speakers)
    labels = clustering.fit_predict(X)
    return labels

def build_df(urls, num_speakers=4):
    all_embeddings = []
    for url in urls:
        print(f"Processing {url}")

        try:
            wav_path = download_audio_with_ytdlp(url)
        except Exception:
            wav_path = download_audio_fallback(url)

        segments = segment_and_embed(wav_path, url)
        all_embeddings.extend(segments)
        os.remove(wav_path)

    labels = cluster_speakers(all_embeddings, num_speakers=num_speakers)
    
    df_data = {}
    for (embed, start, end, url), speaker_id in zip(all_embeddings, labels):
        duration = end - start
        speaker = f"Speaker_{speaker_id}"
        if url not in df_data:
            df_data[url] = {}
        df_data[url][speaker] = df_data[url].get(speaker, 0) + duration

    # Normalize to percentages
    final_rows = []
    for url, speaker_durations in df_data.items():
        total = sum(speaker_durations.values())
        row = {spk: round(100 * dur / total, 2) for spk, dur in speaker_durations.items()}
        row["url"] = url
        final_rows.append(row)

    df = pd.DataFrame(final_rows).fillna(0).set_index("url")
    return df

# --- Example Usage ---
if __name__ == "__main__":
    video_urls = [
        "https://www.youtube.com/watch?v=ioDpjYANuE0",
        "https://www.youtube.com/watch?v=j4K_hn9LJ5M",
    ]
    df = build_df(video_urls, num_speakers=4)
    print(df)
    df.to_csv("speaker_distribution.csv")
