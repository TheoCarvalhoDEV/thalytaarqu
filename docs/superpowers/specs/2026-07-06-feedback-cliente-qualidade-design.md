# Design — Rodada de feedback da cliente + qualidade de assets e animações

**Data:** 2026-07-06
**Projeto:** Site institucional Thalyta Maia · Arquitetura e Interiores (one-page estática, GitHub Pages)
**Origem:** Vídeo + áudios de feedback da cliente (transcritos em anotações internas) e pedido do analista: "arrume, melhore a qualidade das imagens, logos e vídeos, melhore as animações".

## Contexto

O site é uma one-page estática (HTML/CSS/JS vanilla, sem build) publicada via GitHub Pages em `https://theocarvalhodev.github.io/thalytaarqu/`. Nesta sessão já foram entregues: logo oficial no menu (marca horizontal clara/escura com crossfade), selo oval no hero e rodapé, e preview social (Open Graph + Twitter Card).

Feedback da cliente (resumo): menu aprovado; logo no topo ✅ (feito); fotos profissionais virão em julho; Essência possivelmente vira "Sobre Mim" (a analisar); Serviços aprovado visualmente, mas com ideia posterior de remoção (a considerar); Projetos precisa reorganizar/alinhar imagens e agrupar Comercial × Residencial; Bastidores aprovado.

## Decisões tomadas (com o analista, 2026-07-06)

| Tema | Decisão |
|---|---|
| Seção Serviços | **Manter.** Aprovada no vídeo; remoção foi só ideia "a considerar". Remover depois é fácil. |
| Essência | **Rascunho "Sobre Mim"** em primeira pessoa como proposta para a cliente aprovar. Menu e id `#essencia` não mudam (estrutura do menu foi aprovada integralmente). |
| Organização dos Projetos | **Grupos fixos em sequência** (Residenciais → Comerciais), sem abas de filtro. Leitura literal da fala da cliente. |
| Animações | **Refinar + micro-interações**, mantendo a linguagem atual (Ken Burns, letra-a-letra, cortina, reveals, parallax). |
| Abordagem técnica | **A — edição direta + scripts reutilizáveis em `tools/`** (sem pipeline de build). Scripts pagam o investimento em julho com as fotos novas. |

## Seção 1 — Projetos em grupos fixos

- Cabeçalho da seção inalterado ("Portfólio / Conheça alguns dos nossos projetos").
- Dois subtítulos de grupo (`<h3 class="projetos__group-title">`) no estilo da marca (serifada + filete `--terra`):
  - **RESIDENCIAIS:** 1. Quarto Infantil (destaque — único elogiado nominalmente), 2. Cozinha Gourmet, 3. Quarto de Casal, 4. Lavabo & Toucador, 5. Banheiro Terrazzo.
  - **COMERCIAIS:** 6. Loja Marias Kids, 7. Lounge & Recepção (mantém menção "veja em movimento logo abaixo" — Atmosfera segue após a seção), 8. Escritório Orion.
- Zigue-zague (foto esquerda/direita) **reiniciado a cada grupo** — resolve o "reorganizar e alinhar imagens com textos".
- Kickers padronizados: `Categoria · Tipo` (ex.: `Residencial · Interiores`, `Comercial · Reforma`).
- Sem JS novo; grupos entram no sistema de reveal existente.

## Seção 2 — Essência → "Sobre Mim" (rascunho)

- Kicker: `O escritório` → `A arquiteta`. Título "ESSÊNCIA | TM" e retrato mantidos.
- Texto convertido para primeira pessoa, **sem fatos inventados** (usa apenas: CAU A305121-8, atendimento presencial/online Brasil, filosofia dos textos atuais).
- Comentário `<!-- RASCUNHO — aguardando aprovação da Thalyta -->` no HTML.

Texto aprovado pelo analista:

> Sou Thalyta Maia, arquiteta e urbanista (CAU A305121-8). Acredito que a arquitetura vai além das formas e estruturas: cada projeto é uma oportunidade de refletir a essência de quem o vivencia, criando ambientes que acolhem e inspiram. Trabalho com sensibilidade, buscando entender as necessidades e a personalidade de cada cliente para transformar espaços em lugares únicos e cheios de significado.
>
> Para mim, arquitetura é mais do que construir — é criar conexões e emoções. Cada detalhe é pensado para proporcionar uma experiência que ressoe com quem vai habitar o espaço. Atendo de forma presencial e online em todo o Brasil, com carinho e dedicação, criando espaços que conectam com a sua essência, onde quer que você esteja.

## Seção 3 — Qualidade de assets + limpeza técnica

