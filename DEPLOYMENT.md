# Deployment Guide

This guide covers deployment options for the Brain Mapping EEG Classification System.

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python signal_generator.py
python app.py
```

## Docker Deployment

### Single Container
```bash
docker build -t brain-mapping-eeg .
docker run -p 9999:9999 brain-mapping-eeg
```

### Docker Compose
```bash
docker-compose up -d
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:9999 app:app
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment Variables

- `FLASK_ENV`: production
- `FLASK_DEBUG`: false
- `CLASSIFICATION_THRESHOLD`: 600

## Monitoring

Use the monitoring utilities:
```bash
python scripts/monitor.py
```

## Backup

Backup the data directory:
```bash
tar -czf backup.tar.gz data/
```
