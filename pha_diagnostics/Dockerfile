ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Install Python 3
RUN apk add --no-cache python3 py3-pip

# Copy rootfs into the container
COPY rootfs/ /

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
