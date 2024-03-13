import moviepy.editor as mp
import speech_recognition as sr

# Function to convert seconds to SRT format (00:00:00,000)
def convert_to_srt_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

# Convert video to audio
clip = mp.VideoFileClip("test.mp4")
clip.audio.write_audiofile("theaudio.wav")

# Initialize recognizer
r = sr.Recognizer()

# Load the audio file
audio = 'theaudio.wav'

# Use try-except block for error handling
try:
    # Use SpeechRecognizer to transcribe the audio
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)

    # Attempt to transcribe the audio using Google's speech recognition
    text = r.recognize_google(audio_data)

    # Split text into chunks of appropriate length for subtitles
    chunk_size = 4  # seconds
    words = text.split()
    num_words = len(words)
    chunks = [words[i:i+num_words//chunk_size] for i in range(0, num_words, num_words//chunk_size)]

    # Generate SRT format subtitles
    subtitles = ""
    start_time = 0
    for i, chunk in enumerate(chunks):
        end_time = start_time + chunk_size
        subtitle_text = ' '.join(chunk)
        subtitle = f"{i+1}\n{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n{subtitle_text}\n\n"
        subtitles += subtitle
        start_time = end_time

    # Write subtitles to a file
    with open("output.srt", "w") as f:
        f.write(subtitles)

    print("SRT subtitles generated successfully.")

except sr.UnknownValueError:
    # Speech recognition could not understand audio
    print("Speech recognition could not understand audio.")

except sr.RequestError as e:
    # Could not request results from the speech recognition service
    print(f"Could not request results from the speech recognition service: {e}")

except Exception as e:
    # Other exceptions
    print(f"An error occurred: {e}")

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

# Load the video clip
video_clip = VideoFileClip("test.mp4")

# Load the subtitles from the SRT file
generator = lambda txt: TextClip(txt, fontsize=24, color='white', bg_color='black')
subtitles = SubtitlesClip("output.srt", generator)

# Set the position of subtitles
subtitles = subtitles.set_position(('center', 'bottom'))

# Overlay the subtitles onto the video clip
final_clip = CompositeVideoClip([video_clip, subtitles])

# Write the final video with subtitles inserted
final_clip.write_videofile("output_with_subtitles.mp4", codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)

print("Video with subtitles generated successfully.")
