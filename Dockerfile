# Crypto Momentum Lab dashboard. Built by Portainer from the deploy branch of the fork;
# runtime state (parquet candle cache) lives in the momentum-cache volume, see deploy/docker-compose.yml.
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 HOME=/tmp
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --uid 1000 --no-create-home app && mkdir -p data_cache && chown app:app data_cache
USER app
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s   CMD python -c "import urllib.request; urllib.request.urlopen(\"http://127.0.0.1:8501/_stcore/health\")" || exit 1
CMD ["python", "-m", "streamlit", "run", "app.py",      "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true",      "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
