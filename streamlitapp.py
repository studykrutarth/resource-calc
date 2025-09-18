import math
import streamlit as st

# -----------------------
# Translations
# -----------------------
TRANSLATIONS = {
    "en": {
        "title": "⚔️ Kingshot Resource Timer",
        "intro": "Enter **Target (full amount)**, and **Current + Rate in k-units**. Example: `602.6` = 602,600 and `46.8` = 46,800/hour.",
        "targets": "🎯 Resource Targets (full amounts)",
        "current_rates": "📊 Current & Production Rates (in k-units)",
        "bread_target": "🍞 Bread Target",
        "wood_target": "🌲 Wood Target",
        "stone_target": "🪨 Stone Target",
        "iron_target": "⛓ Iron Target",
        "bread_current_k": "🍞 Bread (Current k)",
        "bread_rate_k": "🍞 Bread (Rate k/h)",
        "wood_current_k": "🌲 Wood (Current k)",
        "wood_rate_k": "🌲 Wood (Rate k/h)",
        "stone_current_k": "🪨 Stone (Current k)",
        "stone_rate_k": "🪨 Stone (Rate k/h)",
        "iron_current_k": "⛓ Iron (Current k)",
        "iron_rate_k": "⛓ Iron (Rate k/h)",
        "time_calc": "⏱ Time Calculation",
        "already_enough": "✅ Already enough (current {cur_k:.1f}k / target {target:,})",
        "need_info": "{name}: Need {need_k:.1f}k, time ≈ {h}h {m}m at {rate_k:.1f}k/h",
        "rate_zero": "{name}: ⚠️ Production is 0 — cannot reach target.",
        "bottleneck": "🏆 Bottleneck Resource",
        "bottleneck_info": "The slowest is {name} → about {h}h {m}m to reach its target (needs {need_k:.1f}k).",
        "select_lang": "Select language / Sprache wählen / 选择语言 / Choisir la langue"
    },
    "de": {
        "title": "⚔️ Kingshot Ressourcen-Timer",
        "intro": "Gib **Ziel (Gesamtmenge)** und **Aktuell + Produktion in k-Einheiten** ein. Beispiel: `602.6` = 602.600 und `46.8` = 46.800/Stunde.",
        "targets": "🎯 Ressourcen Ziele (Gesamtmengen)",
        "current_rates": "📊 Aktuell & Produktionsraten (in k-Einheiten)",
        "bread_target": "🍞 Brot Ziel",
        "wood_target": "🌲 Holz Ziel",
        "stone_target": "🪨 Stein Ziel",
        "iron_target": "⛓ Eisen Ziel",
        "bread_current_k": "🍞 Brot (Aktuell k)",
        "bread_rate_k": "🍞 Brot (Rate k/h)",
        "wood_current_k": "🌲 Holz (Aktuell k)",
        "wood_rate_k": "🌲 Holz (Rate k/h)",
        "stone_current_k": "🪨 Stein (Aktuell k)",
        "stone_rate_k": "🪨 Stein (Rate k/h)",
        "iron_current_k": "⛓ Eisen (Aktuell k)",
        "iron_rate_k": "⛓ Eisen (Rate k/h)",
        "time_calc": "⏱ Zeit-Berechnung",
        "already_enough": "✅ Genug vorhanden (aktuell {cur_k:.1f}k / Ziel {target:,})",
        "need_info": "{name}: Benötigt {need_k:.1f}k, Zeit ≈ {h}h {m}m bei {rate_k:.1f}k/h",
        "rate_zero": "{name}: ⚠️ Produktion ist 0 — Ziel nicht erreichbar.",
        "bottleneck": "🏆 Engpass Ressource",
        "bottleneck_info": "Am langsamsten ist {name} → etwa {h}h {m}m bis zum Ziel (benötigt {need_k:.1f}k).",
        "select_lang": "Select language / Sprache wählen / 选择语言 / Choisir la langue"
    },
    "fr": {
        "title": "⚔️ Minuteur de ressources Kingshot",
        "intro": "Entrez **Cible (montant total)** et **Actuel + Production en k-unités**. Exemple : `602.6` = 602 600 et `46.8` = 46 800/heure.",
        "targets": "🎯 Objectifs de ressources (montants totaux)",
        "current_rates": "📊 Actuel & taux de production (en k-unités)",
        "bread_target": "🍞 Objectif Pain",
        "wood_target": "🌲 Objectif Bois",
        "stone_target": "🪨 Objectif Pierre",
        "iron_target": "⛓ Objectif Fer",
        "bread_current_k": "🍞 Pain (Actuel k)",
        "bread_rate_k": "🍞 Pain (Taux k/h)",
        "wood_current_k": "🌲 Bois (Actuel k)",
        "wood_rate_k": "🌲 Bois (Taux k/h)",
        "stone_current_k": "🪨 Pierre (Actuel k)",
        "stone_rate_k": "🪨 Pierre (Taux k/h)",
        "iron_current_k": "⛓ Fer (Actuel k)",
        "iron_rate_k": "⛓ Fer (Taux k/h)",
        "time_calc": "⏱ Calcul du temps",
        "already_enough": "✅ Suffisant (actuel {cur_k:.1f}k / objectif {target:,})",
        "need_info": "{name} : Besoin de {need_k:.1f}k, temps ≈ {h}h {m}m à {rate_k:.1f}k/h",
        "rate_zero": "{name} : ⚠️ La production est 0 — objectif inatteignable.",
        "bottleneck": "🏆 Ressource limitante",
        "bottleneck_info": "La plus lente est {name} → environ {h}h {m}m pour atteindre l'objectif (besoin {need_k:.1f}k).",
        "select_lang": "Select language / Sprache wählen / 选择语言 / Choisir la langue"
    },
    "zh": {  # Simplified Chinese
        "title": "⚔️ Kingshot 资源计时器",
        "intro": "输入**目标（总量）**，以及**当前 + 产量（以千为单位）**。例如：`602.6` = 602,600，`46.8` = 46,800/小时。",
        "targets": "🎯 资源目标（总量）",
        "current_rates": "📊 当前 & 产量（以千为单位）",
        "bread_target": "🍞 粮食 目标",
        "wood_target": "🌲 木材 目标",
        "stone_target": "🪨 石料 目标",
        "iron_target": "⛓ 铁 目标",
        "bread_current_k": "🍞 粮食（当前 k）",
        "bread_rate_k": "🍞 粮食（产量 k/h）",
        "wood_current_k": "🌲 木材（当前 k）",
        "wood_rate_k": "🌲 木材（产量 k/h）",
        "stone_current_k": "🪨 石料（当前 k）",
        "stone_rate_k": "🪨 石料（产量 k/h）",
        "iron_current_k": "⛓ 铁（当前 k）",
        "iron_rate_k": "⛓ 铁（产量 k/h）",
        "time_calc": "⏱ 时间计算",
        "already_enough": "✅ 已经足够（当前 {cur_k:.1f}k / 目标 {target:,}）",
        "need_info": "{name}：需要 {need_k:.1f}k，时间 ≈ {h}小时 {m}分钟，速度 {rate_k:.1f}k/h",
        "rate_zero": "{name}：⚠️ 产量为0 — 无法达到目标。",
        "bottleneck": "🏆 瓶颈资源",
        "bottleneck_info": "最慢的是 {name} → 约 {h}小时 {m}分钟 达到目标（需要 {need_k:.1f}k）。",
        "select_lang": "Select language / Sprache wählen / 选择语言 / Choisir la langue"
    }
     "es": {  # Spanish
        "title": "⚔️ Temporizador de Recursos Kingshot",
        "intro": "Ingresa **Objetivo (cantidad total)** y **Actual + Producción en miles (k)**. Ejemplo: `602.6` = 602,600 y `46.8` = 46,800/hora.",
        "targets": "🎯 Objetivos de Recursos (cantidades totales)",
        "current_rates": "📊 Actual & Tasas de Producción (en miles)",
        "bread_target": "🍞 Objetivo Pan",
        "wood_target": "🌲 Objetivo Madera",
        "stone_target": "🪨 Objetivo Piedra",
        "iron_target": "⛓ Objetivo Hierro",
        "bread_current_k": "🍞 Pan (Actual k)",
        "bread_rate_k": "🍞 Pan (Tasa k/h)",
        "wood_current_k": "🌲 Madera (Actual k)",
        "wood_rate_k": "🌲 Madera (Tasa k/h)",
        "stone_current_k": "🪨 Piedra (Actual k)",
        "stone_rate_k": "🪨 Piedra (Tasa k/h)",
        "iron_current_k": "⛓ Hierro (Actual k)",
        "iron_rate_k": "⛓ Hierro (Tasa k/h)",
        "time_calc": "⏱ Cálculo de Tiempo",
        "already_enough": "✅ Ya tienes suficiente (actual {cur_k:.1f}k / objetivo {target:,})",
        "need_info": "{name}: Faltan {need_k:.1f}k, tiempo ≈ {h}h {m}m a {rate_k:.1f}k/h",
        "rate_zero": "{name}: ⚠️ Producción es 0 — no se puede alcanzar el objetivo.",
        "bottleneck": "🏆 Recurso Limitante",
        "bottleneck_info": "El más lento es {name} → aproximadamente {h}h {m}m para alcanzar el objetivo (faltan {need_k:.1f}k).",
        "select_lang": "Seleccionar idioma / Select language / Sprache wählen / 选择语言 / Choisir la langue"
    },
}

