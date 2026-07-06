# Feedback da Cliente + Qualidade de Assets — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar a rodada de feedback da cliente (projetos agrupados, "Sobre Mim"), consertar o lightbox/reels quebrados, otimizar vídeos/imagens/logos e refinar micro-interações.

**Architecture:** One-page estática (HTML/CSS/JS vanilla, GitHub Pages) editada diretamente, sem pipeline de build. Scripts reutilizáveis de otimização ficam em `tools/` (Node p/ vídeo via `ffmpeg-static`; Python/PIL p/ imagens). Verificação via Playwright headless (instalado no scratchpad da sessão).

**Tech Stack:** HTML5, CSS3, JS vanilla (ES5-style existente), Python 3.14 + Pillow 12, Node 24 + ffmpeg-static, Playwright (verificação).

**Spec:** `docs/superpowers/specs/2026-07-06-feedback-cliente-qualidade-design.md`

## Global Constraints

- Sem pipeline de build; site continua estático puro (abrir `index.html` funciona).
- Todos os textos em pt-BR; tom da marca (elegante, acolhedor).
- IDs de seção e itens do menu NÃO mudam (`#essencia`, `#servicos`, `#projetos`, `#bastidores`, `#contato`) — estrutura aprovada pela cliente.
- Seção Serviços é MANTIDA (decisão registrada no spec).
- URLs de assets relativas (site é servido em `/thalytaarqu/` no GitHub Pages).
- `assets/images/og-thalyta-maia.jpg` permanece JPEG (scrapers sociais).
- Toda animação nova deve ser coberta pelo bloco `@media (prefers-reduced-motion: reduce)` existente em `css/animations.css` (regra global `*` já cobre transitions/animations — não criar animação via JS timer).
- Verificações Playwright: rodar com `cwd` = `C:/Users/assis/AppData/Local/Temp/claude/c--Users-assis-Desktop-thalytaarqu/7e601e33-8dd5-41a6-a595-97dc870dae86/scratchpad` (é onde o pacote `playwright` está instalado; usar `channel: 'chrome'`).
- Commits pequenos por tarefa, mensagens em pt-BR no padrão dos commits existentes (`fix:`, `feat:`, `melhoria:`, `docs:`), terminando com `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` (usar `-m` múltiplos no PowerShell; NUNCA here-string `@'...'@` seguido de `;` na mesma linha).

## Estado atual relevante (medido em 2026-07-06)

- **Bug ativo:** `js/main.js` tem 2 lightboxes: `initGallery()` (main.js:221-319, IDs `#lbImg/#lbTitle/#lbCount/#lbStage/#lbClose/#lbPrev/#lbNext` — **não existem no HTML**) e `initLightbox()` (main.js:368-446, IDs `#lightboxImg/...` — existem). `initGallery` roda primeiro em `init()`, lança `TypeError` (`btnClose.addEventListener` com null) e **mata `initVideos()`/`initLightbox()`**. Resultado confirmado no navegador: lightbox não abre, reels não tocam.
- **CSS duplicado:** `css/styles.css` tem 2 blocos `.lightbox`: linhas ~554-632 (estilo do `initGallery`: `.is-open`, `.lightbox__stage/__cap/__title/__count/__btn`, animação fade+scale pronta) e ~731-865 (estilo do `initLightbox`: `.is-active`, `.lightbox__content/__caption` + media query "Ajustes responsivos para o lightbox"). O segundo sobrescreve o primeiro.
- **Micro-interações já existentes** (ficam, não recriar): zoom hover nas fotos (styles.css:361-365), overlay+ícone ampliar (styles.css:533-552), hover dos cards de serviço (styles.css:314-320), fill dos botões (styles.css:447-465).
- **Working tree sujo** (trabalho da sessão ainda não commitado): logos no nav/hero/rodapé, OG tags, `assets/images/logo-thalyta-*.png`, `og-thalyta-maia.jpg`, deleção de `Thalyta Maia.html`.
- **Órfãos confirmados** (nenhuma referência em HTML/JS/CSS): `assets/images/{home-a,home-b,quarto-a,quarto-b,sala-a,sala-b,loja-a,loja-b}.png` (~4,1 MB).
- **Vídeos:** todos verticais 720×1280+ (posters 720×1280). `assets/videos/*.mp4` = ~93 MB.
- **Dimensões das imagens** (para srcset):
  - Hero: `hero-cozinha` 1440², `hero-lavabo` 1440×1800, `hero-lounge` 1920², `hero-quarto` 1280².
  - Projetos (pinterest): `cozinha-marmore` 1440², `cozinha-office` 1440², `quarto-infantil-floral` 1440², `bercario` 1440², `lavabo-toucador` 1440×1800, `quarto-casal` 1280², `banheiro-terrazzo` 900×1600, `lounge-verde` 4096², `marias-kids-fachada` 1440×1040, `marias-kids-logo` 707×942, `escritorio-orion` 720×960.
  - `portrait.jpg` 686×1200; `pattern.png` 799×791.

---

### Task 0: Higiene do repositório + commit do trabalho pendente da sessão

**Files:**
- Create: `.gitignore`
- Delete: `assets/images/home-a.png`, `home-b.png`, `quarto-a.png`, `quarto-b.png`, `sala-a.png`, `sala-b.png`, `loja-a.png`, `loja-b.png`
- Commit: mudanças pendentes já no working tree (`index.html`, `css/styles.css`, `css/animations.css`, novos `assets/images/logo-thalyta-*.png`, `assets/images/og-thalyta-maia.jpg`, deleção de `Thalyta Maia.html`)

**Interfaces:**
- Produces: working tree limpo para as tasks seguintes; `.gitignore` impedindo que `COMUNICACAO_VISUAL/`, o vídeo de feedback e `tools/node_modules/` entrem no repo.

- [ ] **Step 1: Criar `.gitignore`**

```gitignore
# Material interno de cliente — não publicar
COMUNICACAO_VISUAL/
melhorias.txt
20260706-*.mp4

# Dependências de ferramentas locais
tools/node_modules/

# SO / editor
Thumbs.db
Desktop.ini
```

- [ ] **Step 2: Verificar que os ignorados sumiram do `git status`**

