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

st.write("Enter **Target (full amount)**, and **Current + Rate in k-units**. "
         "Example: `602.6` = 602,600 and `46.8` = 46,800/hour.")

# -----------------------
# Targets Row
# -----------------------
st.subheader("🎯 Resource Targets (full amounts)")

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
st.subheader("📊 Current & Production Rates (in k-units)")

col1, col2 = st.columns(2)
with col1:
    bread_current_k = st.number_input("🍞 Bread (Current k)", min_value=0.0, value=602.6, step=0.1)
    bread_rate_k = st.number_input("🍞 Bread (Rate k/h)", min_value=0.0, value=97.2, step=0.1)
    bread_current = bread_current_k * 1000
    bread_rate = bread_rate_k * 1000

    stone_current_k = st.number_input("🪨 Stone (Current k)", min_value=0.0, value=786.2, step=0.1)
    stone_rate_k = st.number_input("🪨 Stone (Rate k/h)", min_value=0.0, value=39.6, step=0.1)
    stone_current = stone_current_k * 1000
    stone_rate = stone_rate_k * 1000

with col2:
    wood_current_k = st.number_input("🌲 Wood (Current k)", min_value=0.0, value=548.3, step=0.1)
    wood_rate_k = st.number_input("🌲 Wood (Rate k/h)", min_value=0.0, value=93.6, step=0.1)
    wood_current = wood_current_k * 1000
    wood_rate = wood_rate_k * 1000

    iron_current_k = st.number_input("⛓ Iron (Current k)", min_value=0.0, value=513.0, step=0.1)
    iron_rate_k = st.number_input("⛓ Iron (Rate k/h)", min_value=0.0, value=46.8, step=0.1)
    iron_current = iron_current_k * 1000
    iron_rate = iron_rate_k * 1000

# -----------------------
# Calculation
# -----------------------
resources = [
    ("🍞 Bread", bread_target, bread_current, bread_rate, bread_current_k, bread_rate_k),
    ("🌲 Wood", wood_target, wood_current, wood_rate, wood_current_k, wood_rate_k),
    ("🪨 Stone", stone_target, stone_current, stone_rate, stone_current_k, stone_rate_k),
    ("⛓ Iron", iron_target, iron_current, iron_rate, iron_current_k, iron_rate_k),
]

st.subheader("⏱ Time Calculation")

slowest = None
for name, target, current, rate, cur_k, rate_k in resources:
    needed, h, m = time_to_reach(target, current, rate)
    if rate == 0 and needed > 0:
        st.error(f"{name}: ⚠️ Production is 0 — cannot reach target.")
    elif needed == 0:
        st.success(f"{name}: ✅ Already enough (current {cur_k:.1f}k / target {target:,})")
    else:
        st.info(f"{name}: Need {needed/1000:.1f}k, time ≈ {h}h {m}m at {rate_k:.1f}k/h")
        if slowest is None or (h is not None and (h > slowest[1] or (h == slowest[1] and m > slowest[2]))):
            slowest = (name, h, m, needed)

if slowest:
    st.subheader("🏆 Bottleneck Resource")
    st.warning(f"The slowest is {slowest[0]} → about {slowest[1]}h {slowest[2]}m "
               f"to reach its target (needs {slowest[3]/1000:.1f}k).")
