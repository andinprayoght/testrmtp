# Base image Python + ffmpeg
FROM python:3.11-slim

# Install dependencies sistem
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Install Streamlink
RUN pip install --no-cache-dir streamlink>=6.2.0

# Set working directory
WORKDIR /app

# Copy script Python
COPY stream_rtmp_env.py /app/stream_rtmp_env.py

# Set default environment variables
ENV INPUT_URL="https://liveplus.rctiplus.id/RTMP-IN.m3u8" \
    RTMP_URL="rtmps://dc5-1.rtmp.t.me/s/2449204820:4J6tl1qDyBBzpxVn4iYAMQ" \
    WATERMARK_TEXT="TipiStream" \
    REFERER="https://www.rctiplus.com" \
    USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
    ORIGIN=""

# Default command
CMD ["python", "stream_rtmp_env.py"]