Run: `git status --short`
Expected: sem linhas `?? COMUNICACAO_VISUAL/`, `?? melhorias.txt`, `?? 20260706-...mp4`; aparecem `?? .gitignore`, `?? assets/images/logo-...` etc.

- [ ] **Step 3: Commit do trabalho da sessão (logos + OG)**

```powershell
git add index.html css/styles.css css/animations.css assets/images/logo-thalyta-claro.png assets/images/logo-thalyta-escuro.png assets/images/logo-thalyta-selo-claro.png assets/images/og-thalyta-maia.jpg .gitignore
git add "Thalyta Maia.html"
git commit -m 'feat: logo oficial no menu/hero/rodape + preview social (Open Graph)' -m 'Marca horizontal com crossfade claro/escuro no nav, selo oval no hero e rodape, imagem OG 1200x630 e meta tags para WhatsApp/Facebook/Twitter. Adiciona .gitignore para material interno de cliente.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

Expected: commit criado; `git status --short` mostra working tree limpo (exceto arquivos ignorados).

- [ ] **Step 4: Remover PNGs órfãos e commitar**

```powershell
git rm assets/images/home-a.png assets/images/home-b.png assets/images/quarto-a.png assets/images/quarto-b.png assets/images/sala-a.png assets/images/sala-b.png assets/images/loja-a.png assets/images/loja-b.png
git commit -m 'chore: remove 8 PNGs orfaos sem referencia (~4MB)' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

Expected: 8 deleções; `git log --oneline -1` mostra o commit.

---

### Task 1: Restaurar lightbox e reels (bug crítico)

**Files:**
- Modify: `index.html` (bloco `<div class="lightbox" id="lightbox">`, linhas ~520-535)
- Modify: `js/main.js` (remover `initLightbox` ~368-446 e sua chamada em `init()` ~459)
- Modify: `css/styles.css` (remover o 2º bloco `.lightbox`, ~731-865)

**Interfaces:**
- Consumes: markup/CSS/JS existentes.
- Produces: um único lightbox funcional usando `initGallery` (galeria por projeto, swipe, teclado, foco). IDs canônicos: `#lbClose`, `#lbPrev`, `#lbNext`, `#lbStage`, `#lbImg`, `#lbTitle`, `#lbCount`. Classes: `.lightbox.is-open`, `body.lb-lock`.

- [ ] **Step 1: Escrever a verificação e confirmar que FALHA (vermelho)**

Criar `<scratchpad>/verify-lightbox.mjs` (scratchpad = caminho nas Global Constraints):

```js
import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
const url = pathToFileURL('c:/Users/assis/Desktop/thalytaarqu/index.html').href;
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 820 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
await page.goto(url, { waitUntil: 'load' });
await page.waitForTimeout(1500);
await page.evaluate(() => document.querySelector('#projetos').scrollIntoView());
await page.waitForTimeout(600);
await page.locator('.frame').first().click({ force: true });
await page.waitForTimeout(600);
const lb = await page.evaluate(() => ({
  open: document.getElementById('lightbox').classList.contains('is-open'),
  src: (document.getElementById('lbImg') || {}).src || '(sem #lbImg)',
  title: (document.getElementById('lbTitle') || {}).textContent || '(sem #lbTitle)'
}));
// navegar e fechar
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(400);
await page.keyboard.press('Escape');
await page.waitForTimeout(400);
const closed = await page.evaluate(() => !document.getElementById('lightbox').classList.contains('is-open'));
// reel toca?
await page.evaluate(() => document.querySelector('#bastidores').scrollIntoView());
await page.waitForTimeout(600);
await page.locator('.reel__play').first().click({ force: true });
await page.waitForTimeout(1200);
const reel = await page.evaluate(() => !document.querySelector('.reel video').paused);
console.log(JSON.stringify({ pageErrors: errors, lightbox: lb, closedAfterEsc: closed, reelPlays: reel }, null, 2));
const ok = errors.length === 0 && lb.open && lb.src.includes('assets/') && closed && reel;
console.log(ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
```

Run (do scratchpad): `node verify-lightbox.mjs`
Expected: **FAIL** — `pageErrors` contém "Cannot read properties of null"; `lightbox.open: false`; `reelPlays: false`.

- [ ] **Step 2: Substituir o markup do lightbox no `index.html`**

Substituir o bloco inteiro `<!-- Lightbox / Galeria de Fotos Ampliada --> ... </div>` (de `<div class="lightbox" id="lightbox"` até o `</div>` correspondente, antes de `<script src="js/main.js">`) por:

```html
<!-- Lightbox / Galeria de fotos ampliada (initGallery em js/main.js) -->
<div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Visualizador de imagens">
  <button class="lightbox__btn lightbox__close" id="lbClose" aria-label="Fechar visualizador">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
  </button>
  <button class="lightbox__btn lightbox__nav lightbox__nav--prev" id="lbPrev" aria-label="Imagem anterior">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
  </button>
  <figure class="lightbox__stage" id="lbStage">
    <img src="" alt="" class="lightbox__img" id="lbImg">
    <figcaption class="lightbox__cap">
      <span class="lightbox__title" id="lbTitle"></span>
      <span class="lightbox__count" id="lbCount"></span>
    </figcaption>
  </figure>
  <button class="lightbox__btn lightbox__nav lightbox__nav--next" id="lbNext" aria-label="Próxima imagem">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>
  </button>
</div>
```

- [ ] **Step 3: Remover `initLightbox` do `js/main.js`**

1. Apagar o bloco inteiro de `/* ---------- LIGHTBOX (Galeria de Projetos) ---------- */` até o `}` que fecha `function initLightbox()` (imediatamente antes de `/* ---------- init ---------- */`).
2. Em `init()`, apagar a linha `initLightbox();`.

- [ ] **Step 4: Remover o 2º bloco CSS `.lightbox` do `css/styles.css`**

Ler `css/styles.css` a partir da linha ~700 até o fim da região. Apagar do segundo `.lightbox {` (o que contém `.lightbox.is-active`, `.lightbox__content`, `.lightbox__caption` — começa ~731, pode haver um comentário de seção imediatamente acima; apagar o comentário junto) até o fechamento da media query `/* Ajustes responsivos para o lightbox */ @media ... }` (~865). Conferir que o bloco anterior (`.lightbox` com `.is-open`, ~554-632) permanece intacto.

