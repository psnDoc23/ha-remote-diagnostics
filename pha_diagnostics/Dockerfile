ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:3.11
FROM ${BUILD_FROM}

# Copy rootfs into the container
COPY rootfs/ /

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
