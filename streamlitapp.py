import math
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

# -----------------------
# Helpers
# -----------------------
def time_to_reach(target: float, current: float, rate_per_hour: float):
    """
    Returns (needed, hours_float, h, m).
    If already met, returns zeros for time.
    """
    needed = max(0.0, target - current)
    if rate_per_hour <= 0:
        return needed, math.inf, math.inf, math.inf
    if needed == 0:
        return 0.0, 0.0, 0, 0
    hours = needed / rate_per_hour
    h = int(hours)
    m = int(round((hours - h) * 60))
    # normalize 60 minutes -> +1 hour
    if m == 60:
        h += 1
        m = 0
    return needed, hours, h, m

def nice_time(h: int, m: int):
    if h == math.inf:
        return "∞ (rate is 0)"
    if h == 0 and m == 0:
        return "0m (already enough)"
    parts = []
    if h > 0:
        parts.append(f"{h}h")
    if m > 0:
        parts.append(f"{m}m")
    return " ".join(parts) if parts else "0m"

def projection_rows(name, current, rate_h, target, max_hours=48):
    """Generate hourly projection until target or max_hours."""
    rows = []
    amt = current
    hour = 0
    rows.append({"Hour": 0, "Resource": name, "Amount": int(amt)})
    while amt < target and hour < max_hours:
        hour += 1
        amt += rate_h
        rows.append({"Hour": hour, "Resource": name, "Amount": int(amt)})
    return rows

# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="Kingshot Multi-Resource Calculator", layout="centered")
st.title("⚔️ Kingshot Multi-Resource Calculator")
st.caption("Enter your **Target**, **Current**, and **Production Rate (per hour)** for each resource. The app shows per-resource timing and the bottleneck (slowest).")

with st.sidebar:
    st.header("Global Options")
    show_projection = st.toggle("Show hourly projection tables", value=True)
    projection_hours = st.slider("Projection horizon (hours)", 6, 72, 24)
    show_finish_clock = st.toggle("Show finish clock time (local)", value=False)

st.subheader("Inputs")

colA, colB, colC, colD = st.columns(4)
with colA:
    st.markdown("### 🍞 Bread")
    bread_target = st.number_input("Target (Bread)", min_value=0, value=700_000, step=10_000, key="bt")
    bread_current = st.number_input("Current (Bread)", min_value=0, value=640_000, step=10_000, key="bc")
    bread_rate = st.number_input("Rate / hour (Bread)", min_value=0, value=97_200, step=600, key="br")

with colB:
    st.markdown("### 🌲 Wood")
    wood_target = st.number_input("Target (Wood)", min_value=0, value=700_000, step=10_000, key="wt")
    wood_current = st.number_input("Current (Wood)", min_value=0, value=646_000, step=10_000, key="wc")
    wood_rate = st.number_input("Rate / hour (Wood)", min_value=0, value=93_600, step=600, key="wr")

with colC:
    st.markdown("### 🪨 Stone")
    stone_target = st.number_input("Target (Stone)", min_value=0, value=400_000, step=10_000, key="st")
    stone_current = st.number_input("Current (Stone)", min_value=0, value=786_000, step=10_000, key="sc")
    stone_rate = st.number_input("Rate / hour (Stone)", min_value=0, value=39_600, step=600, key="sr")

with colD:
    st.markdown("### ⛓ Iron")
    iron_target = st.number_input("Target (Iron)", min_value=0, value=200_000, step=10_000, key="it")
    iron_current = st.number_input("Current (Iron)", min_value=0, value=513_000, step=10_000, key="ic")
    iron_rate = st.number_input("Rate / hour (Iron)", min_value=0, value=46_800, step=600, key="ir")

resources = [
    ("Bread", bread_target, bread_current, bread_rate, "🍞"),
    ("Wood", wood_target, wood_current, wood_rate, "🌲"),
    ("Stone", stone_target, stone_current, stone_rate, "🪨"),
    ("Iron", iron_target, iron_current, iron_rate, "⛓"),
]

# Compute per-resource
rows = []
finish_times = []

for name, target, current, rate, emoji in resources:
    needed, hours_float, h, m = time_to_reach(target, current, rate)
    rows.append({
        "Resource": f"{emoji} {name}",
        "Target": target,
        "Current": current,
        "Needed": int(needed),
        "Rate/h": rate,
        "Time Needed": nice_time(h, m),
        "Hours (exact)": (None if hours_float == math.inf else round(hours_float, 2))
    })
    finish_times.append(hours_float)

df = pd.DataFrame(rows)

st.subheader("Summary (per resource)")
st.dataframe(df, use_container_width=True)

# Bottleneck
bottleneck_hours = max(finish_times)
if bottleneck_hours == 0:
    st.success("✅ All targets already met for every resource.")
elif bottleneck_hours == math.inf:
    st.error("⚠️ One or more resources have a rate of 0 — cannot reach target.")
else:
    b_h = int(bottleneck_hours)
    b_m = int(round((bottleneck_hours - b_h) * 60))
    if b_m == 60:
        b_h += 1
        b_m = 0

    st.markdown("---")
    st.subheader("⏳ Bottleneck (overall finish)")
    st.info(f"All targets will be met in **~{b_h}h {b_m}m** (limited by the slowest resource).")

    if show_finish_clock:
        finish_at = datetime.now() + timedelta(hours=bottleneck_hours)
        st.caption(f"Estimated finish time: **{finish_at.strftime('%Y-%m-%d %H:%M')}** (your local clock)")

# Projection tables
if show_projection:
    st.markdown("---")
    st.subheader(f"📈 Hourly Projection (up to {projection_hours}h)")
    proj_all = []
    for name, target, current, rate, emoji in resources:
        proj_all.extend(projection_rows(name, current, rate, target, max_hours=projection_hours))
    proj_df = pd.DataFrame(proj_all)
    # Show separate tables per resource for readability
    tabs = st.tabs([r[0] for r in [("🍞 Bread",), ("🌲 Wood",), ("🪨 Stone",), ("⛓ Iron",)]])
    for i, name in enumerate(["Bread", "Wood", "Stone", "Iron"]):
        with tabs[i]:
            sub = proj_df[proj_df["Resource"] == name].copy()
            st.dataframe(sub, use_container_width=True)

st.markdown("---")
st.caption("Tip: If your rates change later (e.g., you add more resource sources), update the numbers above to see the new finish time instantly.")
