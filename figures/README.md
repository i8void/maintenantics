# Figures

All figures in `on_ai_agentic_reliability.md` are committed as PNGs in this
directory so the paper renders with **pandoc** (which does not execute Mermaid
code blocks). The paper references them as plain Markdown images with pandoc
width attributes, e.g. `![](figures/fig03_layers.png){ width=40% }`.

## Two sources

| Kind | Source | Regenerate with |
|------|--------|-----------------|
| Structural diagrams (`figNN_*.png`) | Mermaid in `mermaid/*.mmd` | `./render_mermaid.sh` (needs `mmdc` + Chromium) |
| Quantitative plots (`fig_*.png`) | `make_figures.py` | `python3 make_figures.py` (needs `matplotlib`, `numpy`) |

The plot palette is the validated colorblind-safe reference palette (blue /
orange / aqua / yellow series, single-hue blue sequential ramps), with distinct
line styles as a secondary encoding.

## Building the paper to PDF

Unicode symbols (λ, τ, β, α, ×, ·, §) in the prose require a Unicode engine:

```bash
pandoc on_ai_agentic_reliability.md --pdf-engine=xelatex -o paper.pdf
```
