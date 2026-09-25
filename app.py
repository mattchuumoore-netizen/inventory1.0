import streamlit as st

st.set_page_config(
    page_title="Tank Media Inventory Calculator", page_icon="⚖️", layout="wide"
)

st.title("⚖️ Tank Inventory: Percentage to Weight Converter with Visuals")
st.markdown(
    "Adjust fill percentages to instantly view calculated weights and dynamic tank levels."
)

# Sidebar for global configurations
st.sidebar.header("⚙️ Default Settings")
st.sidebar.markdown(
    "**Face Resin:** 216 in | 496 lbs/in\n\n**Core Resin:** 228 in | 1,000 lbs/in\n\n**Scavenger:** 228 in | 576 lbs/in"
)

default_wax_cap = st.sidebar.number_input("Wax Tank Capacity (cu. ft)", value=1.5)
default_wax_dens = st.sidebar.number_input(
    "Wax Density (lbs/cu. ft)", value=35.0
)


# Helper function to render a custom CSS tank graphic
def render_tank_card(tank_name, percentage, weight, color="#2ecc71"):
    st.markdown(
        f"""
        <div style="border: 2px solid #e0e0e0; border-radius: 10px; padding: 15px; text-align: center; background-color: #f9f9f9; margin-bottom: 10px;">
            <h4 style="margin: 0; color: #333;">{tank_name}</h4>
            <div style="font-size: 18px; font-weight: bold; color: {color}; margin: 5px 0;">{percentage}% ≈ {weight:,.1f} lbs</div>
            <div style="width: 60px; height: 120px; border: 3px solid #555; border-radius: 6px; margin: 10px auto; position: relative; background: #fff; overflow: hidden;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {percentage}%; background-color: {color}; opacity: 0.8; transition: height 0.3s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Layout using Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Face Resin (4)", "Core Resin (2)", "Scavenger (1)", "Wax (3)", "📊 Summary"]
)

weights = {}
percentages = {}

# --- 1. FACE RESIN (216" height @ 496 lbs/in) ---
with tab1:
    st.subheader("Face Resin Tanks (4 Units - 216\" Height)")
    cols = st.columns(4)
    for i in range(1, 5):
        with cols[i - 1]:
            p = st.number_input(
                f"Tank F{i} %",
                0.0,
                100.0,
                100.0,
                key=f"face_{i}",
                label_visibility="visible",
            )
            percentages[f"Face Tank {i}"] = p
            inches_filled = (p / 100.0) * 216
            wt = inches_filled * 496
            weights[f"Face Tank {i}"] = wt
            render_tank_card(f"Tank F{i}", p, wt, color="#3498db")

# --- 2. CORE RESIN (228" height @ 1,000 lbs/in) ---
with tab2:
    st.subheader("Core Resin Tanks (2 Units - 228\" Height)")
    cols = st.columns(2)
    for i in range(1, 3):
        with cols[i - 1]:
            p = st.number_input(
                f"Tank C{i} %",
                0.0,
                100.0,
                100.0,
                key=f"core_{i}",
                label_visibility="visible",
            )
            percentages[f"Core Tank {i}"] = p
            inches_filled = (p / 100.0) * 228
            wt = inches_filled * 1000
            weights[f"Core Tank {i}"] = wt
            render_tank_card(f"Tank C{i}", p, wt, color="#f1c40f")

# --- 3. SCAVENGER (228" height @ 576 lbs/in) ---
with tab3:
    st.subheader("Scavenger Tank (1 Unit - 228\" Height)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        p = st.number_input(
            "Scavenger Tank %",
            0.0,
            100.0,
            100.0,
            key="scav_1",
            label_visibility="visible",
        )
        percentages["Scavenger Tank 1"] = p
        inches_filled = (p / 100.0) * 228
        wt = inches_filled * 576
        weights["Scavenger Tank 1"] = wt
        render_tank_card("Scavenger S1", p, wt, color="#e67e22")

# --- 4. WAX ---
with tab4:
    st.subheader("Wax Tanks (3 Units)")
    cols = st.columns(3)
    for i in range(1, 4):
        with cols[i - 1]:
            p = st.number_input(
                f"Tank W{i} %",
                0.0,
                100.0,
                100.0,
                key=f"wax_{i}",
                label_visibility="visible",
            )
            percentages[f"Wax Tank {i}"] = p
            wt = (p / 100.0) * default_wax_cap * default_wax_dens
            weights[f"Wax Tank {i}"] = wt
            render_tank_card(f"Tank W{i}", p, wt, color="#9b59b6")

# --- 5. SUMMARY ---
with tab5:
    st.subheader("📈 Total Inventory Weight Summary")
    total_weight = sum(weights.values())

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total System Weight", f"{total_weight:,.2f} lbs")
    col_m2.metric(
        "Active Tanks",
        f"{len([v for v in percentages.values() if v > 0])}/10",
    )
    col_m3.metric("Average Fill Level", f"{sum(percentages.values())/10:.1f}%")

    st.markdown("### Breakdown Table")
    summary_data = [
        {"Tank": k, "Fill %": f"{percentages[k]}%", "Weight (lbs)": f"{v:,.2f}"}
        for k, v in weights.items()
    ]
    st.table(summary_data)
