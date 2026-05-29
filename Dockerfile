#syntax=docker/dockerfile:1
FROM python:3.12-alpine AS builder
WORKDIR /build
COPY requirements.txt .
RUN --mount=type=ssh pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-alpine
LABEL org.opencontainers.image.authors="Kamil Rodak"

ARG DEFAULT_TZ=Europe/Warsaw

# brak plików .pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
# brak buforowania wyjścia - natychmiastowe logi
    PYTHONUNBUFFERED=1 \
    TZ=${DEFAULT_TZ}

WORKDIR /app

# kopiowanie bibliotek z etapu budowania, aplikacji i szablonu
COPY --from=builder /install /usr/local
COPY --chown=uzytkownik:uzytkownik zadanie1.py .
COPY --chown=uzytkownik:uzytkownik templates/ ./templates/
    
RUN apk add --no-cache curl && \
# dodanie użytkownika i nadanie mu praw do katalogu aplikacji
    adduser -D uzytkownik && \
    rm -rf /var/lib/apt/lists/*

USER uzytkownik

EXPOSE 2137

# healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:2137/ || exit 1

ENTRYPOINT ["python", "zadanie1.py"]
