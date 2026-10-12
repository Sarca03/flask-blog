"""Primeri članaka za prazan blog.

Pokreće se iz create_app() samo kad je SEED_DEMO_POSTS=true i kad nema
nijednog članka, pa je bezbedno ostaviti promenljivu uključenu.
Članci se pripisuju prvom admin nalogu.
"""
from datetime import datetime, timedelta

from app import db
from app.models import Post, User

POSTS = [
    {
        "days_ago": 9,
        "title": "Prihod se računa samo od završenih termina",
        "subtitle": "Mala odluka u bazi koja menja ceo dashboard aplikacije za perionicu.",
        "content": """Kad sam pravio pregled za aplikaciju za auto perionicu, prvi broj koji sam hteo da prikažem bio je prihod. Najlakše je sabrati cenu svih termina, ali to bi bila laž: otkazan termin nije doneo ni dinar, a termin koji je tek zakazan još nije naplaćen.

Zato se prihod računa samo od termina sa statusom „završen“:

```
SELECT COALESCE(SUM(total_price), 0)
FROM appointments
WHERE status = 'Completed'
```

`COALESCE` je tu da upit vrati 0 umesto praznog rezultata kad još nema nijednog završenog termina, pa frontend ne mora posebno da proverava taj slučaj.

Druga sitnica: cena se pamti na samom terminu, a ne samo na usluzi. Ako vlasnik sutra poskupi pranje, stari termini i dalje pokazuju koliko je klijent tada platio, pa se ni prošlomesečni prihod ne menja.

Na pregledu sada stoji i broj termina po statusu, pa se odmah vidi koliko je toga još na čekanju.""",
    },
    {
        "days_ago": 4,
        "title": "Termin u 10:00 koji se sačuva kao 12:00",
        "subtitle": "Kako sam našao grešku sa vremenskom zonom u formi za zakazivanje.",
        "content": """Zakažem termin za 10:00, sačuvam, a u listi piše 12:00. Tačno dva sata razlike, koliko je Srbija leti ispred UTC vremena.

Polje `<input type="datetime-local">` vraća vreme bez vremenske zone, na primer `2026-10-11T10:00`. Ja sam ga takvog slao serveru, a PostgreSQL ga je čuvao kao da je u UTC-u. Kad se termin vratio u browser i prikazao po lokalnom vremenu, dobio sam dva sata više.

Ista greška je postojala i u suprotnom smeru: forma za izmenu je vreme sa servera pretvarala sa `toISOString()`, što je opet UTC, pa je termin od 10:00 u formi izgledao kao 08:00.

Popravka je bila u dve male funkcije. Pri slanju pretvaram vrednost iz polja u ISO sa zonom, `new Date(value).toISOString()`, da server tačno zna o kom trenutku se radi. Pri otvaranju forme ručno sastavljam lokalni datum i vreme, umesto `toISOString()`.

Od tada, kad god datum ide između browsera i baze, prvo proverim u kojoj je zoni.""",
    },
    {
        "days_ago": 1,
        "title": "Demo nalog koji niko ne može da pokvari",
        "subtitle": "Šta se desi kad javno napišeš admin lozinku na stranici za prijavu.",
        "content": """U aplikaciji za perionicu na stranici za prijavu stajali su korisničko ime i lozinka admin naloga, da onaj ko gleda portfolio može odmah da uđe. Posle nekoliko dana baza je bila puna izmišljenih klijenata i usluga koje ne bih smeo ovde da napišem.

Problem nije bio u lozinci, nego u tome što je demo nalog imao ista prava kao vlasnik. Rešenje ima tri dela.

Prvo, poseban nalog „demo“ koji može samo da čita. Na serveru je to jedan middleware: ako je korisnik demo, a zahtev je `POST`, `PUT`, `PATCH` ili `DELETE`, odgovor je `403`. Frontend sakriva dugmad za izmenu, ali prava zaštita je na serveru, jer se zahtev može poslati i mimo interfejsa.

Drugo, javna registracija je zatvorena. Usput sam našao i ozbiljniju rupu: ruta za registraciju je ulogu uzimala iz tela zahteva, pa je svako mogao da pošalje `role: "admin"` i dobije sva prava. Sada se uloga nikad ne čita iz zahteva.

Treće, nova admin lozinka i novi JWT ključ, da svi stari tokeni prestanu da važe.

Na stranici za prijavu sada stoji dugme „Pogledaj demo“, bez lozinke.""",
    },
]


def seed_demo_posts():
    if Post.query.first() is not None:
        return
    author = User.query.filter_by(is_admin=True).order_by(User.id).first()
    if author is None:
        return
    now = datetime.utcnow()
    for item in POSTS:
        db.session.add(Post(
            title=item["title"],
            subtitle=item["subtitle"],
            content=item["content"],
            date_posted=now - timedelta(days=item["days_ago"]),
            author=author,
        ))
    db.session.commit()

