#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLÉOPÂTRE — diagramme 01_classes_global.png
Vue d'ensemble des classes : 5 packages + zone « Services Applicatifs ».
Master SVG (rendu ensuite en PNG haute résolution, 2400 x 1350).
"""
import os
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

# ---------------------------------------------------------------- design system
BG        = "#FAFAF9"   # papier très chaud
INK       = "#111827"   # quasi noir
INDIGO    = "#1E3A5F"   # accent primaire
GOLD      = "#B45309"   # accent secondaire (parcimonieux)
BORDER    = "#E5E7EB"
WARM      = "#FFFBF5"   # packages chauds
DB_FILL   = "#F0F7F4"   # base de données
DB_BORDER = "#D8E8E0"
MUTED     = "#6B7280"
FAINT     = "#9CA3AF"
CHIP_MUTE = "#4B5563"

FONT_FILES = {
    ("Inter", 400): os.path.join(FONTS, "Inter-Regular.ttf"),
    ("Inter", 500): os.path.join(FONTS, "Inter-Medium.ttf"),
    ("Inter", 600): os.path.join(FONTS, "Inter-SemiBold.ttf"),
    ("Inter", 700): os.path.join(FONTS, "Inter-Bold.ttf"),
    ("JetBrains Mono", 400): os.path.join(FONTS, "JetBrainsMono-Regular.ttf"),
    ("JetBrains Mono", 600): os.path.join(FONTS, "JetBrainsMono-SemiBold.ttf"),
}
_metrics = {}
def _metric(family, weight):
    key = (family, weight)
    if key not in _metrics:
        f = TTFont(FONT_FILES[key], lazy=True)
        upm = f["head"].unitsPerEm
        hmtx = f["hmtx"].metrics
        adv = {}
        for cp, gname in f.getBestCmap().items():
            adv[cp] = hmtx[gname][0] / upm if gname in hmtx else 0.5
        _metrics[key] = adv
    return _metrics[key]

def tw(text, size, family="Inter", weight=400, ls=0.0):
    adv = _metric(family, weight)
    return sum(adv.get(ord(c), 0.5) * size for c in text) + ls * max(0, len(text) - 1)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- primitives
out = []
def rect(x, y, w, h, rx, fill, stroke=None, sw=1.0, shadow=None, opacity=None):
    a = f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}"'
    if stroke:  a += f' stroke="{stroke}" stroke-width="{sw}"'
    if shadow:  a += f' filter="url(#{shadow})"'
    if opacity is not None: a += f' opacity="{opacity}"'
    out.append(a + "/>")

def text(x, y, s, size, family="Inter", weight=400, fill=INK, anchor="start", ls=None, opacity=None):
    a = (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
         f'font-weight="{weight}" fill="{fill}"')
    if anchor != "start": a += f' text-anchor="{anchor}"'
    if ls: a += f' letter-spacing="{ls}"'
    if opacity is not None: a += f' opacity="{opacity}"'
    out.append(a + f'>{esc(s)}</text>')

def line(x1, y1, x2, y2, stroke, sw=1.0, dash=None, opacity=1.0, cap="round"):
    a = (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
         f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"')
    if dash: a += f' stroke-dasharray="{dash}"'
    if opacity < 1: a += f' opacity="{opacity}"'
    out.append(a + "/>")

def circle(cx, cy, r, fill, opacity=1.0):
    a = f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{fill}"'
    if opacity < 1: a += f' opacity="{opacity}"'
    out.append(a + "/>")

def rpath(points, r=12.0, stroke=INDIGO, sw=1.7, dash="7 5", opacity=0.55):
    pts = []
    for x, y in points:                      # élimine les points doublons
        q = (float(x), float(y))
        if not pts or abs(q[0] - pts[-1][0]) > 1e-9 or abs(q[1] - pts[-1][1]) > 1e-9:
            pts.append(q)
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        v1 = (p1[0] - p0[0], p1[1] - p0[1]); v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = abs(v1[0]) + abs(v1[1]); l2 = abs(v2[0]) + abs(v2[1])
        r1 = min(r, l1 / 2); r2 = min(r, l2 / 2)
        a = (p1[0] - (v1[0] / l1) * r1, p1[1] - (v1[1] / l1) * r1)
        b = (p1[0] + (v2[0] / l2) * r2, p1[1] + (v2[1] / l2) * r2)
        d += f" L {a[0]:.2f} {a[1]:.2f} Q {p1[0]:.2f} {p1[1]:.2f} {b[0]:.2f} {b[1]:.2f}"
    d += f" L {pts[-1][0]:.2f} {pts[-1][1]:.2f}"
    out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
               f'stroke-dasharray="{dash}" stroke-linecap="round" stroke-linejoin="round" '
               f'opacity="{opacity}"/>')

SW = 1.7
def arrow_up(x, y, color=INDIGO, opacity=0.55, s=6.0, l=10.0):
    line(x, y, x - s, y + l, color, sw=SW, opacity=opacity)
    line(x, y, x + s, y + l, color, sw=SW, opacity=opacity)

def arrow_left(x, y, color=INDIGO, opacity=0.55, s=6.0, l=10.0):
    line(x, y, x + l, y - s, color, sw=SW, opacity=opacity)
    line(x, y, x + l, y + s, color, sw=SW, opacity=opacity)

# ---------------------------------------------------------------- géométrie
W, H = 2400, 1350
M = 40
C1X, C1W = 40, 704
C2X, C2W = 800, 704
C3X, C3W = 1560, 800
R1Y, RH = 40, 452            # ligne 1 : 40 -> 492
R2Y = 536                    # ligne 2 : 536 -> 988
ZONE_Y, ZONE_H = 1052, 258   # zone services : 1052 -> 1310
ADJ = 26                     # marge intérieure des packages
HEAD = 100                   # hauteur de l'en-tête de package
CHIP_H, CHIP_GAP = 56, 14.0
LL1, LL2 = 1008, 1020        # couloir bas (entre 988 et 1052)
TOPA, TOPB = 522, 506        # couloirs entre les deux lignes (492 -> 536)
LANE_L1, LANE_L2 = 762, 780  # couloirs verticaux gauches
LANE_R1, LANE_R2, LANE_R3, LANE_R4 = 1514, 1526, 1538, 1550

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" font-family="Inter">']
svg += ['<defs>',
        '<filter id="shCard" x="-6%" y="-6%" width="112%" height="116%">'
        '<feDropShadow dx="0" dy="2.5" stdDeviation="6.5" flood-color="#111827" flood-opacity="0.055"/></filter>',
        '<filter id="shChip" x="-6%" y="-6%" width="112%" height="116%">'
        '<feDropShadow dx="0" dy="1.2" stdDeviation="2.4" flood-color="#111827" flood-opacity="0.032"/></filter>',
        '</defs>']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# ---------------------------------------------------------------- composants
TAG_FILL, TAG_INK = "#F1F5F9", "#475569"
def pill(x, y, label, fill, color, border=None):
    size, h = 12.5, 24.0
    w = tw(label, size, weight=500) + 24
    rect(x, y, w, h, 12, fill, stroke=border, sw=1.0)
    text(x + w / 2, y + 17.0, label, size, weight=500, fill=color, anchor="middle", ls=0.15)
    return w

def chip(x, y, w, label, sub=None, tag=None, fill="#FFFFFF", border=BORDER,
         h=CHIP_H, label_size=21, label_dy=None, sub_dy=None):
    rect(x, y, w, h, 10, fill, stroke=border, sw=1.0, shadow="shChip")
    ly = y + (label_dy if label_dy else (h / 2 + 0.36 * label_size if sub is None else h * 0.42))
    text(x + 22, ly, label, label_size, weight=500)
    if sub is not None:
        text(x + 22, y + (sub_dy if sub_dy else h * 0.69), sub, 13.5, weight=400, fill=MUTED)
    if tag:
        pw = tw(tag[0], 12.5, weight=500) + 24
        pill(x + w - 22 - pw, y + (h - 24) / 2, tag[0], tag[1], tag[2], tag[3] if len(tag) > 3 else None)
    return h

def package(x, y, w, h, title, sub, items, style="warm"):
    fill = WARM if style == "warm" else DB_FILL
    bord = BORDER if style == "warm" else DB_BORDER
    rect(x, y, w, h, 12, fill, stroke=bord, sw=1.0, shadow="shCard")
    rect(x + ADJ, y + 28, 4, 24, 2, INDIGO)
    text(x + ADJ + 18, y + 48, title, 24, weight=600, fill=INDIGO)
    text(x + ADJ, y + 74, sub, 14.5, weight=400, fill=MUTED)
    line(x + ADJ, y + HEAD - 18, x + w - ADJ, y + HEAD - 18,
         "#EAE3DA" if style == "warm" else "#DCEAE3", sw=1.0)
    cy = y + HEAD
    for it in items:
        label, s, tag = it[0], it[1], (it[2] if len(it) > 2 else None)
        chip(x + ADJ, cy, w - 2 * ADJ, label, s, tag)
        cy += CHIP_H + CHIP_GAP

# ---------------------------------------------------------------- 4 packages domaine
MODULE = ("«module»", TAG_FILL, TAG_INK)
ACTIONS = ("«actions»", "#FDF4E7", GOLD)

package(C1X, R1Y, C1W, RH, "Utilisateurs & Auth", "Comptes, sessions et adresses", [
    ("User", None), ("Session", None), ("Address", None),
    ("AuthLib", None, MODULE), ("AuthActions", None, ACTIONS),
])
package(C2X, R1Y, C2W, RH, "Catalogue", "Produits, marques et mouvements de stock", [
    ("Product", None), ("Brand", None), ("Concern", None), ("StockMovement", None),
    ("CatalogLib", None, MODULE),
])
package(C1X, R2Y, C1W, RH, "Expérience client", "Wishlist, fidélité et cartes cadeaux", [
    ("Wishlist", None), ("WishlistItem", None), ("WishlistShare", None),
    ("GiftCard", None), ("LoyaltyTransaction", None),
])
package(C2X, R2Y, C2W, RH, "Commandes", "Panier et cycle de vie de la commande", [
    ("Order", None), ("OrderItem", None), ("OrderEvent", None),
    ("CartLib", None, MODULE), ("OrdersLib", None, MODULE),
])

# ---------------------------------------------------------------- 5. Persistance
PX, PY, PW, PH = C3X, R1Y, C3W, R2Y + RH - R1Y          # 1560, 40, 800, 948
rect(PX, PY, PW, PH, 12, DB_FILL, stroke=DB_BORDER, sw=1.0, shadow="shCard")
rect(PX + ADJ, PY + 28, 4, 24, 2, INDIGO)
text(PX + ADJ + 18, PY + 48, "Persistance", 24, weight=600, fill=INDIGO)
text(PX + ADJ, PY + 74, "Drizzle ORM · PostgreSQL", 14.5, fill=MUTED)
line(PX + ADJ, PY + HEAD - 18, PX + PW - ADJ, PY + HEAD - 18, "#DCEAE3", sw=1.0)

pers = [
    ("Schema",     "Définition Drizzle des tables",          None),
    ("PostgreSQL", "Moteur relationnel — instance partagée", ("«singleton»", "#FDF4E7", GOLD)),
    ("Migrations", "Évolution versionnée du schéma",         None),
    ("OrderEvent", "Table des événements de commande",       None),
    ("OrderItem",  "Table des lignes de commande",           None),
]
NOTE_H, PCH, PGAP = 130, 110, 30.0
cy = PY + HEAD
for label, sub, tag in pers:
    chip(PX + ADJ, cy, PW - 2 * ADJ, label, sub, tag, border="#E2EDE8",
         h=PCH, label_size=20, label_dy=47, sub_dy=78)
    cy += PCH + PGAP

note_y = PY + PH - ADJ - NOTE_H
rect(PX + ADJ, note_y, PW - 2 * ADJ, NOTE_H, 10, "#F8FCFA", stroke="#E4EFE9", sw=1.0)
rect(PX + ADJ + 20, note_y + 30, 3, NOTE_H - 60, 1.5, GOLD, opacity=0.9)
text(PX + ADJ + 38, note_y + 56, "Une seule instance (singleton), partagée par les", 14.5, fill=CHIP_MUTE)
text(PX + ADJ + 38, note_y + 80, "modules métier — accès via Drizzle ORM.", 14.5, fill=CHIP_MUTE)
text(PX + ADJ + 38, note_y + 106, "OrderItem et OrderEvent sont vues comme tables", 13, fill=FAINT)

# ---------------------------------------------------------------- zone services
ZX, ZW = M, W - 2 * M
rect(ZX, ZONE_Y, ZW, ZONE_H, 12, "#FFFFFF", stroke=BORDER, sw=1.0, shadow="shCard")

SC_H = 92
sy = ZONE_Y + (ZONE_H - SC_H) / 2                       # 1135
text(ZX + 26, sy + 26, "Services Applicatifs", 24, weight=600, fill=INDIGO)
rect(ZX + 27, sy + 36, 3, 14, 1.5, INDIGO, opacity=0.75)
text(ZX + 39, sy + 48, "src/lib — modules métier", 14, fill=MUTED)
rect(ZX + 27, sy + 60, 3, 14, 1.5, GOLD, opacity=0.75)
text(ZX + 39, sy + 72, "src/actions — Server Actions", 14, fill=MUTED)

svc = [
    ("src/lib/auth.ts",      "Authentification et sessions",   INDIGO),
    ("src/actions/auth.ts",  "Connexion, inscription",         GOLD),
    ("src/lib/catalog.ts",   "Catalogue, stock et recherche",  INDIGO),
    ("src/actions/admin.ts", "Administration du catalogue",    GOLD),
    ("src/lib/orders.ts",    "Panier, commandes et paiement",  INDIGO),
]
sx0, sx1, sgap = 428.0, W - M - 26, 28.0
scw = (sx1 - sx0 - 4 * sgap) / 5
scx = [sx0 + i * (scw + sgap) for i in range(5)]
scc = [x + scw / 2 for x in scx]

# ---------------------------------------------------------------- connecteurs
X_AUTH, X_ACT_AUTH, X_CAT = 470, 530, 1150               # arrivées sur le bord inférieur
Y_CAT_R, Y_ORD_A, Y_ORD_B = 260, 700, 810                # arrivées sur le bord droit
X_ADM_CAT, X_ADM_ORD, X_ORD_R, X_ORD_DB = 1514, 1541, 2120, 2192

conn = [
    dict(pts=[(scc[0], sy), (scc[0], LL1), (LANE_L1, LL1), (LANE_L1, TOPA), (X_AUTH, TOPA), (X_AUTH, R1Y + RH)],
         arrow=("up", X_AUTH, R1Y + RH), start=(scc[0], sy)),
    dict(pts=[(scc[1], sy), (scc[1], LL2), (LANE_L2, LL2), (LANE_L2, TOPB), (X_ACT_AUTH, TOPB), (X_ACT_AUTH, R1Y + RH)],
         arrow=("up", X_ACT_AUTH, R1Y + RH), start=(scc[1], sy)),
    dict(pts=[(scc[2], sy), (scc[2], LL1), (LANE_R2, LL1), (LANE_R2, TOPA), (X_CAT, TOPA), (X_CAT, R1Y + RH)],
         arrow=("up", X_CAT, R1Y + RH), start=(scc[2], sy)),
    dict(pts=[(X_ADM_CAT, sy), (X_ADM_CAT, Y_CAT_R), (C2X + C2W, Y_CAT_R)],
         arrow=("left", C2X + C2W, Y_CAT_R), start=(X_ADM_CAT, sy)),
    dict(pts=[(X_ADM_ORD, sy), (X_ADM_ORD, Y_ORD_B), (C2X + C2W, Y_ORD_B)],
         arrow=("left", C2X + C2W, Y_ORD_B), start=(X_ADM_ORD, sy)),
    dict(pts=[(X_ORD_R, sy), (X_ORD_R, Y_ORD_A), (C2X + C2W, Y_ORD_A)],
         arrow=("left", C2X + C2W, Y_ORD_A), start=(X_ORD_R, sy)),
    dict(pts=[(X_ORD_DB, sy), (X_ORD_DB, PY + PH)], arrow=("up", X_ORD_DB, PY + PH), start=(X_ORD_DB, sy)),
]
for c in conn:
    rpath(c["pts"])

# ---------------------------------------------------------------- cartes de fichiers
for (path, desc, accent), x in zip(svc, scx):
    rect(x, sy, scw, SC_H, 10, "#FFFFFF", stroke=BORDER, sw=1.0, shadow="shChip")
    rect(x + 18, sy + 22, 3, SC_H - 44, 1.5, accent, opacity=0.85)
    text(x + 33, sy + 42, path, 18, family="JetBrains Mono", weight=400, fill=INK)
    text(x + 33, sy + 68, desc, 14, weight=400, fill=MUTED)

# ---------------------------------------------------------------- extrémités
for c in conn:
    px_, py_ = c["start"]
    circle(px_, py_, 3.4, INDIGO, opacity=0.45)
    kind, ax, ay = c["arrow"]
    (arrow_up if kind == "up" else arrow_left)(ax, ay)

# ---------------------------------------------------------------- légende
lg_y = ZONE_Y + ZONE_H - 20
line(ZX + 26, lg_y - 5, ZX + 58, lg_y - 5, INDIGO, sw=SW, dash="7 5", opacity=0.55)
arrow_left(ZX + 26, lg_y - 5)
text(ZX + 70, lg_y, "dépendance — le service applicatif utilise le domaine", 13, fill=FAINT)

svg.extend(out)
svg.append("</svg>")
# le master SVG est écrit dans le dossier parent (01_GLOBAL/)
master = os.path.join(os.path.dirname(HERE), "01_classes_global.svg")
open(master, "w", encoding="utf-8").write("\n".join(svg))
print(f"master SVG : {master}  ({W} x {H})")
