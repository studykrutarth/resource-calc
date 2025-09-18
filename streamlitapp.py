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

st.write("Enter **target, current, and production rate** for each resource. The app will calculate how long until you reach the requirement.")

st.subheader("📊 Resource Inputs")

# Layout like game screen
col1, col2 = st.columns(2)
with col1:
    bread_target = st.number_input("🍞 Bread (Target)", min_value=0, value=700000, step=10000)
    bread_current = st.number_input("🍞 Bread (Current)", min_value=0, value=602600, step=1000)
    bread_rate = st.number_input("🍞 Bread (Rate / hour)", min_value=0, value=97200, step=100)

    stone_target = st.number_input("🪨 Stone (Target)", min_value=0, value=400000, step=10000)
    stone_current = st.number_input("🪨 Stone (Current)", min_value=0, value=786200, step=1000)
    stone_rate = st.number_input("🪨 Stone (Rate / hour)", min_value=0, value=39600, step=100)

with col2:
    wood_target = st.number_input("🌲 Wood (Target)", min_value=0, value=700000, step=10000)
    wood_current = st.number_input("🌲 Wood (Current)", min_value=0, value=548300, step=1000)
    wood_rate = st.number_input("🌲 Wood (Rate / hour)", min_value=0, value=93600, step=100)

    iron_target = st.number_input("⛓ Iron (Target)", min_value=0, value=200000, step=10000)
    iron_current = st.number_input("⛓ Iron (Current)", min_value=0, value=513000, step=1000)
    iron_rate = st.number_input("⛓ Iron (Rate / hour)", min_value=0, value=46800, step=100)

# Resources list
resources = [
    ("🍞 Bread", bread_target, bread_current, bread_rate),
    ("🌲 Wood", wood_target, wood_current, wood_rate),
    ("🪨 Stone", stone_target, stone_current, stone_rate),
    ("⛓ Iron", iron_target, iron_current, iron_rate),
]

st.subheader("⏱ Time Calculation")

slowest = None  # Track bottleneck

for name, target, current, rate in resources:
    needed, h, m = time_to_reach(target, current, rate)
    if rate == 0 and needed > 0:
        st.error(f"{name}: ⚠️ Production is 0 — cannot reach target.")
    elif needed == 0:
        st.success(f"{name}: ✅ Already enough (current {current:,} / target {target:,})")
    else:
        st.info(f"{name}: Need {needed:,}, time ≈ {h}h {m}m at {rate:,}/h")
        if slowest is None or (h is not None and (h > slowest[1] or (h == slowest[1] and m > slowest[2]))):
            slowest = (name, h, m, needed)

if slowest:
    st.subheader("🏆 Bottleneck Resource")
    st.warning(f"The slowest is {slowest[0]} → about {slowest[1]}h {slowest[2]}m to reach its target (needs {slowest[3]:,}).")
