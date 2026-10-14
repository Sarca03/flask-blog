# DevBlog

A Flask blog where I write about bugs I ran into on my projects and how I fixed them.
Readers can sign up and comment, only the admin publishes posts.

Live: https://flask-blog-ud95.onrender.com (free Render server, the first visit takes about half a minute)

The posts and the interface are in Serbian.

## What it does

- Sign up and login (Flask-Login, hashed passwords)
- Posts with a subtitle, comments and pages of 5 posts
- Only the admin can write, edit and delete posts; the first registered account becomes admin
- An empty blog can get three sample posts (`SEED_DEMO_POSTS=true`)

## Security

- CSRF token on every form, including deleting a post
- Write routes check that the user is admin (otherwise 403)
- `SECRET_KEY` and the database address come from the environment

## Stack

Python 3, Flask, SQLAlchemy, Flask-Login, Flask-WTF, PostgreSQL (Neon), Jinja2 and plain CSS. Hosted on Render.

## Running locally

```bash
pip install -r requirements.txt
export SECRET_KEY=something-long-and-random
python run.py
```

Without `DATABASE_URL` the app uses a local SQLite file. Open http://localhost:5000.

## Author

Bogdan Šarčević, Užice, Serbia
