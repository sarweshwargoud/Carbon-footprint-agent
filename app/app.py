import streamlit as st
import sys
import os
import time
import pandas as pd
import json
from datetime import datetime


# Workaround for OpenMP error on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Allow importing from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from agent import generate_advice
from agent import explain_decision
from agent import generate_actionable_steps

from calculator import calculate_total_co2

# -----------------------------------------------------------------------------
# Page Config & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Carbon Footprint Agent",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern aesthetics
st.markdown("""
    <style>
    /* Global Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Center all Headings */
    h1, h2, h3 {
        text-align: center !important;
    }
    
    /* Input Fields Hover Animation */
    div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
        transition: all 0.3s ease;
        border-radius: 8px;
        padding: 2px;
    }
    
    div[data-testid="stNumberInput"]:hover, div[data-testid="stSelectbox"]:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        background-color: rgba(240, 242, 246, 0.5);
    }
    
    /* Card-like styling for metric containers with Hover Animation */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6; 
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease-in-out;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 24px rgba(46, 125, 50, 0.2);
        border: 1px solid #2E7D32;
    }
    
    /* Dark mode adjustment */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"] {
            background-color: #262730;
            box-shadow: 2px 4px 8px rgba(0,0,0,0.5);
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 12px 24px rgba(129, 199, 132, 0.2);
        }
        div[data-testid="stNumberInput"]:hover, div[data-testid="stSelectbox"]:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    }

    /* Gradient Header with Shadow and Animation */
    .header-text {
        background: linear-gradient(120deg, #1b5e20, #4caf50, #81c784);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 4rem; /* Prominent Title */
        margin-bottom: 0.2rem;
        text-align: center; /* Centered */
        text-shadow: 4px 4px 8px rgba(0,0,0,0.1);
        animation: fadeInDown 1.2s ease-out;
    }
    
    .sub-header-text {
        color: #555;
        font-size: 1.4rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
        text-align: center; /* Centered */
        animation: fadeIn 1.5s ease-out;
    }
    
    /* Button styling with Pulse Animation */
    div.stButton > button {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(56, 239, 125, 0.4);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Highlight containers */
    div[data-testid="stExpander"] {
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<div class="header-text">🌱 Carbon Footprint Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header-text">Calculate your environmental impact, visualize data, and get AI-driven sustainability advice.</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# Input Section (Dashboard Layout)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Input Section (Card Style)
# -----------------------------------------------------------------------------
with st.container(border=True):
    st.markdown("<h3 style='text-align: center;'>📝 Your Monthly Usage</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.subheader("⚡ Energy")
        electricity = st.number_input("Electricity (kWh/mo)", min_value=0.0, value=300.0, help="Check your electricity bill.")
        water = st.number_input("Water Usage (m³/mo)", min_value=0.0, value=10.0, help="Approximate monthly consumption.")

    with col2:
        st.subheader("🚗 Transport")
        petrol = st.number_input("Petrol (L/mo)", min_value=0.0, value=40.0)
        diesel = st.number_input("Diesel (L/mo)", min_value=0.0, value=0.0)
        
        with st.expander("🚌 Public Transport & Travel"):
            bus_km = st.number_input("Bus (km/mo)", min_value=0.0, value=0.0)
            train_km = st.number_input("Train (km/mo)", min_value=0.0, value=0.0)
            flight_km = st.number_input("Flight (km/mo)", min_value=0.0, value=0.0)

    with col3:
        st.subheader("🗑️ Lifestyle")
        diet = st.selectbox("Diet Type", ["Veg", "NonVeg"], help="Vegetarian diets generally have lower carbon footprints.")
        plastic = st.number_input("Plastic Waste (kg/mo)", min_value=0.0, value=5.0)
        ewaste = st.number_input("E-waste (kg/mo)", min_value=0.0, value=0.0)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Calculate Button (Centered)
# -----------------------------------------------------------------------------
b_c1, b_c2, b_c3 = st.columns([1, 2, 1])
calculate_clicked = False

with b_c2:
    if st.button("🚀 Calculate Carbon Footprint", use_container_width=True):
        calculate_clicked = True
        with st.spinner("Analyzing your lifestyle..."):
            time.sleep(1)

if calculate_clicked:
    # Prepare Data
    user_data = {
        "electricity_kwh": electricity,
        "petrol_liters": petrol,
        "diesel_liters": diesel,
        "bus_km": bus_km,
        "train_km": train_km,
        "flight_km": flight_km,
        "diet": diet.lower(),
        "plastic_kg": plastic,
        "ewaste_kg": ewaste,
        "water_m3": water,
        "days": 30
    }

    # Calculate
    breakdown, percentages, highest = calculate_total_co2(user_data)
    
    # Save results to session state
    st.session_state['breakdown'] = breakdown
    st.session_state['percentages'] = percentages
    st.session_state['highest'] = highest
    st.session_state['results_ready'] = True

# -----------------------------------------------------------------------------
# Results Display
# -----------------------------------------------------------------------------
if st.session_state.get('results_ready'):
    breakdown = st.session_state['breakdown']
    percentages = st.session_state['percentages']
    highest = st.session_state['highest']

    st.markdown("---")
    
    # Section 1: Key Metrics
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>📊 Emissions Summary</h3>", unsafe_allow_html=True)
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="Monthly Emissions", value=f"{breakdown['monthly_total']} kg CO₂")
        with m_col2:
            st.metric(label="Yearly Projection", value=f"{breakdown['yearly_total']} kg CO₂")
        with m_col3:
            st.metric(label="Top Contributor", value=f"{highest.capitalize()}", delta="Highest Impact", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 2: Visualizations & Analysis
    row2_col1, row2_col2 = st.columns([2, 1], gap="medium")
    
    with row2_col1:
        with st.container(border=True):
            st.markdown("#### 🔍 Emission Breakdown")
            chart_data = pd.DataFrame({
                "Category": ["Electricity", "Transport", "Food", "Waste", "Water"],
                "Emissions (kg)": [breakdown["electricity"], breakdown["transport"], breakdown["food"], breakdown["waste"], breakdown["water"]]
            })
            st.bar_chart(chart_data.set_index("Category"), color="#2E7D32")

    with row2_col2:
        with st.container(border=True):
            st.markdown(f"#### 🔥 Primary Offender: **{highest.capitalize()}**")
            st.info(f"Contributing **{percentages[highest]}%** of your total emissions.")
            
            if highest == "electricity":
                st.warning("💡 **Quick Fix:** Switch to LED bulbs.")
            elif highest == "transport":
                st.warning("🚴 **Quick Fix:** Carpool or Walk.")
            elif highest == "food":
                st.warning("🥗 **Quick Fix:** Meat-free Mondays.")
            elif highest == "waste":
                st.warning("♻️ **Quick Fix:** Recycle plastics.")
            elif highest == "water":
                st.warning("💧 **Quick Fix:** Fix leaks.")
            
            explanation = explain_decision(breakdown, percentages, highest)
            with st.expander("🧠 Why is this highest?"):
                st.write(explanation)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 3: AI Plan
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>🤖 AI Reduction Strategy</h3>", unsafe_allow_html=True)
        advice = generate_advice(breakdown, percentages, highest)
        st.info(advice)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 4: Actionable Steps
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>🚀 Your Action Plan</h3>", unsafe_allow_html=True)
        steps = generate_actionable_steps(breakdown, percentages, highest)
        
        # Split steps into columns for better readability if possible, or just markdown
        st.markdown(steps)

    st.markdown("<br>", unsafe_allow_html=True)

    # Section 5: Impact & Export
    with st.container(border=True):
        st.subheader("🌍 Sustainability Status")

        if breakdown["yearly_total"] < 2000:
            st.success("✅ **Eco-Warrior:** Your footprint is LOW. Keep it up!")
        elif breakdown["yearly_total"] < 4000:
            st.warning("⚠️ **Average:** Your footprint is MODERATE. Room for improvement.")
        else:
            st.error("🚨 **High Impact:** Immediate lifestyle changes recommended.")
        
        reduction_potential = round(breakdown["yearly_total"] * (percentages[highest] / 100) * 0.3, 2)
        st.write(f"📉 **Potential Savings:** Reducing **{highest}** by 30% saves **{reduction_potential} kg CO₂/year**.")

        st.markdown("---")
        st.markdown("### 📥 Export Your Report")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("💾 Save to System", use_container_width=True):
                report = {
                    "breakdown": breakdown,
                    "percentages": percentages,
                    "highest_source": highest,
                    "timestamp": str(datetime.now())
                }
                output_dir = "outputs/user_reports"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                report_path = f"{output_dir}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                try:
                    with open(report_path, "w") as f:
                        json.dump(report, f, indent=4)
                    st.success(f"Saved: `{report_path}`")
                except Exception as e:
                    st.error(str(e))

        with col_exp2:
            report_json = json.dumps({
                    "breakdown": breakdown,
                    "percentages": percentages,
                    "highest_source": highest,
                    "timestamp": str(datetime.now())
                }, indent=4)
            st.download_button(
                label="⬇️ Download JSON",
                data=report_json,
                file_name=f"carbon_report_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
