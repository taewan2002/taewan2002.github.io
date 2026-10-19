#!/usr/bin/env python3
"""Draw restrained, original technical figures for the Pearl essay."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/blog/pearl"
INK, MUTED, RULE = "#202124", "#666a70", "#c7c9cd"


class Figure:
    def __init__(self, w, h, title, description):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" lang="en">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L8 4L0 8" fill="#202124"/></marker></defs>',
            '<style>text{font-family:Arial,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}.math{font-family:"Times New Roman",serif;font-style:italic}.code{font-family:Menlo,Consolas,monospace}</style>',
            f'<rect width="{w}" height="{h}" fill="#fff"/>',
        ]

    def rect(self, x, y, w, h, fill="none", stroke=RULE, dash=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"'+(' stroke-dasharray="4 4"' if dash else '')+'/>')

    def text(self, x, y, text, size=16, color=INK, anchor="start", kind="", weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" class="{kind}">{escape(text)}</text>')

    def line(self, d, arrow=True, dash=False, color=INK):
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.15"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="4 4"' if dash else '')+'/>')

    def matrix(self, cx, y, n=4, cell=10):
        """An unfilled matrix grid; no arbitrary values or heatmap encodings."""
        x, size = cx - n*cell/2, n*cell
        for i in range(1, n):
            self.line(f'M{x+i*cell} {y} V{y+size}', False, color=RULE)
            self.line(f'M{x} {y+i*cell} H{x+size}', False, color=RULE)
        self.line(f'M{x+4} {y} H{x-3} V{y+size} H{x+4}', False)
        self.line(f'M{x+size-4} {y} H{x+size+3} V{y+size} H{x+size-4}', False)

    def save(self, filename):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / filename).write_text("\n".join(self.parts + ["</svg>\n"]), encoding="utf-8")


def pouw(mobile=False):
    w, h = (360, 590) if mobile else (760, 550)
    f = Figure(w, h, "Matrix multiplication: useful output and proof-of-work transcript", "Add low-rank noise E and F to input matrices A and B. Record partial sums in a prescribed order while computing C prime. Remove noise to recover AB; hash the transcript to check the mining target. If the target is met, submit a proof and block for other nodes to verify.")
    centers = (100, 260) if mobile else (250, 510)
    middle = w/2
    f.text(middle, 26, "Input matrices + low-rank noise", 14, MUTED, "middle")
    for cx, label in zip(centers, ("A + E", "B + F")):
        f.matrix(cx, 48)
        f.text(cx, 110, label, 20, anchor="middle", kind="math")
        f.line(f'M{cx} 120 V140 H{middle} V157')
    x, bw = (20, 320) if mobile else (150, 460)
    f.rect(x, 160, bw, 143, stroke=INK)
    f.text(middle, 187, "C′ = (A + E)(B + F)", 18, anchor="middle", kind="math")
    stages = (75, 180, 285) if mobile else (220, 380, 540)
    for cx, label in zip(stages, ("S₁", "S₂", "C′")):
        f.matrix(cx, 211, n=3, cell=11)
        f.text(cx, 268, label, 18, anchor="middle", kind="math")
    f.line(f'M{stages[0]+24} 228 H{stages[1]-26}')
    f.line(f'M{stages[1]+24} 228 H{stages[2]-26}')
    # Ellipsis is placed on an opaque background so it interrupts the flow line.
    f.rect((stages[1]+stages[2])/2-12, 218, 24, 20, fill="#fff", stroke="none")
    f.text((stages[1]+stages[2])/2, 233, "···", 18, anchor="middle")
    f.text(middle, 290, "GEMM · partial sums in a fixed order", 12, MUTED, "middle")
    left, right = (98, 262) if mobile else (210, 550)
    for cx in (left, right):
        f.line(f'M{cx} 303 V350')
    f.text(left+12, 334, "Final value", 12, MUTED)
    f.text(right+12, 334, "Partial sums", 12, MUTED)
    if mobile:
        f.text(left, 376, "Remove noise", 15, anchor="middle")
        f.text(left, 407, "AB", 25, anchor="middle", kind="math")
        f.line(f'M{left} 420 V451')
        f.text(left, 477, "Next operation", 14, anchor="middle")
    else:
        f.text(left, 378, "Recover the useful output", 16, anchor="middle")
        f.text(left, 411, "AB = C′ − AF − E(B + F)", 18, anchor="middle", kind="math")
        f.line(f'M{left} 426 V458')
        f.text(left, 484, "Use in the next operation", 15, anchor="middle")
    f.text(right, 376, "transcript", 17, anchor="middle", kind="code")
    f.text(right, 405, "H(transcript) < target", 13 if mobile else 16, anchor="middle", kind="math")
    f.line(f'M{right} 417 V449')
    f.text(right+12, 438, "If met", 12, MUTED)
    f.text(right, 474, "Submit proof + block", 15, anchor="middle")
    f.line(f'M{right} 485 V512')
    f.text(right, 535, "Other nodes verify", 14, anchor="middle")
    if mobile:
        f.text(20, 574, "Integer construction; commitments and details omitted.", 11, MUTED)
    f.save("pouw-process-mobile.svg" if mobile else "pouw-process.svg")


def kernel_panel(f, x, y, w, fused=False):
    f.text(x, y+18, "(b) Fused kernel" if fused else "(a) Separate kernels", 17, weight=600)
    f.text(x, y+36, "Integer GEMM path" if fused else "Hypothetical comparison", 11, MUTED)
    f.rect(x, y+47, w, 54, fill="#f6f6f6", stroke=INK)
    f.text(x+w/2, y+70, "Off-chip memory", 14, anchor="middle")
    f.text(x+w/2, y+90, "HBM / GDDR", 12, MUTED, "middle", "code")
    f.rect(x, y+209, w, 201, dash=True)
    f.text(x+w/2, y+231, "On-chip · SM", 12, MUTED, "middle")
    if not fused:
        a, b = x+60, x+w-68
        f.rect(x+15, y+268, 110, 80, stroke=INK)
        f.text(x+70, y+294, "GEMM", 17, anchor="middle", kind="code")
        f.text(x+70, y+318, "Partial sum Sₖ", 14, anchor="middle")
        f.text(x+70, y+338, "kernel 1", 11, MUTED, "middle", "code")
        f.rect(x+w-125, y+268, 110, 80, stroke=INK)
        f.text(x+w-70, y+294, "Accumulate", 14, anchor="middle")
        f.text(x+w-70, y+318, "transcript", 12, anchor="middle", kind="code")
        f.text(x+w-70, y+338, "kernel 2", 11, MUTED, "middle", "code")
        f.line(f'M{a-25} {y+101} V{y+268}')
        f.text(a-17, y+157, "Input", 12, MUTED)
        f.line(f'M{a+39} {y+268} V{y+101}', dash=True)
        f.text(a+48, y+190, "Write", 12)
        f.line(f'M{b} {y+101} V{y+268}', dash=True)
        f.text(b+9, y+157, "Read", 12)
        f.text(x+w/2, y+380, "Extra round trip for partial sums", 14, anchor="middle")
    else:
        f.line(f'M{x+37} {y+101} V{y+263}')
        f.text(x+49, y+153, "TMA · load input tiles", 12, MUTED)
        f.line(f'M{x+w-34} {y+264} V{y+101}')
        f.text(x+w-46, y+190, "Store output + transcript", 12, MUTED, "end")
        f.rect(x+15, y+251, w-30, 137, stroke=INK)
        f.text(x+30, y+274, "shared memory → WGMMA", 12, kind="code")
        f.text(x+30, y+305, "Accumulator Sₖ", 13)
        f.line(f'M{x+130} {y+300} H{x+w-101}')
        f.text(x+w-90, y+305, "Accumulate", 14)
        f.text(x+30, y+331, "registers", 11, MUTED, kind="code")
        f.text(x+w-90, y+331, "transcript", 11, MUTED, kind="code")
        f.line(f'M{x+w-60} {y+342} V{y+360} H{x+66} V{y+342}')
        f.text(x+30, y+378, "Next K tile · same kernel mainloop", 12, MUTED)
    f.text(x, y+436, "Input and final output transfers remain." if fused else "Dashed arrows: extra intermediate transfers.", 12, MUTED)


def fused_kernel(mobile=False):
    f = Figure(360 if mobile else 760, 955 if mobile else 485, "Memory paths with separate and fused kernels", "The separate-kernel panel is hypothetical: write GEMM partial sums to off-chip memory and read them in a recording kernel. The fused mainloop updates the transcript from register accumulators, avoiding that extra round trip. Input loads and final output and transcript stores remain. The full proof pipeline is omitted.")
    kernel_panel(f, 22, 17, 316 if mobile else 336)
    kernel_panel(f, 22 if mobile else 402, 499 if mobile else 17, 316 if mobile else 336, True)
    f.save("fused-kernel-mobile.svg" if mobile else "fused-kernel.svg")


if __name__ == "__main__":
    for narrow in (False, True):
        pouw(narrow)
        fused_kernel(narrow)
    print(f"Drew 4 SVG figures in {OUT}")