- [ ] **Step 5: Rodar a verificação (verde)**

Run: `node verify-lightbox.mjs`
Expected: **PASS** — `pageErrors: []`, `lightbox.open: true`, `src` contém `assets/`, `title` = "Cozinha Gourmet", `closedAfterEsc: true`, `reelPlays: true`.

- [ ] **Step 6: Commit**

```powershell
git add index.html js/main.js css/styles.css
git commit -m 'fix: restaura lightbox e reels (removia initLightbox duplicado que quebrava initGallery/initVideos)' -m 'HTML volta aos IDs do initGallery (lbImg/lbTitle/lbStage...), remove initLightbox e o 2o bloco CSS .lightbox. Lightbox com galeria por projeto, teclado, swipe e foco; reels voltam a tocar.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 2: Projetos em grupos fixos (Residenciais → Comerciais)

**Files:**
- Modify: `index.html` (seção `#projetos`, `<article class="project">` ~241-352)
- Modify: `css/styles.css` (novo estilo `.projetos__group-title` — inserir após o bloco `.projetos__head`/antes de `.projetos__list`)

**Interfaces:**
- Consumes: sistema de reveal existente (`data-reveal`, classe `.is-in` via JS).
- Produces: dois `<h3 class="projetos__group-title" data-reveal="up">` e 8 articles reordenados. Nenhum JS novo.

- [ ] **Step 1: Reordenar os articles e inserir títulos de grupo no `index.html`**

Dentro de `<div class="projetos__list">`, aplicar esta estrutura (mover os `<article>` existentes inteiros — não reescrever o conteúdo interno; apenas ajustar `class` do article e o texto do kicker conforme a tabela):

```html
<h3 class="projetos__group-title" data-reveal="up"><span>Residenciais</span></h3>
<!-- 1. Quarto Infantil, 2. Cozinha Gourmet, 3. Quarto de Casal, 4. Lavabo & Toucador, 5. Banheiro Terrazzo -->

<h3 class="projetos__group-title projetos__group-title--gap" data-reveal="up"><span>Comerciais</span></h3>
<!-- 6. Loja Marias Kids, 7. Lounge & Recepção, 8. Escritório Orion -->
```

Tabela de ordem/classes/kickers (zigue-zague reinicia em cada grupo — 1º projeto do grupo SEM `project--reverse`):

| # | Projeto | classe do `<article>` | kicker novo |
|---|---|---|---|
| 1 | Quarto Infantil | `project` | `Residencial · Interiores` |
| 2 | Cozinha Gourmet | `project project--reverse` | `Residencial · Interiores` |
| 3 | Quarto de Casal | `project` | `Residencial · Interiores` |
| 4 | Lavabo & Toucador | `project project--reverse` | `Residencial · Interiores` |
| 5 | Banheiro Terrazzo | `project` | `Residencial · Reforma + Interiores` |
| 6 | Loja Marias Kids | `project` | `Comercial · Reforma` |
| 7 | Lounge & Recepção | `project project--reverse` | `Comercial · Interiores` |
| 8 | Escritório Orion | `project` | `Comercial · Interiores` |

Atenção: nos articles movidos, os atributos `data-reveal="left|right"` de `.project__media`/`.project__text` devem casar com o lado: article normal → media `data-reveal="left"` + text `data-reveal="right"`; article `--reverse` → media `data-reveal="right"` + text `data-reveal="left"`. A frase "veja em movimento logo abaixo" fica no Lounge & Recepção (7) — Atmosfera continua logo após a seção, ok.

- [ ] **Step 2: CSS dos títulos de grupo (com filete que cresce no reveal)**

Inserir em `css/styles.css`, logo após as regras de `.projetos__head` (antes de `.projetos__list`):

```css
/* títulos de grupo do portfólio (Residenciais / Comerciais) */
.projetos__group-title {
  display: flex; align-items: center; gap: 18px;
  font-family: var(--ff-serif); font-weight: 400;
  font-size: clamp(20px, 2.2vw, 28px); letter-spacing: .22em;
  text-transform: uppercase; color: var(--terra);
  margin: clamp(48px, 7vh, 84px) 0 clamp(28px, 4vh, 44px);
}
.projetos__group-title:first-child { margin-top: 0; }
.projetos__group-title::after {
  content: ""; flex: 1; height: 1px; background: var(--terra); opacity: .45;
  transform: scaleX(0); transform-origin: left;
  transition: transform 1.1s var(--ease) .25s;
}
.projetos__group-title.is-in::after { transform: scaleX(1); }
```

(O `data-reveal="up"` cuida do fade/slide do texto; o `::after` cresce quando o JS adiciona `.is-in`. `prefers-reduced-motion` já zera transitions globalmente.)

- [ ] **Step 3: Verificar ordem no DOM + screenshot**

Criar `<scratchpad>/verify-grupos.mjs`:

```js
import { chromium } from 'playwright';
import { pathToFileURL } from 'url';
const url = pathToFileURL('c:/Users/assis/Desktop/thalytaarqu/index.html').href;
const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto(url, { waitUntil: 'load' });
const seq = await page.evaluate(() =>
  Array.from(document.querySelectorAll('.projetos__list .projetos__group-title span, .projetos__list .project__name'))
    .map(e => e.textContent.trim()));
console.log(JSON.stringify(seq, null, 1));
const want = ['Residenciais','Quarto Infantil','Cozinha Gourmet','Quarto de Casal','Lavabo & Toucador','Banheiro Terrazzo','Comerciais','Loja Marias Kids','Lounge & Recepção','Escritório Orion'];
const ok = JSON.stringify(seq) === JSON.stringify(want);
await page.evaluate(() => document.querySelector('#projetos').scrollIntoView());
await page.waitForTimeout(1200);
await page.screenshot({ path: 'grupos.png', clip: { x: 0, y: 0, width: 1280, height: 900 } });
console.log(ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
```

Run: `node verify-grupos.mjs` → Expected: PASS. Abrir `grupos.png` (Read) e conferir visualmente título "Residenciais" + filete + Quarto Infantil primeiro.

