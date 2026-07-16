# Portfólio Rui Diniz Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir e validar um portfólio estático, responsivo e orientado à captação de projetos para a Arcane Tecnologia.

**Architecture:** Página única em HTML sem framework, com design tokens e componentes visuais em CSS e interações progressivas em JavaScript. Ativos locais evitam dependências de build e permitem deploy direto pelo GitHub Pages.

**Tech Stack:** HTML5, CSS3, JavaScript ES2022, Python 3 para validação local.

## Global Constraints

- Manter a oferta “Sistema + site + automação”.
- Usar WhatsApp `(12) 99133-2258` e e-mail `adm@arcanetecnologia.com.br`.
- Não inventar depoimentos, clientes ou resultados.
- Garantir navegação por teclado, contraste e `prefers-reduced-motion`.
- Funcionar como site estático no GitHub Pages sem etapa de build.

---

### Task 1: Ativos e identidade

**Files:**
- Create: `assets/images/arcane-mark.png`
- Create: `assets/images/hero-devices.png`
- Create: `assets/favicon.svg`

- [ ] Recortar a marca Arcane do arquivo horizontal e remover o fundo branco.
- [ ] Recortar o visual de dispositivos do conceito, mantendo o fundo tecnológico.
- [ ] Criar favicon vetorial alinhado à paleta.
- [ ] Conferir dimensões e transparência.

### Task 2: Estrutura semântica e conteúdo

**Files:**
- Create: `index.html`

- [ ] Criar metadados, Open Graph e JSON-LD.
- [ ] Implementar cabeçalho, hero, serviços, projetos, sobre, tecnologias, processo e contato.
- [ ] Usar links reais para GitHub, LinkedIn, Instagram, site e WhatsApp.
- [ ] Garantir headings, landmarks, alt text e skip link.

### Task 3: Sistema visual responsivo

**Files:**
- Create: `styles.css`

- [ ] Definir tokens de cor, tipografia, espaçamento, borda e sombra.
- [ ] Implementar layout desktop fiel ao conceito aprovado.
- [ ] Criar variações visuais para serviços e projetos sem cards genéricos repetitivos.
- [ ] Implementar breakpoints para tablet e celular.
- [ ] Adicionar estados de foco, hover e redução de movimento.

### Task 4: Interações progressivas

**Files:**
- Create: `script.js`

- [ ] Implementar menu móvel acessível.
- [ ] Atualizar ano do rodapé.
- [ ] Implementar destaque de navegação conforme seção visível.
- [ ] Implementar animações de entrada com IntersectionObserver.

### Task 5: Publicação e validação

**Files:**
- Create: `README.md`
- Create: `.nojekyll`
- Create: `tests/validate_site.py`

- [ ] Documentar execução local e GitHub Pages.
- [ ] Validar arquivos, âncoras, imagens, título, descrição e CTA.
- [ ] Servir localmente e verificar desktop e mobile no navegador.
- [ ] Corrigir divergências visuais e funcionais.
- [ ] Empacotar a entrega em ZIP.
