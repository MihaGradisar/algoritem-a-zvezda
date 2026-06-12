"""
A zvezda (A-Star) iskanje najkrajse poti v cestnem omrezju med slovenskimi mesti.

Cilj: poiscemo najcenejso pot od Kopra do Murske Sobote.
- g(n): dejanski sesteti strosek poti od starta do vozlisca n (cestne razdalje v km)
- h(n): hevristika, ocena zracne razdalje od n do cilja (nikoli ne preceni)
- f(n) = g(n) + h(n): ocena celotne poti skozi n
"""

import heapq
import matplotlib.pyplot as plt
import networkx as nx


# --- Definicija problema ------------------------------------------------------

# Neusmerjen cestni graf: mesto -> [(sosed, cestna_razdalja_km), ...]
GRAF = {
    "Koper":         [("Postojna", 55)],
    "Postojna":      [("Koper", 55), ("Ljubljana", 53)],
    "Ljubljana":     [("Postojna", 53), ("Celje", 75), ("Novo mesto", 72)],
    "Celje":         [("Ljubljana", 75), ("Velenje", 30), ("Maribor", 55)],
    "Novo mesto":    [("Ljubljana", 72), ("Maribor", 100)],
    "Velenje":       [("Celje", 30), ("Maribor", 42)],
    "Maribor":       [("Celje", 55), ("Novo mesto", 100), ("Velenje", 42),
                      ("Ptuj", 28), ("Murska Sobota", 58)],
    "Ptuj":          [("Maribor", 28), ("Murska Sobota", 32)],
    "Murska Sobota": [("Maribor", 58), ("Ptuj", 32)],
}

# Hevristika h(n): ocena zracne razdalje do cilja (Murska Sobota) v km.
# Zracna razdalja je vedno krajsa ali enaka cestni, zato hevristika nikoli
# ne preceni dejanskega stroska (je dopustna -> A zvezda najde optimalno pot).
H = {
    "Koper": 250, "Postojna": 210, "Ljubljana": 160, "Celje": 95,
    "Novo mesto": 135, "Velenje": 85, "Maribor": 50, "Ptuj": 28,
    "Murska Sobota": 0,
}

START = "Koper"
CILJ = "Murska Sobota"

# Priblizne geografske lege mest (vzhod, sever) za map-like izris.
LEGE = {
    "Koper": (0.0, 0.0), "Postojna": (1.2, 0.8), "Ljubljana": (2.5, 1.5),
    "Novo mesto": (3.6, 0.4), "Celje": (4.2, 2.2), "Velenje": (4.3, 3.1),
    "Maribor": (6.2, 3.2), "Ptuj": (6.9, 2.5), "Murska Sobota": (8.0, 3.7),
}


# --- Algoritem A zvezda -------------------------------------------------------

def a_zvezda(graf, h, start, cilj):
    """Vrne (pot, skupni_strosek, vrstni_red_sirjenja)."""
    # OPEN je prioritetna vrsta z elementi (f, g, vozlisce)
    open_seznam = [(h[start], 0, start)]
    stars = {start: None}      # za rekonstrukcijo poti
    g_cena = {start: 0}        # najboljsi znani g za vsako vozlisce
    zaprti = set()             # CLOSED
    vrstni_red = []            # vrstni red, v katerem siri vozlisca

    while open_seznam:
        f, g, vozlisce = heapq.heappop(open_seznam)

        # Zastareli vnos (vozlisce smo ze obdelali po cenejsi poti) preskocimo.
        if vozlisce in zaprti:
            continue
        zaprti.add(vozlisce)
        vrstni_red.append(vozlisce)

        if vozlisce == cilj:
            return rekonstruiraj(stars, cilj), g, vrstni_red

        for sosed, cena in graf[vozlisce]:
            if sosed in zaprti:
                continue
            nova_g = g + cena
            # Sosed dodamo/posodobimo le, ce smo nasli cenejso pot do njega.
            if sosed not in g_cena or nova_g < g_cena[sosed]:
                g_cena[sosed] = nova_g
                stars[sosed] = vozlisce
                heapq.heappush(open_seznam, (nova_g + h[sosed], nova_g, sosed))

    return None, float("inf"), vrstni_red


def rekonstruiraj(stars, cilj):
    """Sledi kazalcem stars od cilja do starta in obrne pot."""
    pot = []
    vozlisce = cilj
    while vozlisce is not None:
        pot.append(vozlisce)
        vozlisce = stars[vozlisce]
    return pot[::-1]