- [ ] **Step 4: Commit**

```powershell
git add index.html css/styles.css
git commit -m 'feat: projetos agrupados em Residenciais e Comerciais com kickers padronizados' -m 'Grupos fixos em sequencia (pedido da cliente), zigue-zague reiniciado por grupo, Quarto Infantil abre o grupo residencial. Titulos de grupo com filete animado no reveal.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 3: Essência → "Sobre Mim" (rascunho aprovado)

**Files:**
- Modify: `index.html` (seção `#essencia`, `<div class="essencia__text">` ~149-161)

**Interfaces:**
- Produces: texto em primeira pessoa (rascunho para aprovação da cliente). Título "ESSÊNCIA | TM", retrato e layout inalterados.

- [ ] **Step 1: Substituir kicker e parágrafos**

No `<div class="essencia__text">`: trocar `<div class="kicker kicker--tan" data-reveal="up">O escritório</div>` por `<div class="kicker kicker--tan" data-reveal="up">A arquiteta</div>` e substituir os dois `<p data-reveal="up" ...>` existentes por:

```html
        <!-- RASCUNHO "Sobre Mim" — aguardando aprovação da Thalyta (2026-07-06) -->
        <p data-reveal="up" data-reveal-delay="120">Sou Thalyta Maia, arquiteta e urbanista (CAU A305121-8). Acredito
          que a arquitetura vai além das formas e estruturas: cada projeto é uma oportunidade de refletir a essência de
          quem o vivencia, criando ambientes que acolhem e inspiram. Trabalho com sensibilidade, buscando entender as
          necessidades e a personalidade de cada cliente para transformar espaços em lugares únicos e cheios de
          significado.</p>
        <p data-reveal="up" data-reveal-delay="180">Para mim, arquitetura é mais do que construir — é criar conexões e
          emoções. Cada detalhe é pensado para proporcionar uma experiência que ressoe com quem vai habitar o espaço.
          Atendo de forma presencial e online em todo o Brasil, com carinho e dedicação, criando espaços que conectam
          com a sua essência, onde quer que você esteja.</p>
```

- [ ] **Step 2: Verificar no navegador**

Run (scratchpad): `node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage();await p.goto('file:///c:/Users/assis/Desktop/thalytaarqu/index.html');const t=await p.textContent('.essencia__text');console.log(/Sou Thalyta Maia/.test(t)&&/A arquiteta/.test(await p.textContent('.essencia__text .kicker'))?'PASS':'FAIL');await b.close();})"`
Expected: `PASS`

- [ ] **Step 3: Commit**

