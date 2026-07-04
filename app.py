import streamlit as st
import pandas as pd
import json
from PIL import Image
from core_agents import OrchestratorAgent

# Page configuration for crisp, corporate look and feel
st.set_page_config(page_title="Market Product Trend Assistant", layout="wide")

# Master Application Theme Stylings
st.markdown("""
    <style>
    .main-header { font-size:2.2rem !important; color:#0f172a; font-weight:bold; margin-bottom: 5px; }
    .sub-header { font-size:1.1rem !important; color:#475569; margin-bottom: 25px; }
    .metric-card { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Instantiate the System Orchestrator
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent()

# Track Database state dynamically across session processes
if 'database' not in st.session_state:
    with open('mock_data.json', 'r') as f:
        st.session_state.database = json.load(f)
        # Pre-populate existing database records with agent analysis for demo consistency
        for item in st.session_state.database:
            item["extracted_ingredients"] = st.session_state.orchestrator.ingredient_agent.extract_ingredients(item["raw_claims_text"])
            item["revenue_attribution"] = st.session_state.orchestrator.revenue_agent.calculate_attribution(
                item["total_revenue_usd"], item["extracted_ingredients"]
            )

st.markdown('<div class="main-header">Market Product Trend Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Live Multi-Agent Market Intelligence for the Health & Wellness Supplements Portfolio</div>', unsafe_allow_html=True)

# --- PANEL 1: EXECUTIVE ANALYTICAL OBSERVATIONS ---
st.subheader("📊 Live Market Segment Tracking")
df = pd.DataFrame(st.session_state.database)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-card"><strong>Total Tracked SKUs</strong><br><span style="font-size:1.8rem;color:#0f172a;font-weight:bold;">{len(df)}</span></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><strong>Monitored Industry Capital</strong><br><span style="font-size:1.8rem;color:#0f172a;font-weight:bold;">${df["total_revenue_usd"].sum():,.2f}</span></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><strong>Analysis Mode</strong><br><span style="font-size:1.8rem;color:#10b981;font-weight:bold;">Real-Time</span></div>', unsafe_allow_html=True)

st.write("")
st.dataframe(df[["sku", "brand", "suggested_category", "total_revenue_usd", "raw_claims_text"]], use_container_width=True)

# --- PANEL 2: INTERACTIVE NATURAL LANGUAGE CONVERSATIONAL CORES ---
st.write("---")
st.subheader("🤖 Conversational Market Interrogation (Orchestrator Parsing)")
user_query = st.text_input("Ask anything about this market data slice:", placeholder="e.g., Show me revenue distribution metrics or ingredient insights...")
if user_query:
    response = st.session_state.orchestrator.parse_natural_language_query(user_query, st.session_state.database)
    st.info(response)

# --- PANEL 3: REAL-TIME INGESTION PIPELINE (THE DEMO HERO MECHANIC) ---
st.write("---")
st.subheader("📸 Ingest New Competitor Packaging Asset (Real-Time Extraction Pipeline)")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Step 1: Input Competitor Metadata")
    input_brand = st.text_input("Competitor Brand Name", "Optima Vitality")
    input_revenue = st.number_input("Estimated Brand Catalog Value ($ USD)", min_value=10000, value=500000, step=50000)
    uploaded_file = st.file_uploader("Upload Product Packaging Frontal Image Image (Simulation targets name 'sleep' or 'protein' for variable data paths)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Competitor Target Asset Source", width=250)

with col2:
    st.markdown("### Step 2: Multi-Agent Ingestion Output")
    if st.button("Trigger Ingestion & Run Downstream Agents"):
        if uploaded_file is None:
            st.error("Please upload an asset image to demonstrate the computer vision extraction layer loops.")
        else:
            with st.spinner("Orchestrator coordinating sub-agent workflows..."):
                # Execute the full internal multi-agent loop end-to-end
                result = st.session_state.orchestrator.process_new_packaging_pipeline(
                    uploaded_file, input_brand, input_revenue
                )
                
                # Append live parsed data records straight back into active state memory arrays
                st.session_state.database.append(result)
                
                st.success("✅ Execution complete. System architecture outputs outlined below:")
                
                st.write(f"**Orchestrator Assigned SKU ID:** `{result['sku']}`")
                st.info(f"🧬 **Product Claims Agent Extraction:** *\"{result['raw_claims_text']}\"*")
                st.warning(f"🧪 **Hero Ingredient Extractor Isolation:** {', '.join(result['extracted_ingredients'])}")
                st.success(f"🎯 **Market Matching Agent Mapping:** `{result['suggested_category']}`")
                
                st.write("**Revenue Attribution Agent Allocation Metrics:**")
                st.json(result['revenue_attribution'])
                st.balloons()