def g_vrednosti_sirjenja(graf, h, start, cilj):
    """Zbere koncni g za vsako sirjeno vozlisce (za stolpicni graf)."""
    g_po_sirjenju = {}
    g_cena = {start: 0}
    open_seznam = [(h[start], 0, start)]
    zaprti = set()
    while open_seznam:
        f, g, v = heapq.heappop(open_seznam)
        if v in zaprti:
            continue
        zaprti.add(v)
        g_po_sirjenju[v] = g
        if v == cilj:
            break
        for sosed, cena in graf[v]:
            if sosed in zaprti:
                continue
            ng = g + cena
            if sosed not in g_cena or ng < g_cena[sosed]:
                g_cena[sosed] = ng
                heapq.heappush(open_seznam, (ng + h[sosed], ng, sosed))
    return g_po_sirjenju


# --- Vizualizacija ------------------------------------------------------------

def izrisi_graf(graf, pot, datoteka):
    """Narise cestni graf z razdaljami in oznaci najdeno optimalno pot."""
    G = nx.Graph()
    for vozlisce, sosedje in graf.items():
        for sosed, cena in sosedje:
            G.add_edge(vozlisce, sosed, weight=cena)

    pot_povezave = set(zip(pot, pot[1:]))

    def je_na_poti(u, v):
        return (u, v) in pot_povezave or (v, u) in pot_povezave

    barve_povezav = ["#c0392b" if je_na_poti(u, v) else "#bdc3c7" for u, v in G.edges()]
    sirine = [3.0 if je_na_poti(u, v) else 1.0 for u, v in G.edges()]
    barve_vozlisc = ["#c0392b" if n in pot else "#3498db" for n in G.nodes()]

    # Oznake mest narisemo pod vozlisci, da se daljsa imena ne odrezejo.
    lege_oznak = {n: (x, y - 0.32) for n, (x, y) in LEGE.items()}

    plt.figure(figsize=(11, 6))
    nx.draw_networkx_edges(G, LEGE, edge_color=barve_povezav, width=sirine)
    nx.draw_networkx_nodes(G, LEGE, node_color=barve_vozlisc, node_size=700)
    nx.draw_networkx_labels(G, lege_oznak, font_size=9, font_weight="bold")
    nx.draw_networkx_edge_labels(
        G, LEGE, edge_labels=nx.get_edge_attributes(G, "weight"), font_size=8
    )
    plt.title("Cestni graf z oznaceno optimalno potjo (rdeca)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(datoteka, dpi=150, bbox_inches="tight")
    plt.close()


def izrisi_f_vrednosti(vrstni_red, g_po_sirjenju, h, datoteka):
    """Stolpicni graf g, h in f za vsako vozlisce v vrstnem redu sirjenja."""
    g_vals = [g_po_sirjenju[n] for n in vrstni_red]
    h_vals = [h[n] for n in vrstni_red]
    f_vals = [g + h_ for g, h_ in zip(g_vals, h_vals)]

    x = range(len(vrstni_red))
    sirina = 0.27
    plt.figure(figsize=(10, 5))
    plt.bar([i - sirina for i in x], g_vals, sirina, label="g(n)", color="#3498db")
    plt.bar(list(x), h_vals, sirina, label="h(n)", color="#2ecc71")
    plt.bar([i + sirina for i in x], f_vals, sirina, label="f(n) = g + h", color="#c0392b")
    plt.xticks(list(x), vrstni_red, rotation=30, ha="right")
    plt.ylabel("Strosek (km)")
    plt.title("g, h in f po korakih")
    plt.legend()
    plt.tight_layout()
    plt.savefig(datoteka, dpi=150, bbox_inches="tight")
    plt.close()


# --- Glavni program -----------------------------------------------------------

def main():
    pot, strosek, vrstni_red = a_zvezda(GRAF, H, START, CILJ)

    print("Vrstni red sirjenja vozlisc:")
    print("  " + " -> ".join(vrstni_red))

    if pot is None:
        print("\nPoti do cilja ni.")
        return

    print("\nOptimalna pot:")
    print("  " + " -> ".join(pot))
    print(f"\nSkupni strosek: {strosek} km")

    g_po_sirjenju = g_vrednosti_sirjenja(GRAF, H, START, CILJ)
    izrisi_graf(GRAF, pot, "slika1_graf.png")
    izrisi_f_vrednosti(vrstni_red, g_po_sirjenju, H, "slika2_f.png")
    print("\nShranjena grafa: slika1_graf.png, slika2_f.png")


if __name__ == "__main__":
    main()