```powershell
git add index.html
git commit -m 'feat: secao Essencia em primeira pessoa (rascunho Sobre Mim para aprovacao da cliente)' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 4: Script de otimização de imagens + geração de WebP

**Files:**
- Create: `tools/optimize-images.py`
- Create (gerados): `assets/images/webp/*.webp`

**Interfaces:**
- Produces: WebPs com convenção `assets/images/webp/<basename>-<largura>.webp` (ex.: `hero-cozinha-1280.webp`, `lounge-verde-1200.webp`, `pattern-799.webp`, `portrait-686.webp`). A Task 5 consome exatamente esses nomes. Reuso em julho: adicionar nomes novos ao `CONFIG` e rodar de novo.

- [ ] **Step 1: Escrever `tools/optimize-images.py`**

```python
#!/usr/bin/env python3
"""Gera versões WebP responsivas das imagens do site.

Uso:  python tools/optimize-images.py
Saída: assets/images/webp/<basename>-<largura>.webp
Idempotente: pula arquivos já gerados mais novos que a origem.
Em julho (fotos profissionais): adicionar as fotos novas ao CONFIG e rodar de novo.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "webp")

# (caminho relativo à raiz, [larguras alvo]) — larguras maiores que a origem são ignoradas
CONFIG = [
    ("assets/images/hero-cozinha.jpg",              [768, 1280, 1440]),
    ("assets/images/hero-lavabo.jpg",               [768, 1280, 1440]),
    ("assets/images/hero-lounge.jpg",               [768, 1280, 1920]),
    ("assets/images/hero-quarto.jpg",               [768, 1280]),
    ("assets/images/portrait.jpg",                  [686]),
    ("assets/images/pattern.png",                   [799]),
    ("assets/pinterest/cozinha-marmore.jpg",        [800, 1200]),
    ("assets/pinterest/cozinha-office.jpg",         [800, 1200]),
    ("assets/pinterest/quarto-infantil-floral.jpg", [800, 1200]),
    ("assets/pinterest/bercario.jpg",               [800, 1200]),
    ("assets/pinterest/lavabo-toucador.jpg",        [800, 1200]),
    ("assets/pinterest/quarto-casal.jpg",           [800, 1200]),
    ("assets/pinterest/banheiro-terrazzo.jpg",      [800]),
    ("assets/pinterest/lounge-verde.jpg",           [800, 1200]),
    ("assets/pinterest/marias-kids-fachada.jpg",    [800, 1200]),
    ("assets/pinterest/marias-kids-logo.jpg",       [707]),
    ("assets/pinterest/escritorio-orion.jpg",       [720]),
]
QUALITY = 80

def main():
    os.makedirs(OUT, exist_ok=True)
    total_in = total_out = 0
    for rel, widths in CONFIG:
        src = os.path.join(ROOT, rel)
        im = Image.open(src)
        base = os.path.splitext(os.path.basename(rel))[0]
        for w in widths:
            if w > im.width:
                continue
            dst = os.path.join(OUT, f"{base}-{w}.webp")
            if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
                print(f"  pulado (atual): {os.path.basename(dst)}")
                continue
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).convert("RGB").save(
                dst, "WEBP", quality=QUALITY, method=6)
            print(f"  {rel} -> {os.path.basename(dst)}  {os.path.getsize(dst)//1024}KB")
        total_in += os.path.getsize(src)
    for f in os.listdir(OUT):
        total_out += os.path.getsize(os.path.join(OUT, f))
    print(f"\norigem: {total_in//1024}KB | webp gerados (total): {total_out//1024}KB")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar e conferir**

Run: `python tools/optimize-images.py`
Expected: ~35 arquivos em `assets/images/webp/`; total WebP < 40% do total de origem; sem exceções. Conferir visualmente 1 arquivo: `Read assets/images/webp/lounge-verde-1200.webp` (deve ser o lounge nítido).

- [ ] **Step 3: Commit**

```powershell
git add tools/optimize-images.py assets/images/webp
git commit -m 'feat: script reutilizavel de otimizacao de imagens + WebP responsivo gerado' -m 'Pronto para as fotos profissionais de julho: adicionar ao CONFIG e rodar.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 5: Servir WebP responsivo (hero `<picture>`, projetos, retrato, pattern)

**Files:**
- Modify: `index.html` (slides do hero ~99-105; 13 `<img>` de projeto/retrato; inline style do `.contato__media`)
- Modify: `css/styles.css` (novo `.hero__slide-img`; `.hero__slide` deixa de precisar de background)

**Interfaces:**
- Consumes: WebPs da Task 4 (`assets/images/webp/<basename>-<w>.webp`).
- Produces: hero como `<img>` reais (Ken Burns/parallax intactos — animam o wrapper `.hero__slide`/`#heroSlides`); fotos de projeto em `<picture>` com fallback JPEG original (lightbox continua lendo o `src` original em alta).

- [ ] **Step 1: Converter os 4 slides do hero**

Substituir os 4 `<div class="hero__slide" style="background-image:...">` por (padrão; slide 1 mostrado, demais análogos trocando o basename e SEM `is-active`/`fetchpriority`, COM `loading="lazy"`):

```html
      <div class="hero__slide is-active" data-pan="1">
        <picture>
          <source type="image/webp"
            srcset="assets/images/webp/hero-cozinha-768.webp 768w, assets/images/webp/hero-cozinha-1280.webp 1280w, assets/images/webp/hero-cozinha-1440.webp 1440w"
            sizes="100vw">
          <img class="hero__slide-img" src="assets/images/hero-cozinha.jpg" alt="" fetchpriority="high" decoding="async">
        </picture>
      </div>
      <div class="hero__slide" data-pan="2">
        <picture>
          <source type="image/webp"
            srcset="assets/images/webp/hero-lounge-768.webp 768w, assets/images/webp/hero-lounge-1280.webp 1280w, assets/images/webp/hero-lounge-1920.webp 1920w"
            sizes="100vw">
          <img class="hero__slide-img" src="assets/images/hero-lounge.jpg" alt="" loading="lazy" decoding="async">
        </picture>
      </div>
      <div class="hero__slide" data-pan="3">
        <picture>
          <source type="image/webp"
            srcset="assets/images/webp/hero-lavabo-768.webp 768w, assets/images/webp/hero-lavabo-1280.webp 1280w, assets/images/webp/hero-lavabo-1440.webp 1440w"
            sizes="100vw">
          <img class="hero__slide-img" src="assets/images/hero-lavabo.jpg" alt="" loading="lazy" decoding="async">
        </picture>
      </div>
      <div class="hero__slide" data-pan="4">
        <picture>
          <source type="image/webp"
            srcset="assets/images/webp/hero-quarto-768.webp 768w, assets/images/webp/hero-quarto-1280.webp 1280w"
            sizes="100vw">
          <img class="hero__slide-img" src="assets/images/hero-quarto.jpg" alt="" loading="lazy" decoding="async">
        </picture>
      </div>
```

- [ ] **Step 2: CSS do slide**

Em `css/styles.css`, após o bloco `.hero__slide { ... }` existente, adicionar (e remover `background-size/position/repeat` do `.hero__slide` se presentes — o transform do Ken Burns fica no wrapper):

```css
.hero__slide picture, .hero__slide-img {
  position: absolute; inset: 0; width: 100%; height: 100%;
}
.hero__slide-img { object-fit: cover; }
```

- [ ] **Step 3: Fotos de projeto em `<picture>`**

Envolver cada `<img>` dentro de `.frame` com `<picture>` + `<source>` WebP, mantendo o `<img>` original como fallback (atributos `alt`/`loading` preservados). `sizes="(max-width: 860px) 92vw, 44vw"` em todos. Lista completa dos `srcset`:

| imagem | srcset |
|---|---|
| cozinha-marmore | `webp/cozinha-marmore-800.webp 800w, webp/cozinha-marmore-1200.webp 1200w` |
| cozinha-office | `webp/cozinha-office-800.webp 800w, webp/cozinha-office-1200.webp 1200w` |
| quarto-infantil-floral | `webp/quarto-infantil-floral-800.webp 800w, webp/quarto-infantil-floral-1200.webp 1200w` |
| bercario | `webp/bercario-800.webp 800w, webp/bercario-1200.webp 1200w` |
| lavabo-toucador | `webp/lavabo-toucador-800.webp 800w, webp/lavabo-toucador-1200.webp 1200w` |
| quarto-casal | `webp/quarto-casal-800.webp 800w, webp/quarto-casal-1200.webp 1200w` |
| banheiro-terrazzo | `webp/banheiro-terrazzo-800.webp 800w` |
| lounge-verde | `webp/lounge-verde-800.webp 800w, webp/lounge-verde-1200.webp 1200w` |
| marias-kids-fachada | `webp/marias-kids-fachada-800.webp 800w, webp/marias-kids-fachada-1200.webp 1200w` |
| marias-kids-logo | `webp/marias-kids-logo-707.webp 707w` |
| escritorio-orion | `webp/escritorio-orion-720.webp 720w` |

(prefixo completo: `assets/images/`.) Exemplo completo (aplicar o mesmo padrão aos demais):

```html
<figure class="frame">
  <picture>
    <source type="image/webp"
      srcset="assets/images/webp/cozinha-marmore-800.webp 800w, assets/images/webp/cozinha-marmore-1200.webp 1200w"
      sizes="(max-width: 860px) 92vw, 44vw">
    <img src="assets/pinterest/cozinha-marmore.jpg" alt="Cozinha gourmet — vista geral" loading="lazy">
  </picture>
</figure>
```

Atenção: `initGallery` usa `frame.querySelector('img')` — continua funcionando com `<picture>` (o `<img>` está dentro). O lightbox amplia o JPEG original (alta qualidade) — comportamento desejado.

- [ ] **Step 4: Retrato e pattern**

- Retrato: envolver `<img src="assets/images/portrait.jpg" ...>` com `<picture>` + `<source type="image/webp" srcset="assets/images/webp/portrait-686.webp">`.
- Pattern: no `.contato__media`, trocar o inline style para `background-image:url('assets/images/webp/pattern-799.webp')`.

- [ ] **Step 5: Verificar WebP servido + visual**

Criar `<scratchpad>/verify-webp.mjs`:

```js
import { chromium } from 'playwright';
const { chromium: c } = await import('playwright');
const b = await c.launch({ channel: 'chrome' });
const p = await b.newPage({ viewport: { width: 1280, height: 820 } });
await p.goto('file:///c:/Users/assis/Desktop/thalytaarqu/index.html', { waitUntil: 'load' });
await p.waitForTimeout(1500);
const hero = await p.evaluate(() => document.querySelector('.hero__slide-img').currentSrc);
await p.evaluate(() => document.querySelector('#projetos').scrollIntoView());
await p.waitForTimeout(1200);
const proj = await p.evaluate(() => document.querySelector('.frame img').currentSrc);
console.log({ hero, proj });
await p.screenshot({ path: 'webp-hero.png' });
console.log(hero.includes('.webp') && proj.includes('.webp') ? 'PASS' : 'FAIL');
await b.close();
```

Run: `node verify-webp.mjs` → Expected: PASS (ambos `currentSrc` terminam em `.webp`). Conferir `webp-hero.png` — hero visualmente idêntico ao anterior (Ken Burns ativo).

- [ ] **Step 6: Commit**

```powershell
git add index.html css/styles.css
git commit -m 'melhoria: imagens servidas em WebP responsivo (hero como <picture>, projetos, retrato, pattern)' -m 'Hero deixa background-image e vira <img> com srcset; Ken Burns e parallax preservados no wrapper. Lightbox segue ampliando o JPEG original.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 6: Recompressão dos vídeos (93 MB → ≤25 MB)

**Files:**
- Create: `tools/package.json`, `tools/compress-videos.mjs`
- Modify (binários): `assets/videos/reel-0{1,2,3,5,6,7}.mp4`, `assets/videos/reel-04.mp4`

**Interfaces:**
- Produces: mesmos nomes de arquivo (HTML não muda). Todos os vídeos são verticais (720×1280+).

- [ ] **Step 1: Criar `tools/package.json` e instalar ffmpeg-static**

```json
{
  "name": "thalytaarqu-tools",
  "private": true,
  "type": "module",
  "dependencies": { "ffmpeg-static": "^5.2.0" }
}
```

Run: `cd tools; npm install` → Expected: `node_modules/ffmpeg-static` com binário (`node -e "console.log(require('ffmpeg-static'))"` imprime o caminho). (`tools/node_modules/` já está no `.gitignore`.)

- [ ] **Step 2: Escrever `tools/compress-videos.mjs`**

```js
// Recomprime os vídeos do site (H.264 CRF 23, lado maior <=1920, +faststart).
// Uso:  cd tools && npm install && node compress-videos.mjs
// Substitui o original apenas se o resultado ficar >=15% menor.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const ffmpeg = require('ffmpeg-static');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'assets', 'videos');

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.mp4'));
let before = 0, after = 0;
for (const f of files) {
  const src = path.join(DIR, f);
  const tmp = path.join(DIR, `tmp-${f}`);
  const inMB = fs.statSync(src).size / 1048576;
  before += inMB;
  execFileSync(ffmpeg, [
    '-y', '-i', src,
    '-c:v', 'libx264', '-crf', '23', '-preset', 'slow',
    '-vf', "scale=-2:'min(1920,ih)'",
    '-c:a', 'aac', '-b:a', '128k',
    '-movflags', '+faststart',
    tmp,
  ], { stdio: ['ignore', 'ignore', 'inherit'] });
  const outMB = fs.statSync(tmp).size / 1048576;
  if (outMB < inMB * 0.85) {
    fs.renameSync(tmp, src);
    after += outMB;
    console.log(`${f}: ${inMB.toFixed(1)}MB -> ${outMB.toFixed(1)}MB`);
  } else {
    fs.rmSync(tmp);
    after += inMB;
    console.log(`${f}: mantido (${inMB.toFixed(1)}MB; recompressao nao compensou)`);
  }
}
console.log(`\nTOTAL: ${before.toFixed(1)}MB -> ${after.toFixed(1)}MB`);
```

- [ ] **Step 3: Rodar (demora alguns minutos — usar run_in_background se >2min)**

Run: `cd tools; node compress-videos.mjs`
Expected: cada reel grande caindo para ~2–4 MB; `TOTAL: ~93MB -> <=25MB`. Se algum arquivo falhar, o erro do ffmpeg aparece no stderr — investigar antes de seguir.

- [ ] **Step 4: Verificar reprodução no navegador**

Re-rodar `node verify-lightbox.mjs` (do scratchpad) — a parte `reelPlays` deve continuar `PASS`. Adicionalmente conferir o vídeo ambiente: `node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage();await p.goto('file:///c:/Users/assis/Desktop/thalytaarqu/index.html');await p.evaluate(()=>document.querySelector('#atmosfera').scrollIntoView());await p.waitForTimeout(2500);console.log(await p.evaluate(()=>!document.getElementById('ambientVideo').paused)?'PASS':'FAIL');await b.close();})"`
Expected: `PASS` (autoplay mudo ao entrar na tela).

- [ ] **Step 5: Commit**

```powershell
git add tools/package.json tools/compress-videos.mjs assets/videos
git commit -m 'melhoria: reels recomprimidos (~93MB -> ~20MB) com script reutilizavel ffmpeg-static' -m 'H.264 CRF 23, +faststart, audio mantido. Qualidade visual preservada; carregamento no 4G muito mais rapido.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 7: Favicon a partir do selo oficial

**Files:**
- Create: `tools/make-favicon.py`, `favicon.ico` (raiz), `assets/images/apple-touch-icon.png`
- Modify: `index.html` (`<head>`)

**Interfaces:**
- Consumes: `COMUNICACAO_VISUAL/IDENTIDADE VISUAL THALYTA MAIA/MARCA D´ÁGUA/MARCA D´AGUA 3.png` (selo escuro — visível em abas claras).
- Produces: `favicon.ico` (16/32/48) e `apple-touch-icon.png` (180², fundo creme).

- [ ] **Step 1: Escrever `tools/make-favicon.py`**

```python
#!/usr/bin/env python3
"""Gera favicon.ico (16/32/48) e apple-touch-icon.png (180, fundo creme) do selo oficial."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "COMUNICACAO_VISUAL", "IDENTIDADE VISUAL THALYTA MAIA",
                   "MARCA D´ÁGUA", "MARCA D´AGUA 3.png")
CREAM = (246, 241, 233, 255)

im = Image.open(SRC).convert("RGBA")
# bbox do conteúdo (não transparente e não branco)
px, (w, h) = im.load(), im.size
xs, ys = [], []
for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b, a = px[x, y]
        if a > 20 and not (r > 245 and g > 245 and b > 245):
            xs.append(x); ys.append(y)
m = 14
box = (max(0, min(xs)-m), max(0, min(ys)-m), min(w, max(xs)+m), min(h, max(ys)+m))
seal = im.crop(box)
# quadrado com padding transparente
side = max(seal.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(seal, ((side-seal.width)//2, (side-seal.height)//2), seal)

sq.resize((48, 48), Image.LANCZOS).save(
    os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
touch = Image.new("RGBA", (side, side), CREAM)
touch.alpha_composite(sq)
touch.convert("RGB").resize((180, 180), Image.LANCZOS).save(
    os.path.join(ROOT, "assets", "images", "apple-touch-icon.png"))
print("ok: favicon.ico + apple-touch-icon.png")
```

- [ ] **Step 2: Rodar e conferir**

Run: `python tools/make-favicon.py` → Expected: `ok: ...`. Conferir com Read `assets/images/apple-touch-icon.png` (selo escuro centrado em fundo creme, legível).

- [ ] **Step 3: Tags no `<head>` do `index.html`** (após a linha do `canonical`):

```html
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
```

- [ ] **Step 4: Commit**

```powershell
git add tools/make-favicon.py favicon.ico assets/images/apple-touch-icon.png index.html
git commit -m 'feat: favicon e apple-touch-icon a partir do selo oficial' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 8: Logo vetorial SVG no menu (tentativa time-boxed; fallback = manter PNGs)

**Files:**
- Possibly create: `assets/images/logo-thalyta.svg`
- Possibly modify: `index.html` (nav), `css/styles.css` (`.nav__logo-img*`)

**Interfaces:**
- Consumes: `COMUNICACAO_VISUAL/IDENTIDADE VISUAL THALYTA MAIA/LOGOTIPO PDF/LOGOTIPO {1..4}.pdf` (vetoriais).
- Produces (se der certo): SVG monocromático inline ou via `<img>`; se inline com `fill: currentColor`, o crossfade de 2 PNGs do nav é substituído por herança de cor (`.nav__logo` já transiciona `color` entre `--cream` e `--brand`).
- **Gate de aceitação:** screenshot do nav (topo e sólido) visualmente fiel ao PNG atual. Se não ficar fiel em ~30 min de trabalho, REVERTER (git checkout) e registrar no summary que os PNGs ficam.

- [ ] **Step 1: Instalar pymupdf e inspecionar os PDFs**

Run: `pip install pymupdf` e depois:

```python
# <scratchpad>/inspect-pdfs.py
import fitz, os
base = r"c:/Users/assis/Desktop/thalytaarqu/COMUNICACAO_VISUAL/IDENTIDADE VISUAL THALYTA MAIA/LOGOTIPO PDF"
for n in os.listdir(base):
    if not n.endswith(".pdf"): continue
    doc = fitz.open(os.path.join(base, n))
    page = doc[0]
    pix = page.get_pixmap(dpi=72)
    out = os.path.join(os.path.dirname(__file__), n.replace(".pdf", ".png"))
    pix.save(out)
    print(n, page.rect, "->", out)
```

Read cada PNG gerado; identificar qual PDF é o **lockup horizontal** (monograma à esquerda + THALYTA MAIA — mesmo desenho de `logo-thalyta-claro.png`).

- [ ] **Step 2: Extrair SVG do PDF identificado**

```python
# <scratchpad>/extract-svg.py — trocar LOGOTIPO_X.pdf pelo identificado no Step 1
import fitz, re
doc = fitz.open(r"c:/Users/assis/Desktop/thalytaarqu/COMUNICACAO_VISUAL/IDENTIDADE VISUAL THALYTA MAIA/LOGOTIPO PDF/LOGOTIPO_X.pdf")
svg = doc[0].get_svg_image()
# cores presentes?
print(sorted(set(re.findall(r'(?:fill|stroke)="(#[0-9a-fA-F]{3,6})"', svg))))
open(r"c:/Users/assis/Desktop/thalytaarqu/assets/images/logo-thalyta.svg", "w", encoding="utf-8").write(svg)
print("bytes:", len(svg))
```

Critérios para prosseguir: (a) 1 única cor de fill/stroke (monocromático); (b) tamanho < 80 KB; (c) aberto no navegador, fiel ao logo. Se falhar qualquer um → **Step 5 (fallback)**.

- [ ] **Step 3: Monocromatizar para `currentColor` e embutir no nav**

No SVG: substituir todas as ocorrências da cor única por `currentColor`; adicionar `aria-hidden="true"` e remover width/height fixos (manter `viewBox`). Colar inline no `index.html` dentro de `<a class="nav__logo">`, substituindo as DUAS `<img class="nav__logo-img...">`. CSS: substituir as regras `.nav__logo-img*` por:

```css
.nav__logo svg { height: 46px; width: auto; display: block; }
@media (max-width: 860px) { .nav__logo svg { height: 40px; } }
@media (max-width: 400px) { .nav__logo svg { height: 34px; } }
```

(a cor herda de `.nav__logo { color: var(--cream) }` / `.nav--solid .nav__logo { color: var(--brand) }` — transição já existente.)

- [ ] **Step 4: Verificar crossfade visual**

Rodar screenshots do nav no topo e após scroll (mesma técnica de `verify-lightbox.mjs`, `clip {0,0,1280,110}`, com `window.scrollTo(0,700)` no segundo). Expected: logo creme no topo, logo marrom no sólido, sem distorção. Se fiel → commit; senão → Step 5.

- [ ] **Step 5 (fallback, só se necessário): reverter**

```powershell
git checkout -- index.html css/styles.css
Remove-Item assets/images/logo-thalyta.svg -ErrorAction SilentlyContinue
```

Registrar no summary: "SVG não ficou fiel; PNGs mantidos (já nítidos)."

- [ ] **Step 6: Commit (se deu certo)**

```powershell
git add index.html css/styles.css assets/images/logo-thalyta.svg
git commit -m 'melhoria: logo do menu em SVG vetorial com cor herdada via CSS' -m 'Substitui o crossfade de 2 PNGs; nitidez perfeita em qualquer densidade de tela.' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 9: Micro-interações restantes (drawer em cascata + ícone dos botões)

**Files:**
- Modify: `css/animations.css` (cascata do drawer)
- Modify: `css/styles.css` (nudge do ícone nos botões)

**Interfaces:**
- Consumes: classes existentes `.drawer.is-open`, `.drawer__links a`, `.btn`, `.btn svg`.
- Produces: só CSS; nenhuma mudança de HTML/JS. (Zoom de fotos, ícone de ampliar, hover de cards e fill de botões JÁ EXISTEM — não duplicar.)

- [ ] **Step 1: Cascata dos links do drawer** — adicionar ao final de `css/animations.css`, ANTES do bloco `@media (prefers-reduced-motion: reduce)`:

```css
/* =========================================================
   Drawer mobile — links em cascata na abertura
   ========================================================= */
