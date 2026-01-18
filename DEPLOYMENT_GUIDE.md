# Deployment Guide
## How to Deploy Your Streamlit Application

This guide covers deploying your Data Center Topology Planner application to various platforms.

---

## Quick Decision Matrix

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Streamlit Cloud** | ✅ Yes | ⭐⭐⭐⭐⭐ | Quick deployment, public repos |
| **Render** | ✅ Yes | ⭐⭐⭐⭐ | Free tier, private repos |
| **Railway** | ⚠️ Limited | ⭐⭐⭐⭐ | Modern platform, good DX |
| **Heroku** | ❌ No | ⭐⭐⭐ | Established, reliable |
| **Self-Hosted** | ✅ (VPS cost) | ⭐⭐ | Full control |

---

## Option 1: Streamlit Community Cloud (Recommended)

### Why This is Best
- ✅ **Free** forever
- ✅ **Built specifically for Streamlit**
- ✅ **Zero configuration** needed
- ✅ **Auto-deploys** from GitHub
- ✅ **HTTPS included**

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Step-by-Step Deployment

#### Step 1: Push Code to GitHub

If you haven't already:

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - DCN Topology Planner"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/dc_topology_planner.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Select**:
   - Repository: `YOUR_USERNAME/dc_topology_planner`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click** "Deploy"

**That's it!** Your app will be live in ~2 minutes at:
`https://YOUR_APP_NAME.streamlit.app`

### Configuration

Create `.streamlit/config.toml` (optional):

```toml
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

### Updating Your App

Just push to GitHub:
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud automatically redeploys!

---

## Option 2: Render

### Why Render
- ✅ Free tier available
- ✅ Supports private repos
- ✅ Easy setup
- ✅ Automatic HTTPS

### Step-by-Step Deployment

#### Step 1: Create `render.yaml`

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: dc-topology-planner
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PORT
        value: 8501
```

#### Step 2: Deploy

1. **Go to**: https://render.com
2. **Sign up** (free)
3. **Click** "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure**:
   - Name: `dc-topology-planner`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. **Click** "Create Web Service"

### Important Notes for Render

- Set `server.address = 0.0.0.0` in Streamlit config
- Use `$PORT` environment variable
- Free tier has slower cold starts

---

## Option 3: Railway

### Why Railway
- ✅ Modern platform
- ✅ Great developer experience
- ✅ Supports Python
- ⚠️ Free credits, then paid

### Step-by-Step Deployment

#### Step 1: Create `Procfile`

Create `Procfile` (no extension) in project root:

```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

#### Step 2: Create `runtime.txt`

Create `runtime.txt`:

```
python-3.11.0
```

#### Step 3: Deploy

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click** "New Project"
4. **Select** "Deploy from GitHub repo"
5. **Choose** your repository
6. Railway auto-detects Python and deploys!

### Configuration

Railway automatically:
- Detects Python projects
- Installs from `requirements.txt`
- Runs the `Procfile` command

---

## Option 4: Heroku

### Why Heroku
- ✅ Established platform
- ✅ Reliable
- ❌ No free tier (requires credit card)
- ⚠️ More complex setup

### Step-by-Step Deployment

#### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Create Required Files

**`Procfile`** (no extension):
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

**`runtime.txt`**:
```
python-3.11.0
```

**`setup.sh`** (optional, for dependencies):
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

#### Step 3: Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create dc-topology-planner

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main
```

---

## Option 5: Self-Hosted (VPS/Docker)

### Why Self-Hosted
- ✅ Full control
- ✅ Can be cost-effective
- ❌ Requires server management
- ❌ You handle security/updates

### Docker Deployment

#### Step 1: Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
```

#### Step 3: Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

### VPS Deployment (Ubuntu)

```bash
# On your VPS
sudo apt update
sudo apt install python3.11 python3-pip

# Clone repository
git clone YOUR_REPO_URL
cd dc_topology_planner

# Install dependencies
pip3 install -r requirements.txt

# Run with nohup (or use systemd service)
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &

# Or use systemd (better)
sudo nano /etc/systemd/system/streamlit-app.service
```

**Systemd service file** (`/etc/systemd/system/streamlit-app.service`):

```ini
[Unit]
Description=Streamlit DCN Topology Planner
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/dc_topology_planner
ExecStart=/usr/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app
```

---

## Common Deployment Issues

### Issue: App Not Accessible

**Symptoms:** 404 or connection refused

**Solutions:**
1. Check `server.address = 0.0.0.0` (not `localhost`)
2. Verify port is correct (`$PORT` or `8501`)
3. Check firewall/security groups allow traffic

### Issue: Import Errors

**Symptoms:** `ModuleNotFoundError`

**Solutions:**
1. Verify `requirements.txt` includes all dependencies
2. Check Python version matches (`runtime.txt`)
3. Ensure all files are committed to Git

### Issue: Build Fails

**Symptoms:** Deployment fails during build

**Solutions:**
1. Check `requirements.txt` syntax
2. Verify Python version compatibility
3. Check build logs for specific errors

### Issue: App Crashes After Deployment

**Symptoms:** App deploys but crashes on access

**Solutions:**
1. Check application logs
2. Verify environment variables
3. Test locally first: `streamlit run app.py`

---

## Environment Variables

Some platforms allow environment variables. Common ones:

```bash
# Streamlit config
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Python
PYTHON_VERSION=3.11.0
```

---

## Security Considerations

### For Production

1. **Don't commit secrets**: Use environment variables
2. **Enable authentication**: Streamlit supports password protection
3. **Use HTTPS**: Most platforms provide this automatically
4. **Rate limiting**: Consider adding if public-facing

### Streamlit Authentication

Create `.streamlit/config.toml`:

```toml
[server]
headless = true

[server.enableXsrfProtection]
enabled = true
```

Or use Streamlit's built-in authentication (Streamlit Cloud).

---

## Monitoring and Logs

### Streamlit Cloud
- Logs available in dashboard
- Real-time log streaming

### Render
- Logs tab in dashboard
- Can download logs

### Railway
- Logs in dashboard
- Real-time streaming

### Heroku
```bash
heroku logs --tail
```

---

## Cost Comparison

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Streamlit Cloud | ✅ Unlimited | N/A |
| Render | ✅ Free (slow) | $7/month |
| Railway | ⚠️ $5 credit | $5+/month |
| Heroku | ❌ None | $7+/month |
| VPS (DigitalOcean) | ❌ None | $6+/month |

---

## Recommendation

**For most users:** Use **Streamlit Community Cloud**
- Easiest setup
- Free forever
- Built for Streamlit
- Zero configuration

**For private repos:** Use **Render**
- Free tier supports private repos
- Easy setup
- Good performance

**For advanced needs:** Use **Railway** or **Self-Hosted**
- More control
- Custom configurations
- Better for production

---

## Next Steps

1. **Choose a platform** based on your needs
2. **Follow the step-by-step guide** for that platform
3. **Test your deployment** thoroughly
4. **Monitor logs** for any issues
5. **Update documentation** with your app URL

---

## Quick Reference

### Files Needed for Deployment

- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Main application
- ⚠️ `Procfile` - For Heroku/Railway
- ⚠️ `runtime.txt` - For Heroku/Railway
- ⚠️ `render.yaml` - For Render
- ⚠️ `Dockerfile` - For Docker/self-hosted

### Essential Commands

```bash
# Test locally
streamlit run app.py

# Check requirements
pip list

# Freeze requirements
pip freeze > requirements.txt

# Git workflow
git add .
git commit -m "Deploy ready"
git push
```

---

**Need help?** Check platform-specific documentation or the main SETUP_GUIDE.md for local development issues.
