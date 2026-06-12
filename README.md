# Iskanje z algoritmom A*

Cilj je razumeti in uporabiti algoritem A* (A-star) za iskanje najcenejše poti ter rezultat predstaviti v kratkem poročilu.

## Kaj se študent nauči

- Razume razliko med slepim in informiranim iskanjem ter vlogo hevristike.
- Razume pomen vrednosti g(n), h(n) in f(n).
- Razume vlogo seznamov OPEN in CLOSED ter kako določata vrstni red širjenja vozlišč.
- Razume, kako algoritem sestavi končno pot in njen strošek.
- Razume, zakaj dopustna hevristika zagotavlja optimalno pot.

## Naloga

Implementiraj A* in ga uporabi na problemu, ki si ga izbereš sam. Uporabiš ga lahko povsod, kjer iščeš najcenejšo pot skozi prostor stanj in imaš hevristiko za oceno oddaljenosti do cilja. Nekaj možnih problemov:

- pot na cestnem ali mestnem zemljevidu,
- pot v mreži (grid) za igro ali robota, s Manhattansko ali evklidsko razdaljo kot hevristiko,
- premične uganke, na primer osmica (8-puzzle), s številom napačno postavljenih ploščic kot hevristiko,
- katerikoli graf, kjer znaš definirati stroške povezav in hevristiko.

Sam definiraj vozlišča, povezave s stroški, začetno in ciljno stanje ter hevristiko h(n). Hevristika nikoli ne sme preceniti dejanske cene do cilja (dopustnost), sicer A* ne zagotavlja optimalne rešitve.

## Zahteve

1. Z A* poišči najcenejšo pot od začetnega do ciljnega stanja.
2. Za vsak korak prikaži razširjeno vozlišče ter g(n), h(n) in f(n).
3. Vodi seznama OPEN in CLOSED ter določi vrstni red širjenja.
4. Rekonstruiraj končno pot in izračunaj skupni strošek.
5. Oceni optimalnost (je hevristika dopustna in konsistentna?).
6. Implementiraj A* v Pythonu (priporočeno: `heapq` za OPEN, slovarji za graf in hevristiko). Koda naj izpiše potek in ga vizualizira.
7. Oddaj poročilo v PDF, 3–4 strani z grafi in razlago.

## Primer v tem repozitoriju

Priložen primer reši konkreten primerek: pot med slovenskimi mesti od Kopra do Murske Sobote. Služi le kot vzorec poročila in kode. Tvoj problem je lahko drugačen.

- `a_zvezda.py` – celotna rešitev (podatki, algoritem, izris). Za drug problem spremeniš podatke na vrhu datoteke.
- `algoritem_a_zvezda.pdf` – vzorčno poročilo.
- `slika1_graf.png`, `slika2_f.png` – grafa, ki ju ustvari koda.

## Zagon

```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install networkx matplotlib
python a_zvezda.py
```

Program izpiše vrstni red širjenja, optimalno pot in strošek ter shrani sliki `slika1_graf.png` in `slika2_f.png`.
