# syntax=docker/dockerfile:1

# ---- Stage 1: build the Tailwind CSS bundle ----
FROM node:20-bookworm-slim AS css-builder
WORKDIR /app
COPY package.json ./
RUN npm install
# Tailwind scans templates / views.py / forms.py (see tailwind.config.js content globs)
COPY tailwind.config.js ./
COPY static/src ./static/src
COPY templates ./templates
COPY . .
RUN npm run build:css:prod

# ---- Stage 2: Python runtime ----
FROM python:3.14-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Python deps (psycopg[binary] and pillow ship self-contained wheels — no apt build deps needed)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application source
COPY . .
# Overwrite the committed CSS with the freshly minified build
COPY --from=css-builder /app/static/css/output.css ./static/css/output.css

# Collect static into STATIC_ROOT (served by WhiteNoise). Dummy DB vars just let
# settings import — collectstatic never touches the database.
RUN DB_NAME=build DB_USER=build DB_PASSWORD=build DB_HOST=localhost \
    python manage.py collectstatic --noinput

# Run as an unprivileged user
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /app/media \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "growthmaster.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
