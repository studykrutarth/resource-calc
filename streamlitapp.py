import math
import streamlit as st

# -----------------------
# Helper function
# -----------------------
def time_to_reach(target, current, rate):
    needed = max(0, target - current)
    if needed == 0:
        return needed, 0, 0
    if rate <= 0:
        return needed, None, None
    hours = needed / rate
    h = int(hours)
    m = int((hours - h) * 60)
    return needed, h, m

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="Kingshot Resource Timer", layout="centered")
st.title("⚔️ Kingshot Resource Timer")

st.write("Enter **Target, Current, and Production Rate (in k/hour)** for each resource. "
         "Example: `46.8` means 46,800 per hour.")

# -----------------------
# Targets Row
# -----------------------
st.subheader("🎯 Resource Targets")

tcol1, tcol2, tcol3, tcol4 = st.columns(4)
with tcol1:
    bread_target = st.number_input("🍞 Bread Target", min_value=0, value=700000, step=10000)
with tcol2:
    wood_target = st.number_input("🌲 Wood Target", min_value=0, value=700000, step=10000)
with tcol3:
    stone_target = st.number_input("🪨 Stone Target", min_value=0, value=400000, step=10000)
with tcol4:
    iron_target = st.number_input("⛓ Iron Target", min_value=0, value=200000, step=10000)

# -----------------------
# Current + Rate inputs
# -----------------------
st.subheader("📊 Current & Production Rates (in k/hour)")

col1, col2 = st.columns(2)
with col1:
    bread_current = st.number_input("🍞 Bread (Current)", min_value=0, value=602600, step=1000)
    bread_rate_k = st.number_input("🍞 Bread (Rate / k per hour)", min_value=0.0, value=97.2, step=0.1)
    bread_rate = bread_rate_k * 1000  # convert to actual

    stone_current = st.number_input("🪨 Stone (Current)", min_value=0, value=786200, step=1000)
    stone_rate_k = st.number_input("🪨 Stone (Rate / k per hour)", min_value=0.0, value=39.6, step=0.1)
    stone_rate = stone_rate_k * 1000

with col2:
    wood_current = st.number_input("🌲 Wood (Current)", min_value=0, value=548300, step=1000)
    wood_rate_k = st.number_input("🌲 Wood (Rate / k per hour)", min_value=0.0, value=93.6, step=0.1)
    wood_rate = wood_rate_k * 1000

    iron_current = st.number_input("⛓ Iron (Current)", min_value=0, value=513000, step=1000)
    iron_rate_k = st.number_input("⛓ Iron (Rate / k per hour)", min_value=0.0, value=46.8, step=0.1)
    iron_rate = iron_rate_k * 1000

# -----------------------
# Calculation
# -----------------------
resources = [
    ("🍞 Bread", bread_target, bread_current, bread_rate),
    ("🌲 Wood", wood_target, wood_current, wood_rate),
    ("🪨 Stone", stone_target, stone_current, stone_rate),
    ("⛓ Iron", iron_target, iron_current, iron_rate),
]

st.subheader("⏱ Time Calculation")

slowest = None
for name, target, current, rate in resources:
    needed, h, m = time_to_reach(target, current, rate)
    if rate == 0 and needed > 0:
        st.error(f"{name}: ⚠️ Production is 0 — cannot reach target.")
    elif needed == 0:
        st.success(f"{name}: ✅ Already enough (current {current:,} / target {target:,})")
    else:
        st.info(f"{name}: Need {needed:,}, time ≈ {h}h {m}m at {rate/1000:.1f}k/h")
        if slowest is None or (h is not None and (h > slowest[1] or (h == slowest[1] and m > slowest[2]))):
            slowest = (name, h, m, needed)

if slowest:
    st.subheader("🏆 Bottleneck Resource")
    st.warning(f"The slowest is {slowest[0]} → about {slowest[1]}h {slowest[2]}m "
               f"to reach its target (needs {slowest[3]:,}).")
