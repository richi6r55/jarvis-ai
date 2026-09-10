# JARVIS AI - Complete Deployment Guide

## Production Deployment

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker installed
- Docker Compose installed
- API keys ready

#### Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

#### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Systemd Service (Linux)

#### Create Service File
```bash
sudo nano /etc/systemd/system/jarvis-ai.service
```

Paste:
```ini
[Unit]
Description=JARVIS AI Assistant
After=network.target

[Service]
Type=simple
User=jarvis
WorkingDirectory=/home/jarvis/jarvis-ai
ExecStart=/home/jarvis/jarvis-ai/venv/bin/python backend/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Enable and Start
```bash
sudo systemctl enable jarvis-ai
sudo systemctl start jarvis-ai
sudo systemctl status jarvis-ai
```

### Option 3: Cloud Deployment (Heroku/Railway/Replit)

#### For Heroku
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create jarvis-ai

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set GROQ_API_KEY=your_key

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## Environment Setup

### Production .env
```env
APP_ENV=production
APP_DEBUG=false

GEMINI_API_KEY=your_production_key
GROQ_API_KEY=your_production_key

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE=+1234567890

HOME_ASSISTANT_URL=http://your-ha-instance:8123
HOME_ASSISTANT_TOKEN=your_token
```

### Security Considerations
- Use environment variables for all secrets
- Never commit .env to version control
- Use HTTPS in production
- Implement rate limiting
- Add authentication/authorization
- Use firewall rules
- Regular security audits

## Database Setup (Optional)

### PostgreSQL (for chat history)
```sql
CREATE DATABASE jarvis_ai;

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    message_text TEXT,
    response TEXT,
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_id ON conversations(user_id);
CREATE INDEX idx_created_at ON conversations(created_at);
```

## Monitoring & Logging

### Application Logs
```bash
# View logs
journalctl -u jarvis-ai -f

# Or with Docker
docker-compose logs -f backend
```

### Health Monitoring
```bash
# Set up monitoring
while true; do
  curl http://localhost:8000/health
  sleep 60
done
```

### Error Tracking (Optional)
```bash
# Install Sentry
pip install sentry-sdk
```

Add to backend/main.py:
```python
import sentry_sdk
sentry_sdk.init(
    dsn="your_sentry_dsn",
    traces_sample_rate=1.0
)
```

## Scaling

### Horizontal Scaling
- Run multiple backend instances
- Use load balancer (nginx, HAProxy)
- Implement request queuing
- Cache responses where possible

### Performance Optimization
- Enable caching for frequent queries
- Use CDN for frontend assets
- Implement lazy loading
- Database indexing
- Query optimization

## Backup & Disaster Recovery

### Backup Strategy
```bash
# Backup database
pg_dump jarvis_ai > backup.sql

# Backup environment
cp .env .env.backup

# Backup code
git push origin main
```

### Recovery Procedures
```bash
# Restore from backup
psql jarvis_ai < backup.sql

# Rollback to previous version
git rollback <commit_hash>
```

## Troubleshooting

### High Memory Usage
```bash
# Check memory
docker stats

# Restart service
docker-compose restart backend
```

### API Rate Limits
- Groq: 30 req/min
- Gemini: 60 req/min, 1500/day
- Implement request queuing
- Use caching

### Database Connection Issues
```bash
# Test connection
psql -U user -d jarvis_ai -c "SELECT 1"

# Check connection pool
pg_stat_activity
```

## Maintenance

### Regular Tasks
- Daily: Check logs, monitor health
- Weekly: Database maintenance, backups
- Monthly: Security updates, dependency updates
- Quarterly: Performance review, optimization

### Update Procedure
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart jarvis-ai

# Verify
sudo systemctl status jarvis-ai
```

## Support & Resources

- GitHub Issues: https://github.com/richi6r55/jarvis-ai/issues
- Documentation: `/docs` (API docs)
- Health Check: `/health` (system status)
- Models Info: `/models` (available LLMs)
