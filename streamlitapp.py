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

st.write("Enter your **current resources** and **production per hour** just like in your Alliance Territory screen, then set the target requirement.")

# Input target
target = st.number_input("🎯 Target requirement (for HQ / upgrade)", min_value=0, value=700000, step=10000)

st.subheader("📊 Resource Status")

# Layout like game screen
col1, col2 = st.columns(2)
with col1:
    bread_current = st.number_input("🍞 Bread (Current)", min_value=0, value=602600, step=1000)
    bread_rate = st.number_input("🍞 Bread (Rate / hour)", min_value=0, value=97200, step=100)

    stone_current = st.number_input("🪨 Stone (Current)", min_value=0, value=786200, step=1000)
    stone_rate = st.number_input("🪨 Stone (Rate / hour)", min_value=0, value=39600, step=100)

with col2:
    wood_current = st.number_input("🌲 Wood (Current)", min_value=0, value=548300, step=1000)
    wood_rate = st.number_input("🌲 Wood (Rate / hour)", min_value=0, value=93600, step=100)

    iron_current = st.number_input("⛓ Iron (Current)", min_value=0, value=513000, step=1000)
    iron_rate = st.number_input("⛓ Iron (Rate / hour)", min_value=0, value=46800, step=100)

# Resources list
resources = [
    ("🍞 Bread", bread_current, bread_rate),
    ("🌲 Wood", wood_current, wood_rate),
    ("🪨 Stone", stone_current, stone_rate),
    ("⛓ Iron", iron_current, iron_rate),
]

st.subheader("⏱ Time Calculation")

slowest_time = (0, 0, 0, "")  # h, m, needed, name

for name, current, rate in resources:
    needed, h, m = time_to_reach(target, current, rate)
    if rate == 0:
        st.error(f"{name}: ⚠️ Production is 0 — cannot reach target.")
    elif needed == 0:
        st.success(f"{name}: ✅ Already enough (current {current:,} / target {target:,})")
    else:
        st.info(f"{name}: Need {needed:,}, time ≈ {h}h {m}m at {rate:,}/h")
        if h is not None and (h > slowest_time[0] or (h == slowest_time[0] and m > slowest_time[1])):
            slowest_time = (h, m, needed, name)

if slowest_time[2] > 0:
    st.subheader("🏆 Bottleneck Resource")
    st.warning(f"The slowest is {slowest_time[3]} → about {slowest_time[0]}h {slowest_time[1]}m to reach the target.")
