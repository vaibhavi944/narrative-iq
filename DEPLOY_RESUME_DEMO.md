# NarrativeIQ Free Demo Deployment

This branch is prepared for a free split deployment:

- Frontend on Vercel
- Backend on Hugging Face Spaces using Docker

This is the easiest no-card path that stays close to your localhost app.

## What Stays The Same

- Same Next.js frontend
- Same FastAPI backend
- Same `src/` AI/ML pipeline
- Same `/analyze` and `/rewrite` API flow

## What Is Different From Localhost

- The frontend and backend use different public URLs
- The frontend calls the live backend URL instead of `http://localhost:8000`
- The backend may be slower on the first request after inactivity

## Why This Path

- Vercel is the easiest free host for your existing Next.js frontend
- Hugging Face Spaces supports Docker and offers free `CPU Basic` hardware
- This avoids Oracle VM setup and avoids adding a credit card to a service like Northflank or Koyeb

## 1. Deploy The Frontend To Vercel

Push this branch first:

```bash
git push origin demo/resume-deploy
```

Then in Vercel:

1. Import your GitHub repo
2. Set the Root Directory to `frontend`
3. Do not deploy yet if you don't know the backend URL

## 2. Create The Backend On Hugging Face Spaces

Create a new public Space on Hugging Face:

- SDK: `Docker`
- Space name: for example `narrativeiq-backend`

Then create a separate backend repo for the Space by copying these items from this project into the Space repo root:

- `api/`
- `src/`
- `data/`
- `requirements.txt`
- files from [hf-space-template](/abs/path/C:/Users/vaibh/ai_projects/narrative-iq/hf-space-template)

The template folder gives you the `Dockerfile` and `README.md` needed by the Space.

## 3. Add Backend Secret On Hugging Face

In your Space settings, add this secret:

- `GROQ_API_KEY_1`

Use your real Groq key as the value.

If you use more than one key locally, you can also add:

- `GROQ_API_KEY_2`
- `GROQ_API_KEY_3`

## 4. Wait For The Space To Build

When the Space finishes building, it will have a URL like:

```text
https://your-username-narrativeiq-backend.hf.space
```

Check health:

```text
https://your-username-narrativeiq-backend.hf.space/health
```

You want:

```json
{"status":"ok"}
```

## 5. Finish Vercel Frontend Setup

In your Vercel project environment variables, add:

```env
NEXT_PUBLIC_API_URL=https://your-username-narrativeiq-backend.hf.space
```

Then deploy the frontend.

## 6. Test The Live App

Open the Vercel URL and test:

- analyze flow
- rewrite flow
- language switching

## Localhost Still Works

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

Your local frontend still uses `http://localhost:8000` automatically.

## Important Limits

- Hugging Face free Spaces can sleep after inactivity on free hardware
- The first request after a sleep can be slower
- This is still much better for your no-card requirement than trying to force the backend onto small free serverless containers

## Rollback

Your exact preserved snapshot is:

- Branch: `pre-demo-snapshot-2026-05-22`
- Commit: `97560627672de09f8ba5b9671d2d9a310ae2586d`
