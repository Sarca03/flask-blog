# DevBlog Portfolio — Flask Blog App

Full-stack blog aplikacija napravljena u Flask-u sa SQLite bazom.

## Funkcionalnosti
- Registracija i prijava korisnika
- Kreiranje, izmena i brisanje članaka
- Komentari na člancima
- Paginacija
- Admin uloga (prvi korisnik postaje admin)
- Responsive dizajn (Bootstrap 5)

## Tehnologije
- Python 3 + Flask
- SQLAlchemy (ORM)
- Flask-Login (auth)
- Flask-WTF (forme)
- SQLite (baza)
- Bootstrap 5 + FontAwesome
- Jinja2 (templates)

## Bezbednost
- password_hash() za lozinke
- CSRF zaštita (Flask-WTF)
- Zaštićene rute (login_required)
- Admin provere

## Instalacija
1. Kloniraj repo
2. `pip install -r requirements.txt`
3. Napravi `.env` fajl sa `SECRET_KEY`
4. `python run.py`
5. Otvori `http://localhost:5000`

## Autor
Bogdan Šarčević — Full-Stack Developer