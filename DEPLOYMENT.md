# Deployment

Set `CORS_ORIGINS` in the backend environment to the exact frontend origin, for example:

```env
CORS_ORIGINS=https://your-wishmate.vercel.app
```

For multiple frontend origins, separate them with commas and do not add trailing slashes.

## Backend

Build and run the backend from the `backend` directory:

```powershell
docker build -t wishmate-api .
docker run --env-file .env -p 8000:8000 wishmate-api
```

Keep the Supabase secret key, Groq key, email credentials, and JWT secret in the hosting provider's server-side environment settings.

For Render, configure Gmail SMTP with STARTTLS:

```env
EMAIL_ADDRESS=your-gmail@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_SSL=false
```

Configure the deployment health checks as follows:

- Liveness: `GET /health`
- Readiness: `GET /ready`

Run only one backend scheduler instance unless scheduling is moved to a separate worker. Multiple API replicas can otherwise send duplicate birthday emails.

## Frontend

Build the frontend with the public API URL:

```powershell
docker build --build-arg VITE_API_URL=https://api.example.com -t wishmate-web .
docker run -p 8080:80 wishmate-web
```

`VITE_API_URL` is public and must contain only the backend URL. Never put backend secrets in frontend environment variables.

## Supabase

Run `backend/supabase_schema.sql` in the Supabase SQL Editor before the first deployment. Keep RLS enabled and use the Supabase secret/service-role key only in the backend.