.drawer .drawer__links a {
  opacity: 0; transform: translateX(18px);
  transition: opacity .5s var(--ease), transform .5s var(--ease),
              color .3s var(--ease), padding-left .3s var(--ease);
}
.drawer.is-open .drawer__links a { opacity: 1; transform: none; }
.drawer.is-open .drawer__links a:nth-child(1) { transition-delay: .10s; }
.drawer.is-open .drawer__links a:nth-child(2) { transition-delay: .16s; }
.drawer.is-open .drawer__links a:nth-child(3) { transition-delay: .22s; }
.drawer.is-open .drawer__links a:nth-child(4) { transition-delay: .28s; }
.drawer.is-open .drawer__links a:nth-child(5) { transition-delay: .34s; }
```

E DENTRO do bloco `@media (prefers-reduced-motion: reduce)` existente, adicionar:

```css
  .drawer .drawer__links a { opacity: 1 !important; transform: none !important; }
```

- [ ] **Step 2: Nudge do ícone nos botões** — em `css/styles.css`, junto às regras `.btn` (~447-465):

```css
.btn svg { transition: transform .35s var(--ease); }
.btn:hover svg { transform: translateX(2px) scale(1.05); }
```

- [ ] **Step 3: Verificar drawer no mobile**

Run (scratchpad): `node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:390,height:780}});await p.goto('file:///c:/Users/assis/Desktop/thalytaarqu/index.html');await p.waitForTimeout(1200);await p.click('#burger');await p.waitForTimeout(700);await p.screenshot({path:'drawer.png'});const op=await p.evaluate(()=>getComputedStyle(document.querySelector('.drawer__links a')).opacity);console.log(op==='1'?'PASS':'FAIL ('+op+')');await b.close();})"`
Expected: `PASS`; `drawer.png` mostra menu aberto com links visíveis.

