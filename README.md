# DevBlog

Blog u Flasku gde pišem o greškama na koje sam naišao u svojim projektima i kako sam ih rešio.
Čitaoci mogu da se registruju i komentarišu, a članke objavljuje samo admin.

Uživo: https://flask-blog-ud95.onrender.com (besplatan Render server, prvo otvaranje traje oko pola minuta)

## Šta radi

- Registracija i prijava (Flask-Login, lozinke kao heš)
- Članci sa podnaslovom, komentari i stranice po 5 članaka
- Pisanje, izmena i brisanje članaka samo za admina; prvi registrovani nalog postaje admin
- Prazan blog može da dobije tri primera članka (`SEED_DEMO_POSTS=true`)

## Bezbednost

- CSRF token na svakoj formi, uključujući brisanje članka
- Rute za pisanje proveravaju da li je korisnik admin (inače 403)
- `SECRET_KEY` i adresa baze se čitaju iz okruženja

## Tehnologije

Python 3, Flask, SQLAlchemy, Flask-Login, Flask-WTF, PostgreSQL (Neon), Jinja2 i čist CSS. Hostovano na Renderu.

## Lokalno

```bash
pip install -r requirements.txt
export SECRET_KEY=nesto-dugacko-i-nasumicno
python run.py
```

Bez `DATABASE_URL` aplikacija koristi lokalni SQLite fajl. Otvori http://localhost:5000.

## Autor

Bogdan Šarčević, Užice
