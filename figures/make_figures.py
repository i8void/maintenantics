#!/usr/bin/env python3
"""Generate variable-sensitivity figures for the reliability paper.
Palette from the dataviz skill's validated reference instance (light surface)."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)

# --- palette (validated, light surface) ---
SURFACE   = "#fcfcfb"
INK       = "#0b0b0b"
INK2      = "#52514e"
MUTED     = "#898781"
GRID      = "#e1e0d9"
AXIS      = "#c3c2b7"
SERIES    = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
GOOD      = "#0ca30c"
CRIT      = "#d03b3b"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#256abf", "#184f95", "#0d366b"]
SEQ = LinearSegmentedColormap.from_list("brandblue", BLUE_RAMP)

mpl.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.family": "sans-serif", "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.edgecolor": AXIS, "axes.linewidth": 1.0,
    "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.grid": True, "axes.axisbelow": True,
    "savefig.dpi": 150, "savefig.bbox": "tight",
    "figure.dpi": 150,
})

def style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(length=3, colors=MUTED)

STYLES = ["-", "--", "-.", ":"]

# ---------- Fig R1: SR = HR * TR heatmap (§2) ----------
def fig_hr_tr():
    hr = np.linspace(0, 1, 200); tr = np.linspace(0, 1, 200)
    HR, TR = np.meshgrid(hr, tr); Z = HR * TR
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    cf = ax.contourf(HR, TR, Z, levels=np.linspace(0, 1, 21), cmap=SEQ)
    cs = ax.contour(HR, TR, Z, levels=[0.2, 0.4, 0.57, 0.7, 0.9],
                    colors=INK, linewidths=0.8, alpha=0.55)
    ax.clabel(cs, fmt="%.2f", fontsize=9, colors=INK)
    ax.plot(0.60, 0.95, "o", ms=9, mfc=CRIT, mec="white", mew=1.5, zorder=5)
    ax.annotate("HR=0.60, TR=0.95\nSR = 0.57",
                xy=(0.60, 0.95), xytext=(0.13, 0.62), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
    cb = fig.colorbar(cf, ax=ax, pad=0.02); cb.set_label("System reliability  SR", color=INK2)
    cb.outline.set_edgecolor(AXIS)
    ax.set_xlabel("Human reliability  HR"); ax.set_ylabel("Technological reliability  TR")
    ax.set_title("SR = HR · TR — a weak required factor caps the product", fontsize=12, pad=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    style(ax); ax.grid(False)
    fig.savefig(f"{OUT}/fig_sr_hr_tr.png"); plt.close(fig)

# ---------- Fig R2: SR vs R_t for several R_c (§6) ----------
def fig_rt_rc():
    rt = np.linspace(0, 1, 200)
    rcs = [1.0, 0.8, 0.6]
    labels = ["R_c = 1.0  (traditional, decomposable)", "R_c = 0.8", "R_c = 0.6"]
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    for i, (rc, lab) in enumerate(zip(rcs, labels)):
        ax.plot(rt, rt * rc, STYLES[i], color=SERIES[i], lw=2, label=lab)
    # overstatement annotation at R_t = 0.9
    ax.plot([0.9, 0.9], [0.9 * 0.6, 0.9 * 1.0], color=MUTED, lw=1, ls=":")
    ax.annotate("", xy=(0.9, 0.90), xytext=(0.9, 0.54),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.2))
    ax.text(0.905, 0.72, "reporting only R_t\noverstates SR by 0.36\nat R_t=0.9",
            fontsize=9.5, color=INK, va="center")
    ax.set_xlabel("Technological reliability  R_t")
    ax.set_ylabel("Effective reliability  SR = R_t · R_c")
    ax.set_title("The hidden axis: how coherence R_c scales the reported reliability",
                 fontsize=12, pad=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.xaxis.set_major_locator(MultipleLocator(0.2)); ax.yaxis.set_major_locator(MultipleLocator(0.2))
    leg = ax.legend(frameon=False, fontsize=10, loc="upper left")
    for t in leg.get_texts(): t.set_color(INK2)
    style(ax)
    fig.savefig(f"{OUT}/fig_rt_rc.png"); plt.close(fig)

# ---------- Fig R3: SR = R^n vs n for several R (§5) ----------
def fig_power_n():
    n = np.arange(1, 13)
    Rs = [0.99, 0.97, 0.95, 0.90]
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    for i, R in enumerate(Rs):
        ax.plot(n, R ** n, STYLES[i], color=SERIES[i], lw=2, marker="o", ms=5,
                mfc=SERIES[i], mec="white", mew=0.8, label=f"R = {R:.2f}")
    ax.axhline(0.90, color=MUTED, lw=1.2, ls=(0, (4, 3)))
    ax.text(12, 0.905, "SR_min = 0.90", ha="right", va="bottom", fontsize=9.5, color=INK2)
    ax.set_xlabel("Number of required components / occurrences  n")
    ax.set_ylabel("Modeled system reliability  SR = R^n")
    ax.set_title("Required components multiply: how n and per-step R erode SR",
                 fontsize=12, pad=10)
    ax.set_xlim(1, 12); ax.set_ylim(0.6, 1.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    leg = ax.legend(frameon=False, fontsize=10, loc="lower left")
    for t in leg.get_texts(): t.set_color(INK2)
    style(ax)
    fig.savefig(f"{OUT}/fig_power_n.png"); plt.close(fig)

# ---------- Fig R4: improve / worsen decision region (§12) ----------
def fig_decision_region():
    d = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ymax = 0.16
    b10 = 0.10 * (1 - d)           # boundary at F_base = 0.10
    ax.fill_between(d, 0, b10, color=GOOD, alpha=0.12)
    ax.fill_between(d, b10, ymax, color=CRIT, alpha=0.10)
    # boundary family
    for i, fb in enumerate([0.05, 0.10, 0.20]):
        ax.plot(d, fb * (1 - d), STYLES[i], color=SERIES[i], lw=2,
                label=f"boundary  I = F_base(1-d),  F_base = {fb:.2f}")
    # worked example points at d = 0.30
    ax.plot(0.30, 0.035, "o", ms=9, mfc=GOOD, mec="white", mew=1.5, zorder=6)
    ax.plot(0.30, 0.075, "o", ms=9, mfc=CRIT, mec="white", mew=1.5, zorder=6)
    ax.plot([0.30, 0.30], [0.035, 0.075], color=MUTED, lw=1, ls=":")
    ax.annotate("modeled  I = 0.035\n→ improves", xy=(0.30, 0.035),
                xytext=(0.40, 0.017), fontsize=9.5, color="#0a6d0a",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
    ax.annotate("honest  I = 0.075 (+F_U)\n→ worsens", xy=(0.30, 0.075),
                xytext=(0.40, 0.105), fontsize=9.5, color="#9c2020",
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
    ax.text(0.03, 0.012, "IMPROVES", fontsize=11, color="#0a6d0a", weight="bold")
    ax.text(0.03, 0.145, "WORSENS", fontsize=11, color="#9c2020", weight="bold")
    ax.set_xlabel("Fraction of original failures remaining  d(x)")
    ax.set_ylabel("Introduced failure  I = F_A + F_C + F_U")
    ax.set_title("When does agentic AI improve reliability? (shading at F_base = 0.10)",
                 fontsize=11.5, pad=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, ymax)
    leg = ax.legend(frameon=False, fontsize=9, loc="upper right")
    for t in leg.get_texts(): t.set_color(INK2)
    style(ax); ax.grid(True, alpha=0.5)
    fig.savefig(f"{OUT}/fig_decision_region.png"); plt.close(fig)

# ---------- Fig R5: R(tau) = e^{-lambda tau} family (§19) ----------
def fig_exposure():
    tau = np.linspace(0, 6, 200)
    lams = [0.2, 0.5, 1.0, 2.0]
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    for i, lam in enumerate(lams):
        ax.plot(tau, np.exp(-lam * tau), STYLES[i], color=SERIES[i], lw=2,
                label=f"λ = {lam:.1f}")
    tb, ta = 4.0, 1.5
    ax.axvspan(ta, tb, color=BLUE_RAMP[0], alpha=0.45)
    for t in (ta, tb):
        ax.axvline(t, color=MUTED, lw=1, ls=":")
    ax.text((ta + tb) / 2, 0.93, "cut exposure\nτ_b → τ_a", ha="center", fontsize=9.5, color=INK2)
    # gain marker for lambda = 0.5
    g_a, g_b = np.exp(-0.5 * ta), np.exp(-0.5 * tb)
    ax.annotate("", xy=(ta, g_a), xytext=(ta, g_b),
                arrowprops=dict(arrowstyle="<->", color=SERIES[1], lw=1.4))
    ax.text(ta - 0.15, (g_a + g_b) / 2, f"E(Δτ) = {g_a - g_b:.2f}\n(λ=0.5)",
            ha="right", va="center", fontsize=9.5, color=SERIES[1])
    ax.set_xlabel("Exposure time  τ")
    ax.set_ylabel("Exposure-time reliability  R(τ) = e^(−λτ)")
    ax.set_title("Exposure and failure rate: how λ and τ jointly set reliability",
                 fontsize=12, pad=10)
    ax.set_xlim(0, 6); ax.set_ylim(0, 1)
    leg = ax.legend(frameon=False, fontsize=10, loc="upper right", title="failure rate")
    leg.get_title().set_color(INK2)
    for t in leg.get_texts(): t.set_color(INK2)
    style(ax)
    fig.savefig(f"{OUT}/fig_exposure.png"); plt.close(fig)

# ---------- Fig R6: V = SR*Q/tau contour (§22) ----------
def fig_value():
    sr = np.linspace(0, 1, 200); tau = np.linspace(0.5, 4, 200)
    SR, TAU = np.meshgrid(sr, tau); Q = 1.0
    V = SR * Q / TAU
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    cf = ax.contourf(SR, TAU, V, levels=np.linspace(0, 2, 21), cmap=SEQ)
    cs = ax.contour(SR, TAU, V, levels=[0.25, 0.5, 0.75, 1.0, 1.5],
                    colors=INK, linewidths=0.8, alpha=0.55)
    ax.clabel(cs, fmt="%.2f", fontsize=9, colors=INK)
    srmin = 0.90
    ax.axvspan(0, srmin, color="#000000", alpha=0.10)
    ax.axvline(srmin, color=CRIT, lw=1.8, ls="--")
    ax.text(srmin - 0.02, 3.7, "SR < SR_min\nexcluded", ha="right", va="top",
            fontsize=9.5, color=INK)
    cb = fig.colorbar(cf, ax=ax, pad=0.02); cb.set_label("Value per unit time  V = SR·Q/τ", color=INK2)
    cb.outline.set_edgecolor(AXIS)
    ax.set_xlabel("Reliability  SR"); ax.set_ylabel("Time  τ")
    ax.set_title("Value V = SR·Q/τ (Q=1), constrained by SR ≥ SR_min",
                 fontsize=12, pad=10)
    ax.set_xlim(0, 1); ax.set_ylim(0.5, 4)
    style(ax); ax.grid(False)
    fig.savefig(f"{OUT}/fig_value.png"); plt.close(fig)

for f in (fig_hr_tr, fig_rt_rc, fig_power_n, fig_decision_region, fig_exposure, fig_value):
    f(); print("wrote", f.__name__)
print("done")