- [ ] **Step 4: Commit**

```powershell
git add css/animations.css css/styles.css
git commit -m 'melhoria: micro-interacoes (links do drawer em cascata, icone dos botoes no hover)' -m 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>'
```

---

### Task 10: Verificação final integrada

**Files:**
- Nenhum (verificação); screenshots no scratchpad.

- [ ] **Step 1: Sweep completo**

Criar `<scratchpad>/verify-final.mjs` consolidando: (1) zero `pageerror` no load e após interações; (2) sequência de grupos/projetos correta (mesma asserção da Task 2); (3) texto "Sou Thalyta Maia" presente; (4) lightbox abre/navega/fecha; (5) reel toca; (6) `currentSrc` do hero e de um projeto terminam em `.webp`; (7) logo do nav troca claro→escuro no scroll (comparar `opacity` das `.nav__logo-img` OU cor computada do SVG conforme resultado da Task 8); (8) favicon linkado (`document.querySelector('link[rel=icon]')`). Screenshots full-page desktop (1280) e mobile (390) salvos como `final-desktop.png`/`final-mobile.png`.
Expected: `PASS` em todos os 8 pontos; inspecionar os 2 screenshots com Read.

- [ ] **Step 2: Pesos finais**

Run: `du -sh assets assets/videos assets/images assets/pinterest` (Bash)
Expected: `assets/videos` ≤ 25 MB; total `assets` ≤ ~40 MB (de 99 MB).

