import cv2
import subprocess

# YouTube RTMP server and stream key
youtube_rtmp_url = 'rtmp://a.rtmp.youtube.com/live2'
stream_key = '6g45-11ku-ha6k-41qy-16j3'  # Replace with your YouTube stream key

# Full RTMP URL
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/6g45-11ku-ha6k-41qy-16j3"

# Set up webcam (index 0 is typically the default webcam)
cap = cv2.VideoCapture(0)

# Set webcam resolution (1080p)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# FFmpeg command for streaming to YouTube
ffmpeg_cmd = [
    'ffmpeg',
    '-y',  # Overwrite output files without asking
    '-f', 'rawvideo',  # Input format
    '-vcodec', 'rawvideo',  # Raw video input
    '-pix_fmt', 'bgr24',  # Pixel format from OpenCV (BGR24)
    '-s', '1920x1080',  # Frame size (1080p)
    '-r', '30',  # Frame rate
    '-i', '-',  # Read from stdin
    '-c:v', 'libx264',  # Video codec
    '-b:v', '4500k',  # Bitrate
    '-preset', 'veryfast',  # Preset for lower latency
    '-f', 'flv',  # Output format for streaming
    '-flvflags', 'no_duration_filesize',  # Skip writing duration and filesize
    rtmp_url  # RTMP URL for YouTube
]

# Start FFmpeg process
ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

try:
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image from webcam. Exiting...")
            break

        # Write the frame to FFmpeg's stdin
        ffmpeg_process.stdin.write(frame.tobytes())

except KeyboardInterrupt:
    print("Stream stopped manually.")

finally:
    # Release resources
    cap.release()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
    print("Streaming ended and resources released.")