LANG_OPTIONS = {
    "English": "en",
    "Deutsch (German)": "de",
    "Français (French)": "fr",
    "中文 (简体)": "zh",
    "Español (Spanish)": "es"
}

# -----------------------
# Helpers
# -----------------------
def t(key):
    return TRANSLATIONS[lang_code].get(key, key)

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
# UI
# -----------------------
st.set_page_config(page_title="Kingshot Resource Timer", layout="centered")

# Language selector
lang_choice = st.selectbox("🌐 " + "Select language", list(LANG_OPTIONS.keys()), index=0)
lang_code = LANG_OPTIONS[lang_choice]

# Use translations
st.title(TRANSLATIONS[lang_code]["title"])
st.write(TRANSLATIONS[lang_code]["intro"])

# Targets row
st.subheader(TRANSLATIONS[lang_code]["targets"])
tcol1, tcol2, tcol3, tcol4 = st.columns(4)
with tcol1:
    bread_target = st.number_input(TRANSLATIONS[lang_code]["bread_target"], min_value=0, value=700000, step=10000)
with tcol2:
    wood_target = st.number_input(TRANSLATIONS[lang_code]["wood_target"], min_value=0, value=700000, step=10000)
with tcol3:
    stone_target = st.number_input(TRANSLATIONS[lang_code]["stone_target"], min_value=0, value=400000, step=10000)
