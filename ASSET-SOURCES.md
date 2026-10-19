# Asset sources

The layout is independently implemented in HTML/CSS. The monochrome palette, large sans-serif headings, restrained navigation, and generous spacing take inspiration from the official [SpaceX](https://www.spacex.com/), [Tesla](https://www.tesla.com/), and [Palantir](https://www.palantir.com/) websites. No assets or source code from those sites are used. The original publication list was inspired by [Jon Barron's academic website](https://jonbarron.info/).

| Asset | Source and attribution |
| --- | --- |
| `assets/human-researcher.png` | Existing Human Researcher banner, copied unchanged from the author's local repository `docs/assets/human-researcher-hero.png`. Project: https://github.com/taewan2002/human-researcher. |
| `assets/portrait.jpg` | Taewan Cho's public GitHub profile image, downloaded unchanged from https://avatars.githubusercontent.com/u/89565530?v=4. |
| `assets/plaid-labs.svg` | Official Plaid Labs navigation wordmark, copied unchanged from https://plaidlabs.ai/images/layout/gnb-logo.svg. Retained from the earlier site design. |
| `assets/plaid-labs-white.png` | White Plaid Labs wordmark with symbol and blue accents (1339 × 174 transparent PNG), supplied by Taewan Cho on October 18, 2026 and copied unchanged. Used in the home-page company section and Company page. |
| `assets/nuvion-logo.png` | NUVION logo supplied by Taewan Cho (368 × 368 PNG), copied unchanged. Displayed beside the NUVION product description. |
| `assets/opscale-logo.png` | OPSCALE logo supplied by Taewan Cho (368 × 368 PNG), copied unchanged. Displayed beside the OPSCALE product description. |
| `assets/retovla.png` | Figure 1 of RetoVLA, Jiyeon Koo, Taewan Cho, et al. Original image from https://arxiv.org/html/2509.21243v2/fig1.png; paper: https://arxiv.org/abs/2509.21243. |
| `assets/spaceclip.png` | Figure 2 of SPACE-CLIP, Taewan Cho, Taeryang Kim, Andrew Jaeyong Choi. Original image from https://arxiv.org/html/2601.17657v3/fig2.png; paper: https://arxiv.org/abs/2601.17657. |
| `assets/edgezsad.png` | Figure 2 of EdgeZSAD, Taewan Cho and Andrew Jaeyong Choi. Image extracted without content changes from page 2 of https://arxiv.org/pdf/2606.16119; paper: https://arxiv.org/abs/2606.16119. |
| `assets/impact-agent.png` | Original Figure 2, extracted unchanged from page 3 of the author's manuscript `IMPAC_Agent.pdf`. Taewan Cho, Hyunwoo You, and Andrew Jaeyong Choi; published paper: https://doi.org/10.1109/ACCESS.2026.3674148. |
| `assets/model-merging.jpg` | Original Figure 1, extracted unchanged from page 2 of the published paper `1-s2.0-S0952197625016884-main.pdf`. Taewan Cho, Rina Kim, and Andrew Jaeyong Choi: https://doi.org/10.1016/j.engappai.2025.111686. |
| `assets/spaceclipv2.png` | Author-supplied SPACE-CLIPv2 figure (5096 × 3438), copied unchanged from the attachment provided by Taewan Cho. Shows the detailed Local Token Aggregation module and full depth-decoding architecture. Hyun Song, Taewan Cho, Kangmin Kim, and Andrew Jaeyong Choi. Author order and ACCV 2026 acceptance confirmed by Taewan Cho; public paper: https://arxiv.org/abs/2610.05029. |
| `assets/spacecraft-berthing.png` | Original Figure 2, copied unchanged from `figure2.png` in the author's manuscript source. Jiyeon Koo, Taewan Cho, Chansoo Son, and Andrew Jaeyong Choi; preprint: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6999268. |
| `assets/apisat2025.png` | Author-supplied space robotic arm depth-fusion figure (1274 × 824 PNG), copied unchanged from Taewan Cho's attachment for the APISAT 2025 entry. |
| `assets/geobridge-vla.png` | Author-supplied GeoBridge-VLA architecture figure (1026 × 316 PNG), copied unchanged from Taewan Cho's attachment on September 29, 2026. Hyun Song, Kangmin Kim, Loren Jinsoo Um, Minhui Han, Jaehyeok Park, Taewan Cho, and Andrew Jaeyong Choi. Public paper: https://arxiv.org/abs/2610.05026. |
| `assets/ai-flight-safety.png` | W-shaped AI/ML assurance process figure supplied by Taewan Cho (1888 × 858 PNG), copied unchanged from the October 4, 2026 attachment for the aircraft software flight safety verification paper: https://doi.org/10.5139/JKSAS.2025.53.6.665. |

All ten publication thumbnails are actual figures from the corresponding papers or supplied by the author. No generated or redrawn conceptual figures are used as publication thumbnails. Paper figures remain attributed to their respective authors. The site owner is a coauthor of the displayed papers; no blanket license over the paper figures is asserted by this website.

## Original blog diagrams

`assets/blog/pearl/pouw-process.svg`, `fused-kernel.svg`, and their `-mobile.svg` companions are original conceptual illustrations drawn for the October 18, 2026 personal essay. Editable drawing source: `scripts/draw_blog_figures.py`. No upstream artwork is copied. The PoUW figure follows the basic construction in [Ilan Komargodski and Omri Weinstein](https://arxiv.org/html/2504.09971v4#S2), with Pearl's proof submission stage shown conceptually. The fused-kernel figure follows the [public integer GEMM mainloop](https://github.com/pearl-research-labs/pearl/blob/master/miner/pearl-gemm/csrc/gemm/collective_mainloop.hpp). The separate-kernel panel is an explanatory hypothetical, not a historical Pearl implementation. These diagrams do not claim zero overhead, universal FP8 compatibility, or verification of a full inference request. Figure captions identify the scope and sources; the mobile variants preserve the same relationships in a vertical layout.

Company copy also draws on the owner-supplied `plaid-labs-A4-trifold-print.pdf` (revision `2026-10-12-v21`, pages 1–2), including QAIPI 2026 APAC selection, NUVION's inspection approach, Qualcomm-based on-device implementation, and the assess → validate → build workflow. The PDF itself and its device image are not included in the public site. Official company source URLs and the source-document revision are recorded in `content/company.json`.
