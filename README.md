<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Coffee Shop API — User Service</title>
</head>
<body>

<h1>☕ Coffee Shop API — User Service</h1>

<h2>📌 Overview</h2>
<p>
  This service is part of the <strong>Coffee Shop API</strong> and provides full user management:
</p>
<ul>
  <li>Registration, authentication, verification (email/SMS)</li>
  <li>JWT tokens (access & refresh)</li>
  <li>Role-based access (User/Admin)</li>
  <li>Background tasks (verification cleanup)</li>
  <li>Async stack: <strong>FastAPI + SQLAlchemy 2.0 + Celery + Redis + Postgres</strong></li>
</ul>
<p>
  The project follows <strong>Domain Driven Design (DDD)</strong>, <strong>Clean Architecture</strong> and <strong>SOLID</strong> principles.
</p>

<h2>🏗️ Architecture & Patterns</h2>
<ul>
  <li><strong>Domain Driven Design (DDD)</strong>
    <ul>
      <li><code>domain/</code> — entities, value objects, domain services, domain exceptions</li>
      <li><code>application/</code> — use cases (services, DTOs)</li>
      <li><code>infrastructure/</code> — SQLAlchemy ORM, repositories, Celery, email adapters</li>
      <li><code>presentation/</code> — FastAPI routers, dependencies, error mappers</li>
    </ul>
  </li>
  <li><strong>Unit of Work pattern</strong> — abstract <code>IUnitOfWork</code> in <code>domain/</code>, SQLAlchemy implementation in <code>infrastructure/</code></li>
  <li><strong>Repository pattern</strong> — abstract in <code>domain/</code>, SQLAlchemy in <code>infrastructure/</code></li>
  <li><strong>Security</strong> — JWT provider, password hashing (Argon2 / bcrypt) in <code>infrastructure/security/</code></li>
  <li><strong>Background tasks</strong> — Celery workers + Celery Beat scheduler for cleaning up unverified users</li>
</ul>

<h2>⚙️ Configuration</h2>
<p>All configuration lives in the <code>configs/</code> package and can be overridden in two ways:</p>
<ol>
  <li>
    <strong>Environment variables</strong> — for example, in <code>.env</code>:
    <pre>
DB_USER=postgres
DB_PASS=123456
DB_HOST=db
DB_PORT=5432
DB_NAME=coffee_shop

SERVER_HOST=0.0.0.0
SERVER_PORT=8000

REDIS_HOST=redis
REDIS_PORT=6379

MAIL_SMTP_HOST=maildev
MAIL_SMTP_PORT=1025
MAIL_SENDER_EMAIL=no-reply@coffeeshop.local
    </pre>
  </li>
  <li>
    <strong>Bash entrypoint scripts</strong> — values can be overridden at runtime via ENV in Docker Compose.
  </li>
</ol>

<h2>📬 Email / MailDev</h2>
<p>For local development we use <strong>MailDev</strong>:</p>
<ul>
  <li>Web UI: <a href="http://localhost:1080">http://localhost:1080</a></li>
  <li>SMTP: <code>host=maildev</code>, <code>port=1025</code></li>
</ul>
<p>All verification codes/emails are sent to MailDev instead of real mail servers.</p>

<h2>🚀 How to run</h2>
<h3>1. Clone repo & set up <code>.env</code></h3>
<pre><code>cp .env.example .env</code></pre>

<h3>2. Start with Docker Compose</h3>
<pre><code>docker compose up --build</code></pre>
<p>This runs:</p>
<ul>
  <li><strong>api</strong> — FastAPI app via Gunicorn/Uvicorn</li>
  <li><strong>celery</strong> — worker + beat (background tasks)</li>
  <li><strong>db</strong> — Postgres 16</li>
  <li><strong>redis</strong> — Redis 7</li>
  <li><strong>maildev</strong> — MailDev</li>
</ul>

<h3>3. Check API docs</h3>
<p><a href="http://localhost:8000/docs">http://localhost:8000/docs</a></p>

<h3>4. Run migrations manually (if needed)</h3>
<pre><code>docker compose exec api alembic upgrade head</code></pre>

<h2>🔑 Endpoints</h2>
<ul>
  <li><code>POST /auth/signup</code> — Register new user</li>
  <li><code>POST /auth/login</code> — Authenticate (get tokens)</li>
  <li><code>POST /auth/verify</code> — Verify user via email code</li>
  <li><code>POST /auth/refresh</code> — Refresh access token</li>
  <li><code>GET /me</code> — Current user info</li>
  <li><code>GET /users</code> — List users (Admin only)</li>
</ul>

<h2>🛠️ Development notes</h2>
<ul>
  <li>Hot-reload available via <code>volumes</code> in <code>docker-compose.override.yml</code></li>
  <li>Error handling unified via <code>DomainError</code> → HTTPException mapper</li>
</ul>

</body>
</html>
