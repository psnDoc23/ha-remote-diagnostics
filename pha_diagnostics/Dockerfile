ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Install Python + build tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    libffi-dev \
    openssl-dev

# Create a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install FastAPI + Uvicorn inside the venv
# RUN pip install --no-cache-dir fastapi uvicorn
# per cop 20260117
RUN /venv/bin/pip install \
    fastapi \
    uvicorn \
    httpx


# Copy rootfs
COPY rootfs/ /

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
