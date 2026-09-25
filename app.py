import streamlit as st

st.set_page_config(
    page_title="Tank Media Inventory Calculator", page_icon="⚖️", layout="wide"
)

st.title("⚖️ Tank Inventory: Percentage to Weight Converter")
st.markdown(
    "Enter the fill percentage and customize the total capacity / density for each tank group below."
)

# Sidebar for global default configurations
st.sidebar.header("⚙️ Default Settings")
default_face_cap = st.sidebar.number_input(
    "Default Face Resin Tank Capacity (cu. ft)", value=2.5
)
default_face_dens = st.sidebar.number_input(
    "Default Face Resin Density (lbs/cu. ft)", value=50.0
)

default_core_cap = st.sidebar.number_input(
    "Default Core Resin Tank Capacity (cu. ft)", value=3.0
)
default_core_dens = st.sidebar.number_input(
    "Default Core Resin Density (lbs/cu. ft)", value=52.0
)

default_scav_cap = st.sidebar.number_input(
    "Default Scavenger Tank Capacity (cu. ft)", value=2.0
)
default_scav_dens = st.sidebar.number_input(
    "Default Scavenger Density (lbs/cu. ft)", value=45.0
)

default_wax_cap = st.sidebar.number_input(
    "Default Wax Tank Capacity (cu. ft)", value=1.5
)
default_wax_dens = st.sidebar.number_input(
    "Default Wax Density (lbs/cu. ft)", value=35.0
)

# Layout using Tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Face Resin (4)", "Core Resin (2)", "Scavenger (1)", "Wax (3)", "📊 Summary"]
)

# Store inputs globally in session state simulation via dicts
weights = {}
percentages = {}

# --- 1. FACE RESIN (4 Tanks) ---
with tab1:
    st.subheader("Face Resin Tanks (4 Units)")
    col1, col2 = st.columns(2)
    face_percentages = []
    for i in range(1, 5):
        with col1 if i <= 2 else col2:
            st.markdown(f"**Tank F{i}**")
            p = st.number_input(
                f"Fill % (Tank F{i})",
                0.0,
                100.0,
                100.0,
                key=f"face_{i}",
                label_visibility="collapsed",
            )
            percentages[f"Face Tank {i}"] = p
            wt = (p / 100.0) * default_face_cap * default_face_dens
            weights[f"Face Tank {i}"] = wt
            st.text(f"Weight: {wt:.2f} lbs")
            st.divider()

# --- 2. CORE RESIN (2 Tanks) ---
with tab2:
    st.subheader("Core Resin Tanks (2 Units)")
    for i in range(1, 3):
        st.markdown(f"**Tank C{i}**")
        p = st.number_input(
            f"Fill % (Tank C{i})",
            0.0,
            100.0,
            100.0,
            key=f"core_{i}",
            label_visibility="collapsed",
        )
        percentages[f"Core Tank {i}"] = p
        wt = (p / 100.0) * default_core_cap * default_core_dens
        weights[f"Core Tank {i}"] = wt
        st.text(f"Weight: {wt:.2f} lbs")
        st.divider()

# --- 3. SCAVENGER (1 Tank) ---
with tab3:
    st.subheader("Scavenger Tank (1 Unit)")
    p = st.number_input(
        "Fill % (Scavenger Tank)",
        0.0,
        100.0,
        100.0,
        key="scav_1",
        label_visibility="collapsed",
    )
    percentages["Scavenger Tank 1"] = p
    wt = (p / 100.0) * default_scav_cap * default_scav_dens
    weights["Scavenger Tank 1"] = wt
    st.text(f"Weight: {wt:.2f} lbs")

# --- 4. WAX (3 Tanks) ---
with tab4:
    st.subheader("Wax Tanks (3 Units)")
    col1, col2 = st.columns(2)
    for i in range(1, 4):
        with col1 if i <= 2 else col2:
            st.markdown(f"**Tank W{i}**")
            p = st.number_input(
                f"Fill % (Tank W{i})",
                0.0,
                100.0,
                100.0,
                key=f"wax_{i}",
                label_visibility="collapsed",
            )
            percentages[f"Wax Tank {i}"] = p
            wt = (p / 100.0) * default_wax_cap * default_wax_dens
            weights[f"Wax Tank {i}"] = wt
            st.text(f"Weight: {wt:.2f} lbs")
            st.divider()

# --- 5. SUMMARY ---
with tab5:
    st.subheader("📈 Total Inventory Weight Summary")

    total_weight = sum(weights.values())

    # Display totals metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total System Weight", f"{total_weight:,.2f} lbs")
    col_m2.metric(
        "Total Active Tanks", f"{len([v for v in percentages.values() if v > 0])}/10"
    )
    col_m3.metric("Average Fill Level", f"{sum(percentages.values())/10:.1f}%")

    st.markdown("### Breakdown by Tank")
    summary_data = [
        {"Tank": k, "Fill %": f"{percentages[k]}%", "Weight (lbs)": f"{v:,.2f}"}
        for k, v in weights.items()
    ]
    st.table(summary_data)