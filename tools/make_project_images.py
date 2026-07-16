"""
Gera mockups de UI (PNG) para os cards de projeto, na paleta Arcane.
Cada imagem simula uma tela real do produto: dashboard, pipeline, chat, trading, agenda.
Saida: assets/images/projects/<nome>.png  (800x450, 16:9)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "images", "projects"))
os.makedirs(OUT, exist_ok=True)

FONT_DIR = "C:/Windows/Fonts"
F_REG = os.path.join(FONT_DIR, "segoeui.ttf")
F_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")
F_LIGHT = os.path.join(FONT_DIR, "segoeuil.ttf")

# Paleta Arcane
NAVY = (6, 26, 43)
NAVY2 = (7, 40, 68)
BLUE = (18, 63, 110)
BLUE7 = (30, 93, 145)
SKY = (120, 195, 245)
SKY_SOFT = (199, 221, 240)
WHITE = (255, 255, 255)
MUTED = (150, 170, 188)
CARD = (13, 38, 64)
LINE = (40, 70, 100)
GREEN = (35, 185, 121)
RED = (226, 87, 76)
AMBER = (245, 163, 50)


def font(size, bold=False, light=False):
    path = F_LIGHT if light else (F_BOLD if bold else F_REG)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def text(d, pos, s, f, fill, anchor="la"):
    d.text(pos, s, font=f, fill=fill, anchor=anchor)


def dot(d, pos, color, r=4):
    d.ellipse([pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r], fill=color)


def header_bar(d, W, title, accent=SKY):
    rounded(d, [0, 0, W, 56], 0, NAVY2)
    dot(d, (28, 28), RED, 5)
    dot(d, (46, 28), AMBER, 5)
    dot(d, (64, 28), GREEN, 5)
    text(d, (90, 28), title, font(18, bold=True), WHITE, anchor="lm")
    rounded(d, [W - 150, 16, W - 24, 40], 8, BLUE7)
    text(d, (W - 87, 28), "Arcane", font(13, bold=True), WHITE, anchor="mm")


def sidebar(d, x0, y0, y1, items, active=0):
    rounded(d, [x0, y0, x0 + 150, y1], 0, CARD)
    cy = y0 + 80
    for i, it in enumerate(items):
        if i == active:
            rounded(d, [x0 + 12, cy - 14, x0 + 138, cy + 14], 8, BLUE7)
            text(d, (x0 + 28, cy), it, font(14, bold=True), WHITE, anchor="lm")
        else:
            text(d, (x0 + 28, cy), it, font(14), MUTED, anchor="lm")
        cy += 40


def make_jiu(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "Equipe Jiu — Painel")
    sidebar(d, 0, 56, H, ["Início", "Alunos", "Aulas", "Presenças", "Graduações"], active=1)
    # cartoes de alunos
    cx = 180
    for i in range(3):
        rounded(d, [cx, 80, cx + 180, 170], 12, CARD)
        dot(d, (cx + 34, 110), SKY, 18)
        text(d, (cx + 64, 100), f"Aluno {i+1}", font(14, bold=True), WHITE, anchor="lm")
        text(d, (cx + 64, 122), "Faixa azul", font(12), MUTED, anchor="lm")
        cx += 200
    # tabela de presencas
    rounded(d, [180, 200, W - 24, H - 24], 12, CARD)
    text(d, (200, 220), "Presenças da semana", font(14, bold=True), SKY_SOFT, anchor="lm")
    for r in range(4):
        y = 260 + r * 38
        for c in range(7):
            x = 210 + c * 78
            dot(d, (x, y), GREEN if (r + c) % 3 else LINE, 9)
    return img


def make_aws(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "ETL Pipeline — AWS")
    # nos do pipeline
    nodes = ["API", "Lambda", "S3", "RDS"]
    x = 70
    for i, n in enumerate(nodes):
        rounded(d, [x, 120, x + 120, 180], 12, BLUE7 if i % 2 == 0 else BLUE)
        text(d, (x + 60, 150), n, font(16, bold=True), WHITE, anchor="mm")
        if i < 3:
            d.line([x + 120, 150, x + 170, 150], fill=AMBER, width=3)
            text(d, (x + 145, 138), "→", font(18, bold=True), AMBER, anchor="mm")
        x += 170
    # grafico de barras (throughput)
    rounded(d, [70, 230, W - 70, H - 24], 12, CARD)
    text(d, (90, 250), "Throughput (registros/s)", font(13, bold=True), SKY_SOFT, anchor="lm")
    bars = [40, 70, 55, 90, 75, 110, 95]
    bw = (W - 200) / len(bars)
    for i, b in enumerate(bars):
        bx = 100 + i * bw
        rounded(d, [bx, H - 50 - b * 1.6, bx + bw - 14, H - 50], 6, SKY)
    return img


def make_gcp(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "GCP Serverless ETL")
    # nuvem
    rounded(d, [70, 90, 230, 150], 18, BLUE7)
    text(d, (150, 120), "Cloud", font(16, bold=True), WHITE, anchor="mm")
    text(d, (150, 142), "Functions", font(13), SKY_SOFT, anchor="mm")
    d.line([230, 120, 320, 120], fill=AMBER, width=3)
    rounded(d, [320, 95, 470, 150], 12, BLUE)
    text(d, (395, 122), "BigQuery", font(15, bold=True), WHITE, anchor="mm")
    # tabela estilo Looker
    rounded(d, [70, 190, W - 70, H - 24], 12, CARD)
    cols = ["data", "canal", "valor", "status"]
    cw = (W - 160) / len(cols)
    for i, c in enumerate(cols):
        text(d, (100 + i * cw, 210), c, font(13, bold=True), SKY, anchor="lm")
    for r in range(4):
        y = 245 + r * 36
        d.line([80, y - 14, W - 80, y - 14], fill=LINE, width=1)
        vals = [f"2026-07-{r+1:02d}", "web", f"R$ {1200+r*340}", "ok" if r % 2 == 0 else "proc"]
        for i, v in enumerate(vals):
            color = GREEN if (i == 3 and r % 2 == 0) else (AMBER if i == 3 else MUTED)
            text(d, (100 + i * cw, y), v, font(12), color, anchor="lm")
    return img


def make_arcane(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "Arcane Tecnologia")
    # hero institucional
    rounded(d, [40, 90, W - 40, 230], 16, NAVY2)
    text(d, (70, 130), "Sistemas + Sites + Automação", font(22, bold=True), WHITE, anchor="lm")
    text(d, (70, 165), "Transformamos operações em produtos digitais.", font(14), SKY_SOFT, anchor="lm")
    rounded(d, [70, 195, 230, 222], 8, BLUE7)
    text(d, (150, 208), "Falar no WhatsApp", font(13, bold=True), WHITE, anchor="mm")
    # grade de servicos
    labels = ["Sistemas", "Sites", "Automação", "IA"]
    x = 40
    for i, l in enumerate(labels):
        rounded(d, [x, 260, x + 170, 320], 12, CARD)
        text(d, (x + 85, 290), l, font(14, bold=True), SKY, anchor="mm")
        x += 185
    return img


def make_chatbot(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "SaaS Chatbot — Omnichannel")
    # coluna de canais
    chans = ["WhatsApp", "Instagram", "Web", "E-mail"]
    y = 80
    for i, c in enumerate(chans):
        rounded(d, [20, y, 200, y + 44], 10, CARD)
        dot(d, (44, y + 22), GREEN if i == 0 else SKY, 7)
        text(d, (64, y + 22), c, font(13, bold=True), WHITE, anchor="lm")
        y += 54
    # janela de conversa
    rounded(d, [230, 80, W - 24, H - 24], 12, CARD)
    bubbles = [("Cliente", 270, False), ("Bot", 340, True), ("Cliente", 410, False), ("Bot", 470, True)]
    for who, by, bot in bubbles:
        if bot:
            rounded(d, [250, by, 560, by + 40], 12, BLUE7)
            text(d, (268, by + 20), "Resposta automática gerada por IA", font(12), WHITE, anchor="lm")
        else:
            rounded(d, [W - 290, by, W - 44, by + 40], 12, (20, 50, 80))
            text(d, (W - 272, by + 20), "Olá, quero um orçamento", font(12), SKY_SOFT, anchor="lm")
    return img


def make_crypto(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "Crypto Trading — Live")
    # ticker
    pairs = [("BTC", "64.2k", GREEN), ("ETH", "3.4k", RED), ("SOL", "148", GREEN)]
    x = 30
    for sym, val, col in pairs:
        rounded(d, [x, 80, x + 150, 140], 12, CARD)
        text(d, (x + 18, 100), sym, font(16, bold=True), WHITE, anchor="lm")
        text(d, (x + 18, 124), val, font(18, bold=True), col, anchor="lm")
        x += 165
    # grafico de candlesticks
    rounded(d, [30, 160, W - 30, H - 24], 12, CARD)
    cx = 60
    for i in range(14):
        up = i % 2 == 0
        col = GREEN if up else RED
        top = 200 + (i * 13) % 90
        bot = top + 30 + (i * 7) % 40
        d.rectangle([cx, top, cx + 14, bot], fill=col)
        d.line([cx + 7, top - 12, cx + 7, bot + 12], fill=col, width=2)
        cx += 52
    return img


def make_barber(W, H):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    header_bar(d, W, "SaaS Barberflow — Agenda")
    # calendario lateral
    hours = ["09:00", "10:00", "11:00", "14:00", "15:00"]
    y = 80
    for h in hours:
        text(d, (30, y + 14), h, font(12), MUTED, anchor="lm")
        y += 56
    # colunas de profissionais
    pros = ["João", "Maria", "Pedro"]
    x = 110
    for p in pros:
        rounded(d, [x, 76, x + 200, 110], 10, BLUE7)
        text(d, (x + 100, 93), p, font(14, bold=True), WHITE, anchor="mm")
        # agendamentos
        jobs = [("Corte", 130, GREEN), ("Barba", 200, SKY), ("Corte+Barba", 270, AMBER)]
        for name, jy, col in jobs:
            rounded(d, [x + 8, jy, x + 192, jy + 44], 8, CARD)
            dot(d, (x + 24, jy + 22), col, 6)
            text(d, (x + 40, jy + 22), name, font(12, bold=True), WHITE, anchor="lm")
        x += 215
    return img


JOBS = {
    "equipe-jiu": make_jiu,
    "etl-aws": make_aws,
    "etl-gcp": make_gcp,
    "site-arcane": make_arcane,
    "saas-chatbot": make_chatbot,
    "crypto-trading": make_crypto,
    "saas-barberflow": make_barber,
}

if __name__ == "__main__":
    W, H = 800, 450
    for name, fn in JOBS.items():
        out = os.path.join(OUT, f"{name}.png")
        fn(W, H).save(out)
        print("OK", out)
