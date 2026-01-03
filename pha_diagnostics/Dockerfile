FROM python:3.11-slim

# Create the directory where our script will live
RUN mkdir -p /usr/local/bin

# Copy the run script into the container
COPY run.sh /run.sh
RUN chmod +x /run.sh

# Copy the placeholder server file
COPY rootfs/usr/local/bin/server.py /usr/local/bin/server.py

CMD ["/run.sh"]
