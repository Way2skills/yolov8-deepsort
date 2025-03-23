from moviepy.editor import VideoFileClip

# Load the video
video = VideoFileClip("sample.mp4")

# Trim from 10 to 30 seconds
trimmed_video = video.subclip(40, 50)

# Save the trimmed video
trimmed_video.write_videofile("output.mp4", codec="libx264", fps=24)