with tcol4:
    iron_target = st.number_input(TRANSLATIONS[lang_code]["iron_target"], min_value=0, value=200000, step=10000)

st.subheader(TRANSLATIONS[lang_code]["current_rates"])
col1, col2 = st.columns(2)
with col1:
    bread_current_k = st.number_input(TRANSLATIONS[lang_code]["bread_current_k"], min_value=0.0, value=602.6, step=0.1, format="%.1f")
    bread_rate_k = st.number_input(TRANSLATIONS[lang_code]["bread_rate_k"], min_value=0.0, value=97.2, step=0.1, format="%.1f")
    bread_current = bread_current_k * 1000
    bread_rate = bread_rate_k * 1000

    stone_current_k = st.number_input(TRANSLATIONS[lang_code]["stone_current_k"], min_value=0.0, value=786.2, step=0.1, format="%.1f")
    stone_rate_k = st.number_input(TRANSLATIONS[lang_code]["stone_rate_k"], min_value=0.0, value=39.6, step=0.1, format="%.1f")
    stone_current = stone_current_k * 1000
    stone_rate = stone_rate_k * 1000

with col2:
    wood_current_k = st.number_input(TRANSLATIONS[lang_code]["wood_current_k"], min_value=0.0, value=548.3, step=0.1, format="%.1f")
    wood_rate_k = st.number_input(TRANSLATIONS[lang_code]["wood_rate_k"], min_value=0.0, value=93.6, step=0.1, format="%.1f")
    wood_current = wood_current_k * 1000
    wood_rate = wood_rate_k * 1000

    iron_current_k = st.number_input(TRANSLATIONS[lang_code]["iron_current_k"], min_value=0.0, value=513.0, step=0.1, format="%.1f")
    iron_rate_k = st.number_input(TRANSLATIONS[lang_code]["iron_rate_k"], min_value=0.0, value=46.8, step=0.1, format="%.1f")
    iron_current = iron_current_k * 1000
    iron_rate = iron_rate_k * 1000

# Calculate and display
st.subheader(TRANSLATIONS[lang_code]["time_calc"])
resources = [
    (TRANSLATIONS[lang_code]["bread_target"], bread_target, bread_current, bread_rate, bread_current_k, bread_rate_k, "🍞"),
    (TRANSLATIONS[lang_code]["wood_target"], wood_target, wood_current, wood_rate, wood_current_k, wood_rate_k, "🌲"),
    (TRANSLATIONS[lang_code]["stone_target"], stone_target, stone_current, stone_rate, stone_current_k, stone_rate_k, "🪨"),
    (TRANSLATIONS[lang_code]["iron_target"], iron_target, iron_current, iron_rate, iron_current_k, iron_rate_k, "⛓"),
]

slowest = None
for label, target, current, rate, cur_k, rate_k, emoji in resources:
    needed, h, m = time_to_reach(target, current, rate)
    name = f"{emoji} {label}"
    if rate == 0 and needed > 0:
        st.error(TRANSLATIONS[lang_code]["rate_zero"].format(name=name))
    elif needed == 0:
        st.success(TRANSLATIONS[lang_code]["already_enough"].format(cur_k=cur_k, target=target))
    else:
        st.info(TRANSLATIONS[lang_code]["need_info"].format(name=name, need_k=needed/1000.0, h=h, m=m, rate_k=rate_k))
        if slowest is None or (h is not None and (h > slowest[1] or (h == slowest[1] and m > slowest[2]))):
            slowest = (name, h, m, needed)

if slowest:
    st.subheader(TRANSLATIONS[lang_code]["bottleneck"])
    st.warning(TRANSLATIONS[lang_code]["bottleneck_info"].format(name=slowest[0], h=slowest[1], m=slowest[2], need_k=slowest[3]/1000.0))

# Footer hint about adding languages
st.caption("Tip: Add or edit translations in the TRANSLATIONS dict to support more languages.")

