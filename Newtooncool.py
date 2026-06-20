"""
Newton's Law of Cooling - Interactive Curve Tracing Model
Formula: T(t) = T_s + (T0 - T_s) * e^(-k*t)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, Button, TextBox


# Initial parameter values
T0_INIT  = 100.0   # Initial temperature (°C)
TS_INIT  =  25.0   # Surrounding/ambient temperature (°C)
K_INIT   =   0.10  # Cooling constant (per minute)
TMAX_INIT = 60.0   # Time duration (minutes)


def compute_curve(T0, Ts, k, t_max, n=500):
    """Return time array and temperature array."""
    t = np.linspace(0, t_max, n)
    T = Ts + (T0 - Ts) * np.exp(-k * t)
    return t, T


def half_time(k):
    return np.log(2) / k


# Figure layout
fig = plt.figure(figsize=(12, 8), facecolor="#f8f9fa")
fig.canvas.manager.set_window_title("Newton's Law of Cooling")

# Adjusted 'top' from 0.93 to 0.88 to prevent suptitle overlap
gs = gridspec.GridSpec(
    3, 3,
    figure=fig,
    top=0.88, bottom=0.30,
    left=0.08, right=0.97,
    hspace=0.40, wspace=0.35
)

ax_main  = fig.add_subplot(gs[:, :2])   # main curve (left, tall)
ax_rate  = fig.add_subplot(gs[0, 2])    # dT/dt subplot (top-right)
ax_stats = fig.add_subplot(gs[1:, 2])   # stats table (bottom-right)

#  Styling helpers 
BLUE   = "#1a73e8"
ORANGE = "#e8710a"
GREEN  = "#1e8e3e"
GRAY   = "#5f6368"
BG     = "#ffffff"

for ax in [ax_main, ax_rate]:
    ax.set_facecolor(BG)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#dadce0")
    ax.tick_params(colors=GRAY, labelsize=9)
    ax.grid(True, color="#f1f3f4", linewidth=0.8, zorder=0)

ax_stats.axis("off")

#  Initial draw
t, T = compute_curve(T0_INIT, TS_INIT, K_INIT, TMAX_INIT)
dTdt  = -K_INIT * (T - TS_INIT)

# Main curve
line_T,    = ax_main.plot(t, T,    color=BLUE,   lw=2.5, label="T(t)  object temp", zorder=3)
line_Ts,   = ax_main.plot(t, np.full_like(t, TS_INIT), color=ORANGE,
                           lw=1.5, ls="--", label="T∞  ambient temp", zorder=2)

# Half-time vertical marker
ht = half_time(K_INIT)
ht_T = TS_INIT + (T0_INIT - TS_INIT) * np.exp(-K_INIT * ht)
vline  = ax_main.axvline(ht, color=GREEN, lw=1.2, ls=":", alpha=0.8, zorder=2)
dot,   = ax_main.plot(ht, ht_T, "o", color=GREEN, ms=7, zorder=4)

# Adjusted text positioning relative to window limits
htlbl  = ax_main.text(ht + TMAX_INIT * 0.015, ht_T + (T0_INIT - TS_INIT) * 0.02, 
                       f"t½={ht:.1f} min\nT={ht_T:.1f}°C",
                       fontsize=8, color=GREEN, va="bottom")

ax_main.set_xlabel("Time (minutes)", color=GRAY, fontsize=10)
ax_main.set_ylabel("Temperature (°C)", color=GRAY, fontsize=10)

# Shifted subplot title slightly up using y parameter to avoid hugging the plot
ax_main.set_title("Newton's Law of Cooling  —  T(t) = T∞ + (T₀ − T∞)·e^(−kt)",
                   fontsize=11, color="#202124", pad=12, y=1.02)
ax_main.legend(fontsize=9, loc="upper right", framealpha=0.9)

# Rate-of-change subplot
line_rate, = ax_rate.plot(t, dTdt, color="#9c27b0", lw=1.8)
ax_rate.axhline(0, color="#dadce0", lw=0.8)
ax_rate.set_xlabel("Time (min)", color=GRAY, fontsize=8)
ax_rate.set_ylabel("dT/dt  (°C/min)", color=GRAY, fontsize=8)
ax_rate.set_title("Rate of Cooling", fontsize=9, color="#202124", pad=8, y=1.02)

# Stats table
stats_text = ax_stats.text(
    0.05, 0.90, "", transform=ax_stats.transAxes,
    fontsize=9, va="top", fontfamily="monospace", color="#202124",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="#e8f0fe", edgecolor="#c5cae9", lw=0.8)
)
ax_stats.set_title("Key Statistics", fontsize=9, color="#202124", pad=4, y=0.15)


def update_stats(T0, Ts, k, t_max):
    T_end  = Ts + (T0 - Ts) * np.exp(-k * t_max)
    ht     = np.log(2) / k
    T_half = Ts + (T0 - Ts) * np.exp(-k * ht)
    drop   = T0 - T_end
    rate0  = -k * (T0 - Ts)

    txt = (
        f"{'Parameter':─<22}\n"
        f"  T₀  (initial)  : {T0:.1f} °C\n"
        f"  T∞  (ambient)  : {Ts:.1f} °C\n"
        f"  k   (constant) : {k:.3f} /min\n"
        f"  t   (duration) : {t_max:.0f} min\n"
        f"\n{'Result':─<22}\n"
        f"  T(0)           : {T0:.2f} °C\n"
        f"  T(t_max)       : {T_end:.2f} °C\n"
        f"  Temp drop      : {drop:.2f} °C\n"
        f"  Half-time t½   : {ht:.2f} min\n"
        f"  T at t½        : {T_half:.2f} °C\n"
        f"  Init rate dT/dt: {rate0:.3f} °C/min"
    )
    stats_text.set_text(txt)


update_stats(T0_INIT, TS_INIT, K_INIT, TMAX_INIT)

# ─ Sliders 
slider_color = "#e8f0fe"

ax_s_T0   = fig.add_axes([0.08, 0.22, 0.55, 0.025], facecolor=slider_color)
ax_s_Ts   = fig.add_axes([0.08, 0.17, 0.55, 0.025], facecolor=slider_color)
ax_s_k    = fig.add_axes([0.08, 0.12, 0.55, 0.025], facecolor=slider_color)
ax_s_tmax = fig.add_axes([0.08, 0.07, 0.55, 0.025], facecolor=slider_color)

sl_T0   = Slider(ax_s_T0,   "T₀  Initial (°C)",    50,  300, valinit=T0_INIT,   valstep=1,   color=BLUE)
sl_Ts   = Slider(ax_s_Ts,   "T∞  Ambient (°C)",   -20,   80, valinit=TS_INIT,   valstep=1,   color=ORANGE)
sl_k    = Slider(ax_s_k,    "k   Cooling const",  0.01, 0.5, valinit=K_INIT,    valstep=0.01, color="#9c27b0")
sl_tmax = Slider(ax_s_tmax, "t   Duration (min)",  10,  120, valinit=TMAX_INIT, valstep=5,   color=GRAY)
# Reset button
ax_reset = fig.add_axes([0.76, 0.10, 0.09, 0.04])
btn_reset = Button(ax_reset, "Reset", color="#fce8e6", hovercolor="#f28b82")

# Export button
ax_export = fig.add_axes([0.87, 0.10, 0.10, 0.04])
btn_export = Button(ax_export, "Save PNG", color="#e6f4ea", hovercolor="#81c995")


#  Update callback
def update(val=None):
    T0   = sl_T0.val
    Ts   = sl_Ts.val
    k    = sl_k.val
    tmax = sl_tmax.val

    t, T   = compute_curve(T0, Ts, k, tmax)
    dTdt_v = -k * (T - Ts)

    line_T.set_data(t, T)
    line_Ts.set_data(t, np.full_like(t, Ts))
    line_rate.set_data(t, dTdt_v)

    ht   = half_time(k)
    ht_T = Ts + (T0 - Ts) * np.exp(-k * ht)

    vline.set_xdata([ht, ht])
    dot.set_data([ht], [ht_T])
    htlbl.set_position((ht + tmax * 0.015, ht_T + (T0 - Ts) * 0.02))
    htlbl.set_text(f"t½={ht:.1f} min\nT={ht_T:.1f}°C")

    # Rescale axes
    pad = (T0 - Ts) * 0.08 if T0 != Ts else 5
    ax_main.set_xlim(0, tmax)
    ax_main.set_ylim(min(Ts, T[-1]) - pad, T0 + pad)

    ax_rate.set_xlim(0, tmax)
    ax_rate.relim(); ax_rate.autoscale_view()

    update_stats(T0, Ts, k, tmax)
    fig.canvas.draw_idle()


def reset(event):
    sl_T0.reset(); sl_Ts.reset(); sl_k.reset(); sl_tmax.reset()


def save_png(event):
    fname = "newtons_cooling_curve.png"
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    print(f"[Saved] → {fname}")


sl_T0.on_changed(update)
sl_Ts.on_changed(update)
sl_k.on_changed(update)
sl_tmax.on_changed(update)
btn_reset.on_clicked(reset)
btn_export.on_clicked(save_png)

# Initial axis limits
ax_main.set_xlim(0, TMAX_INIT)
ax_main.set_ylim(TS_INIT - 10, T0_INIT + 10)
ax_rate.set_xlim(0, TMAX_INIT)

# Pushed main title higher using y=0.96 to make sure it clears everything completely
plt.suptitle("Newton's Law of Cooling  |  Interactive Simulator",
             fontsize=13, color="#202124", y=0.96, fontweight="500")

plt.show()
