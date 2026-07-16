"""
Gera um vídeo 'code rain' na paleta azul Arcane para usar como fundo do hero.
Saida: assets/video/hero-code-rain.mp4 (loopavel, ~12s, 1280x720, sem audio).

Como funciona:
- Colunas de caracteres caem em ritmos diferentes (estilo matrix, porem em azul).
- A cabeca da coluna e mais clara; a cauda desvanece.
- Um leve vignette/gradiente mantem o texto do hero legivel por cima.
- O ultimo frame casa com o primeiro para dar loop perfeito.
"""

import numpy as np
import imageio.v2 as imageio
import os

# --- Parametros -------------------------------------------------------------
W, H = 1280, 720
FPS = 30
DURATION = 12.0
N_FRAMES = int(FPS * DURATION)
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "video")
OUT_PATH = os.path.abspath(os.path.join(OUT_DIR, "hero-code-rain.mp4"))

# Paleta Arcane (RGB)
BG_TOP = np.array([6, 26, 43])      # #061A2B
BG_BOTTOM = np.array([7, 40, 68])   # #072844
HEAD = np.array([190, 225, 250])    # quase branco azulado (cabeca brilhante)
BRIGHT = np.array([120, 195, 245])  # #79C3F5 (azul claro)
MID = np.array([43, 110, 166])      # #2B6EA6 (azul medio)
DIM = np.array([18, 63, 110])       # #123F6E (azul escuro)

GLYPH = "01<>{}[]#$%&*+=/\\|ABCDEF0123456789アイウエオカキクケコサシスセソタチツテト".encode("utf-8")
FONT_PATH = None  # None = usa bitmap interno (sem dependencia de fonte)

# Grade de caracteres (blocos de ~20px)
CELL = 20
COLS = W // CELL
ROWS = H // CELL

rng = np.random.default_rng(7)

# Cada coluna tem posicao (em linhas, float) e velocidade
col_y = rng.uniform(-ROWS, ROWS, COLS)
col_speed = rng.uniform(2.2, 5.5, COLS)          # linhas por segundo
col_glyph = rng.integers(0, 256, (COLS, ROWS))   # mapa de glyph por celula
# offset de fase para o loop: a posicao precisa voltar ao inicio apos DURATION
# escolhemos velocidades multiplas de (ROWS / DURATION) para fechar o ciclo
base = ROWS / DURATION
col_speed = (rng.integers(1, 4, COLS).astype(float)) * base / rng.choice([1.0, 1.0, 1.0])  # 1x..3x
col_speed = np.maximum(col_speed, base * 0.6)


def glyph_at(col, row, frame):
    """Glyph pseudo-aleatorio que muda lentamente para dar vida a coluna."""
    idx = (col_glyph[col, row] + frame // 4) % 256
    return idx


def build_frame(frame_idx):
    t = frame_idx / FPS
    # Fundo: gradiente vertical
    yy = np.linspace(0, 1, H)[:, None, None]
    bg = (BG_TOP + (BG_BOTTOM - BG_TOP) * yy).astype(np.float32)
    bg = np.broadcast_to(bg, (H, W, 3)).copy()

    # Camada de chuva
    layer = np.zeros((H, W, 3), dtype=np.float32)
    for c in range(COLS):
        y = (col_y[c] + col_speed[c] * t) % (ROWS + 8) - 4
        head_row = int(round(y))
        # desenha cabeca + cauda (algumas celulas acima)
        for k in range(14):
            r = head_row - k
            if 0 <= r < ROWS:
                cx = c * CELL
                cy = r * CELL
                # intensidade decrescente na cauda
                fade = (1.0 - k / 14.0) ** 1.6
                if k == 0:
                    color = HEAD * 1.0
                    alpha = 0.95
                elif k <= 2:
                    color = BRIGHT
                    alpha = 0.85 * fade
                elif k <= 6:
                    color = MID
                    alpha = 0.55 * fade
                else:
                    color = DIM
                    alpha = 0.30 * fade
                # bloco de celula (com leve padding)
                block = layer[cy + 2:cy + CELL - 2, cx + 2:cx + CELL - 2]
                if block.size:
                    block[..., :] = block[..., :] * (1 - alpha) + color * alpha

    # Compoe fundo + chuva
    img = bg + layer
    # Vignette para legibilidade do texto do hero (mais escuro nas bordas)
    xs = np.linspace(-1, 1, W)[None, :]
    ys = np.linspace(-1, 1, H)[:, None]
    vig = 1 - 0.45 * (xs ** 2 * 0.7 + ys ** 2)
    vig = np.clip(vig, 0, 1)[:, :, None]
    img = img * vig

    # Leve escurecimento geral para nao competir com o conteudo
    img = img * 0.82
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    writer = imageio.get_writer(
        OUT_PATH,
        fps=FPS,
        codec="libx264",
        quality=7,
        macro_block_size=1,
        ffmpeg_params=["-an"],
    )
    for i in range(N_FRAMES):
        writer.append_data(build_frame(i))
    writer.close()
    size = os.path.getsize(OUT_PATH)
    print(f"OK -> {OUT_PATH} ({size/1024:.0f} KB, {N_FRAMES} frames, {DURATION}s)")


if __name__ == "__main__":
    main()
