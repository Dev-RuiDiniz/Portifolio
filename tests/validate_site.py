from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.images: list[tuple[str, str | None]] = []
        self.title = ""
        self._in_title = False
        self.description = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"] or "")
        if tag == "a" and data.get("href"):
            self.links.append(data["href"] or "")
        if tag == "img" and data.get("src"):
            self.images.append((data["src"] or "", data.get("alt")))
        if tag == "title":
            self._in_title = True
        if tag == "meta" and data.get("name") == "description":
            self.description = data.get("content")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def local_path(url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme or url.startswith("#") or url.startswith("mailto:"):
        return None
    return ROOT / parsed.path


def main() -> None:
    required_files = ["index.html", "styles.css", "script.js", ".nojekyll"]
    for name in required_files:
        assert (ROOT / name).exists(), f"Arquivo obrigatório ausente: {name}"

    parser = SiteParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))

    assert "Rui Diniz" in parser.title, "O title deve identificar Rui Diniz"
    assert parser.description and len(parser.description) >= 80, "Meta description insuficiente"
    assert "https://wa.me/5512991332258" in "\n".join(parser.links), "CTA do WhatsApp não encontrado"
    assert "adm@arcanetecnologia.com.br" in (ROOT / "index.html").read_text(encoding="utf-8")

    for href in parser.links:
        if href.startswith("#"):
            anchor = href[1:]
            assert anchor in parser.ids, f"Âncora sem destino: {href}"
        path = local_path(href)
        if path:
            assert path.exists(), f"Link local quebrado: {href}"

    for src, alt in parser.images:
        path = local_path(src)
        if path:
            assert path.exists(), f"Imagem ausente: {src}"
        assert alt is not None, f"Imagem sem atributo alt: {src}"

    print(f"OK: {len(parser.ids)} IDs, {len(parser.links)} links e {len(parser.images)} imagens validados.")


if __name__ == "__main__":
    main()
