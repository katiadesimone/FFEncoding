#immagine di base
FROM alpine:latest
#installazione dipendenze
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
#installazione prometheus_client per invio delle metriche
RUN pip install prometheus_client
#installazione ffmpeg
RUN apk add ffmpeg
#FROM alpine:latest
#USER root
#configurazione della working directory
COPY app /app
COPY Jellyfish_1080_10s_1MB.webm /app
COPY FFencoding-video_v4.py /app
COPY encoded app/
WORKDIR app/
# Eseguiamo lo script
CMD ["python3", "FFencoding-video_v4.py"]
