# NarrativeIQ Demo Deployment Guide

This branch is prepared for a single-VM deployment so the frontend and backend
keep working together without changing the core AI/ML pipeline.

## What This Branch Preserves

- The existing FastAPI backend
- The existing Next.js frontend
- The current `src/` AI/ML pipeline
- The local workflow you already use

## What Changed On This Branch

- Added Docker packaging for frontend and backend
- Added Caddy as a reverse proxy so one domain serves both apps
- Added backend lazy initialization to make startup less brittle
- Added same-origin API fallback so deployed frontend can call the backend

## Recommended Free Hosting Path

Use an Oracle Cloud Always Free VM and run this branch with Docker Compose.

Why this path:

- It can stay up for months
- It supports your current heavier Python runtime better than free serverless
- It avoids splitting frontend and backend across two fragile free services

## 1. Create the VM

Create an Oracle Cloud Always Free Ubuntu VM.

Recommended minimum setup:

- Ubuntu 22.04 or 24.04
- Public IP enabled
- Ports `80`, `443`, and `22` opened in Oracle security rules

## 2. Install Docker

SSH into the VM and run:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

## 3. Upload the Repo

On the VM:

```bash
git clone <your-repo-url>
cd narrative-iq
git checkout demo/resume-deploy
```

## 4. Create the Environment File

Create `.env` in the repo root:

```env
GROQ_API_KEY_1=your_key_here
CADDY_HOST=your-domain.com
```

If you do not have a custom domain yet, use:

```env
GROQ_API_KEY_1=your_key_here
CADDY_HOST=localhost
```

For public use, a real domain is better because Caddy can automatically create HTTPS.

## 5. Start the Stack

```bash
docker compose up -d --build
```

## 6. Check Health

```bash
docker compose ps
docker compose logs backend --tail=100
docker compose logs frontend --tail=100
docker compose logs caddy --tail=100
curl http://localhost/health
```

Expected result:

```json
{"status":"ok"}
```

## 7. Optional Domain Setup

Point your domain's DNS `A` record to the VM public IP.

Then set:

```env
CADDY_HOST=your-domain.com
```

Restart:

```bash
docker compose up -d
```

Caddy will handle HTTPS automatically after DNS is correct.

## Local Development Still Works

Your existing local setup is still valid.

Backend:

```bash
python api/main.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend still uses `http://localhost:8000` automatically when running on localhost.

## Notes

- The first retrieval request may be slower because the sentence-transformer model may need to download into the Hugging Face cache volume.
- Free serverless hosts are still likely to fail on this backend because of runtime size and memory usage.
- This branch is for deployment stability. Your original development snapshot was preserved separately before these changes.
