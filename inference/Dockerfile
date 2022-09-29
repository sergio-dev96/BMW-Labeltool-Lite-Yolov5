FROM tiangolo/uvicorn-gunicorn:python3.8 AS uvicorn-builder
FROM openvino/ubuntu20_runtime:latest

USER root

# Copy scripts form uvicorn-builder (this is the only purpose of the uvicorn-builder build stage)
COPY --from=uvicorn-builder /start.sh /start.sh
COPY --from=uvicorn-builder /start-reload.sh /start-reload.sh

ENV DEBIAN_FRONTEND noninteractive
WORKDIR /build

RUN python3 -m pip install --no-cache-dir --upgrade pip
COPY ./code/requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -U -r requirements.txt

# Configure webserver settings
ENV HOST 0.0.0.0
ENV PORT 80
ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 1
ENV LOG_LEVEL debug

EXPOSE 80

COPY ./code /app
COPY ./yolov5-master /app

WORKDIR /app

# Setup OpenVINO environment vars before starting
CMD ["/bin/bash", "-c", "source /opt/intel/openvino/setupvars.sh && /start.sh"]