### Vídeos (~93 MB → ~15-20 MB)
- Recompressão dos 6 reels + vídeo ambiente com `ffmpeg-static` (npm; sem instalação no sistema): H.264 CRF 23, lado maior limitado a 1920px (reels verticais → 1080×1920; vídeo ambiente horizontal → 1920 de largura), áudio AAC mantido (reels têm botão de som), `+faststart`.
- Script reutilizável: `tools/compress-videos.mjs`.

### Imagens (WebP + tamanhos responsivos)
- **Slides do hero:** converter de `background-image` para `<img>` com `object-fit: cover` + `srcset` WebP (1920/1280/768). Ken Burns/parallax continuam animando o wrapper. Slide 1 com `preload`/`fetchpriority=high`; slides 2–4 lazy.
- **Fotos de projeto:** `<picture>` com WebP em 2 larguras (~800/1200); ex.: `lounge-verde.jpg` 891 KB → ~120 KB.
- **Retrato e pattern:** WebP direto (suporte universal).
- **Imagem OG permanece JPEG** (compatibilidade com scrapers sociais).
- Script reutilizável: `tools/optimize-images.py` (base PIL) — reuso em julho com as fotos profissionais.

### Logos
- PNGs atuais já nítidos (fonte 3–5× o tamanho exibido) — sem ação obrigatória.
- **Tentativa time-boxed:** extrair **SVG vetorial** dos PDFs da identidade visual (`LOGOTIPO PDF/`). Se monocromático e fiel, o logo do menu passa a herdar cor via CSS (elimina crossfade de 2 imagens). Fallback: manter PNGs.

### Limpeza técnica
1. **Consolidar lightbox:** `main.js` tem duas implementações concorrentes (`initGallery` com IDs `#lbImg/#lbTitle/#lbStage` e `initLightbox` com `#lightboxImg/#lightboxCaption`) ligando cliques nas mesmas imagens. Inspecionar o HTML, manter **uma só** (a mais completa: galeria por projeto, swipe, teclado, gestão de foco) com os IDs corretos, remover a outra.
2. **`.gitignore`:** `COMUNICACAO_VISUAL/`, vídeo de feedback `20260706-*.mp4` (53 MB), `melhorias.txt` (anotações internas de cliente — não publicar em repo público).
3. **Remover 8 PNGs órfãos** (~4,1 MB, confirmado sem referências): `home-a/b`, `quarto-a/b`, `sala-a/b`, `loja-a/b`.
4. **Favicon** a partir do selo oficial (`.ico` multi-tamanho + `apple-touch-icon` 180px + tags no `<head>`).

## Seção 4 — Animações refinadas + micro-interações

Tudo CSS puro, sem JS novo (exceto stagger do drawer se CSS não bastar), respeitando o bloco `prefers-reduced-motion` existente:

1. Fotos de projeto: zoom lento no hover (`scale 1.05`, ~1.2s) + leve clareada + ícone discreto de "ampliar" (affordance do lightbox).
2. Cards de Serviço: elevação `translateY(-4px)` + número (01–04) ganhando cor `--terra` no hover.
3. Lightbox: abertura com fade do backdrop + imagem `scale .96 → 1`; fechamento suave.
4. Drawer mobile: links em cascata (stagger ~60ms) na abertura.
5. Subtítulos dos grupos: reveal com filete crescendo da esquerda (linguagem do `rule-left`).
6. Botões: preenchimento mais suave + micro-deslocamento do ícone no hover.

**Não muda:** Ken Burns, letra-a-letra, cortina de intro, parallax.

## Fora de escopo (registrado para o futuro)

- Substituição das fotos por fotos profissionais (cliente fotografa em julho; scripts de `tools/` prontos para isso).
- Remoção da seção Serviços (decisão pendente da cliente).
- Abas de filtro nos Projetos (descartado nesta rodada em favor de grupos fixos).
- Descrições emotivas/conceituais dos projetos (a cliente disse que ela mesma escreverá).
- Depoimentos, formulário de contato, JSON-LD (backlog de melhorias).

## Critérios de sucesso e verificação

1. Projetos agrupados Residenciais → Comerciais com zigue-zague alinhado por grupo (screenshot desktop + mobile).
2. Sobre Mim em primeira pessoa, marcado como rascunho no código.
3. `assets/videos/` total ≤ 25 MB com reprodução OK (verificação manual de 2 reels no navegador).
4. Imagens do hero e projetos servidas em WebP responsivo; página inicial sem regressão visual (screenshots antes/depois).
5. Um único lightbox funcional (abrir, navegar, teclado, swipe, fechar).
6. Favicon visível na aba; `.gitignore` cobrindo os arquivos internos; PNGs órfãos removidos.
7. Micro-interações visíveis em hover (fotos, cards, botões) e drawer com cascata; com `prefers-reduced-motion` ativo, nada disso anima.
8. Lighthouse (ou equivalente) sem regressão de performance — meta: melhora perceptível no peso total transferido.
