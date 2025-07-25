FROM python:3.12-slim-bookworm AS installer

WORKDIR /usr/src/app

COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY LICENSE LICENSE
COPY NOTICE NOTICE
COPY src src

# Generate python dependencies wheels
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git mailcap && \
    groupadd -g 1000 app && \
    useradd -mr -d /home/app -s /bin/bash -u 1000 -g 1000 app && \
    rm -rf /var/lib/apt/lists/*

COPY --from=installer /wheels /wheels

RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

USER app

WORKDIR /home/app

CMD ["eoap-tools"]