- [ ] **Step 3: Commit de eventuais ajustes + atualizar o plano com checkboxes marcados**

```powershell
git add -A
git status --short
```

Se houver sobras legítimas, commitar com mensagem descritiva; caso contrário, nada a fazer.

---

## Self-review (do plano, executado em 2026-07-06)

- **Cobertura do spec:** grupos fixos → T2; Sobre Mim → T3; vídeos → T6; imagens WebP/hero `<img>` → T4+T5; logos SVG → T8; lightbox único → T1; `.gitignore`/órfãos → T0; favicon → T7; micro-interações → T2 (filete) + T9 (drawer/botões) + T1 (reativa as existentes); critérios de sucesso → T10. Fora de escopo do spec respeitado (sem abas, Serviços intacto). ✓
- **Placeholders:** nenhum TBD; todos os código/comandos completos. `LOGOTIPO_X.pdf` na T8 é decidido pelo Step 1 da própria task (inspeção). ✓
- **Consistência de nomes:** `assets/images/webp/<basename>-<w>.webp` idêntico entre T4 (gera) e T5 (consome, tabela conferida contra o CONFIG); IDs `lb*` idênticos entre T1-HTML e `initGallery`; `.projetos__group-title` idêntico entre T2-HTML/CSS/verificação. ✓
