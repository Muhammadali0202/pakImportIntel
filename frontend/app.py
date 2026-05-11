import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import json
import time
from utils.api_client import get_shipments, estimate_duties, chat_query, upload_document

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="CargoSense",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to CargoSense. I am your Pakistan Import Intelligence AI. How can I assist you with your shipments today?"}]
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
if "route_info" not in st.session_state:
    st.session_state.route_info = {
        "origin": [22.5431, 114.0579],
        "destination": [24.8607, 67.0011],
    }
if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "AI Chat"

# Intelligence placeholders
for key in ['intel_origin', 'intel_destination', 'intel_hs_code', 'intel_declared_value', 'intel_consignee', 'intel_shipment_type', 'intel_status']:
    if key not in st.session_state:
        st.session_state[key] = "—"

default_cif = 15000000
# Try to fetch real duty estimation from backend; fallback to zeroes if unavailable.
res = estimate_duties(default_cif, "CN", "8517.13")
if res and "raw_data" in res:
    default_duties = res["raw_data"]
else:
    default_duties = {
        "CIF Value": default_cif,
        "Customs Duty (CD) @ 20%": 0,
        "Regulatory Duty (RD) @ 5%": 0,
        "Additional Customs Duty (ACD) @ 2%": 0,
        "Sales Tax (ST) @ 18%": 0,
        "Withholding Tax (WHT)": 0,
        "Total Taxes": 0,
        "Landed Cost": default_cif
    }

if "current_metrics" not in st.session_state:
    st.session_state.current_metrics = {
        "total_duty_pkr": default_duties["Total Taxes"],
        "wht_pkr": default_duties["Withholding Tax (WHT)"],
        "cif_pkr": default_duties["CIF Value"],
        "landed_cost_pkr": default_duties["Landed Cost"]
    }
if "detailed_duty" not in st.session_state:
    st.session_state.detailed_duty = default_duties
if "current_alerts" not in st.session_state:
    st.session_state.current_alerts = ["SBP reduces LC margins for telecom imports by 10%."]
if "current_risk" not in st.session_state:
    st.session_state.current_risk = {
        "level": "Medium",
        "alerts": ["Port Qasim Congestion: 48h delay", "Strait of Malacca: Piracy advisory active"]
    }

# -----------------------------------------------------------------------------
# DYNAMIC CSS (THEME ENGINE)
# -----------------------------------------------------------------------------
if st.session_state.theme == "Dark":
    bg_color = "#0A1128"
    surface_color = "#011627"
    border_color = "#1E2D3D"
    text_primary = "#E6F1FF"
    text_secondary = "#8B9BB4"
    accent_color = "#00A6FB"
    accent_hover = "#05D9E8"
    danger_color = "#F28B82"
    warning_color = "#FDE293"
    success_color = "#81C995"
else:
    bg_color = "#F0F4F8"
    surface_color = "#FFFFFF"
    border_color = "#D9E2EC"
    text_primary = "#102A43"
    text_secondary = "#486581"
    accent_color = "#2680EB"
    accent_hover = "#186ADE"
    danger_color = "#B3261E"
    warning_color = "#B38200"
    success_color = "#146C2E"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* Base theme */
.stApp {{
    background-color: {bg_color};
    color: {text_primary};
    font-family: 'Inter', sans-serif !important;
}}

/* Hide default sidebar to use custom left column navigation */
[data-testid="collapsedControl"] {{ display: none; }}
[data-testid="stSidebar"] {{ display: none; }}

/* Cards & Containers */
.css-1r6slb0, .css-12oz5g7, div[data-testid="stVerticalBlock"] > div.element-container > div.stMarkdown > div > div > div.card {{
    background-color: {surface_color};
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid {border_color};
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

/* Headers & Text */
h1, h2, h3, h4, h5, h6 {{ 
    color: {text_primary} !important; 
    font-family: 'Inter', sans-serif !important;
    font-weight: 500;
}}
p, span, div {{ 
    color: {text_primary}; 
    font-family: 'Inter', sans-serif;
}}

/* Custom metrics */
.metric-container {{
    background-color: {surface_color};
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid {border_color};
    margin-bottom: 0.5rem;
}}
.metric-label {{
    color: {text_secondary};
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
}}
.metric-value {{
    color: {text_primary};
    font-size: 1.25rem;
    font-weight: 600;
}}
.metric-value.accent {{
    color: {accent_color};
}}

/* File Uploader */
[data-testid="stFileUploader"] > section,
[data-testid="stFileUploadDropzone"] {{
    background-color: {surface_color} !important;
    border: 1px dashed {border_color} !important;
    border-radius: 12px !important;
}}
[data-testid="stFileUploadDropzone"] * {{
    color: {text_primary} !important;
}}
[data-testid="stFileUploadDropzone"] svg {{
    fill: {text_primary} !important;
    color: {text_primary} !important;
}}
[data-testid="stFileUploadDropzone"] button {{
    background-color: {accent_color} !important;
    color: #FFFFFF !important;
    border: none !important;
}}
[data-testid="stFileUploadDropzone"] button * {{
    color: #FFFFFF !important;
}}
[data-testid="stFileUploadDropzone"] button svg {{
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}}
[data-testid="stUploadedFile"] {{
    background-color: {bg_color} !important;
    color: {text_primary} !important;
    border: 1px solid {border_color} !important;
}}
[data-testid="stUploadedFile"] * {{
    color: {text_primary} !important;
}}
[data-testid="stUploadedFile"] svg {{
    fill: {text_primary} !important;
}}


/* Chat Input */
[data-testid="stChatInput"] {{
    background-color: {surface_color};
    border: 1px solid {border_color};
    border-radius: 24px;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 24px;
    background-color: transparent;
}}
.stTabs [data-baseweb="tab"] {{
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: {text_secondary};
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    background-color: transparent;
    color: {accent_color} !important;
    border-bottom: 2px solid {accent_color};
}}

/* Source Panel Specifics */
.source-panel-header {{
    font-size: 0.9rem;
    font-weight: 600;
    color: {text_secondary};
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.extracted-intel-card {{
    background-color: {surface_color};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
}}
.intel-item {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}}
.intel-key {{ color: {text_secondary}; }}
.intel-val {{ color: {text_primary}; font-weight: 500; }}

/* Premium Chat Bubbles */
[data-testid="stChatMessage"] {{
    background-color: {surface_color} !important;
    border: 1px solid {border_color} !important;
    border-radius: 16px !important;
    margin-bottom: 12px !important;
    padding: 1rem !important;
}}

/* Distinguish User and Assistant */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background-color: rgba(0, 166, 251, 0.05) !important;
    border: 1px solid rgba(0, 166, 251, 0.2) !important;
}}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background-color: {surface_color} !important;
    border: 1px solid {border_color} !important;
}}

[data-testid="stChatMessage"] .stMarkdown p {{
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    color: {text_primary} !important;
}}

/* Code Blocks & Tables in Chat */
pre {{
    background-color: {bg_color} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}}
th, td {{
    padding: 8px 12px;
    border: 1px solid {border_color};
    text-align: left;
}}
th {{ background-color: rgba(0, 166, 251, 0.1); }}

/* Status indicators */
.status-badge-transit {{ color: {accent_color}; font-weight: 500; }}
.status-badge-hold {{ color: {danger_color}; font-weight: 500; }}
.status-badge-delay {{ color: {warning_color}; font-weight: 500; }}
.status-badge-clear {{ color: {success_color}; font-weight: 500; }}

.legend-strip {{
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background-color: {surface_color};
    border: 1px solid {border_color};
    border-radius: 8px;
    margin-top: -10px;
    margin-bottom: 10px;
    font-size: 0.75rem;
}}
.legend-item {{ display: flex; align-items: center; gap: 5px; color: {text_secondary}; }}
.legend-color {{ width: 8px; height: 8px; border-radius: 50%; }}

.threat-overview {{
    background-color: {surface_color};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 1rem;
    margin-top: 10px;
}}
.threat-overview h5 {{ color: {text_primary} !important; margin-top: 0; font-size: 0.9rem; }}
.threat-overview ul {{ margin-bottom: 0; padding-left: 20px; font-size: 0.85rem; color: {text_secondary}; }}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS & MOCK DATA
# -----------------------------------------------------------------------------

def format_pkr(amount):
    """Format large numbers into PKR shorthand (e.g., Rs 2.7M)"""
    try:
        amount = float(amount)
        if amount >= 1_000_000:
            return f"Rs {amount/1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"Rs {amount/1_000:.0f}K"
        return f"Rs {amount:,.0f}"
    except (ValueError, TypeError):
        return amount

def classify_intent(query):
    query = query.lower()
    if any(k in query for k in ['track', 'where', 'status', 'eta', 'delay']):
        return 'shipment_tracking'
    elif any(k in query for k in ['duty', 'tax', 'wht', 'calculate', 'cost', 'cif']):
        return 'duty_calculation'
    elif any(k in query for k in ['route', 'compare', 'air', 'sea', 'colombo', 'dubai']):
        return 'route_recommendation'
    elif any(k in query for k in ['document', 'invoice', 'hs code', 'declared']):
        return 'document_question'
    return 'general'

def send_query(query, context=None):
    """Dual Mode API System: Tries FastAPI, falls back to intelligent mock JSON"""
    response = chat_query(query, context)
    if response:
        # Backend returns 'response' key — normalize to 'answer' for UI consistency
        if "response" in response and "answer" not in response:
            response["answer"] = response.pop("response")
        return response
    else:
        # Fallback if backend is unreachable
        time.sleep(0.5) # Simulate API latency
        intent = classify_intent(query)
        
        cif_val = 15000000 # 15M PKR
        mock_response = {
            "answer": "I have analyzed your request. (Backend offline, using fallback data)",
            "citations": [],
            "route_info": {
                "origin": [22.5431, 114.0579],
                "destination": [24.8607, 67.0011],
                "midpoint": [23.7, 90.5],
                "status": "IN_TRANSIT",
                "threat_level": "Medium"
            },
            "risk_profile": {
                "level": "Medium",
                "alerts": ["Port Qasim Congestion: 48h delay"]
            },
            "trade_alerts": [
                "SBP reduces LC margins for telecom imports by 10%."
            ],
            "financial_metrics": {
                "total_duty_pkr": 0,
                "wht_pkr": 0,
                "cif_pkr": cif_val,
                "landed_cost_pkr": cif_val
            },
            "detailed_duty": {}
        }
        return mock_response

def build_map(route_info=None):
    # Use light or dark tiles based on theme
    tiles = "CartoDB positron" if st.session_state.theme == "Light" else "CartoDB dark_matter"
    m = folium.Map(location=[20.0, 90.0], zoom_start=4, tiles=tiles)
    if route_info:
        origin = route_info.get("origin", [22.5431, 114.0579])
        dest = route_info.get("destination", [24.8607, 67.0011])
        folium.Marker(origin, popup="Origin: Shenzhen", icon=folium.Icon(color="blue")).add_to(m)
        folium.Marker(dest, popup="Destination: Karachi", icon=folium.Icon(color="green")).add_to(m)
        
        midpoint = [(origin[0] + dest[0])/2, (origin[1] + dest[1])/2]
        folium.Marker(midpoint, popup="Current Location", icon=folium.Icon(color="orange")).add_to(m)
        folium.PolyLine([origin, dest], color=accent_color, weight=2.5, opacity=0.8).add_to(m)
        m.fit_bounds([origin, dest])
    return m

# Mock Shipments Data
mock_shipments = pd.DataFrame([
    {"ID": "SHP-883", "ETA": "2024-10-15", "Status": "IN_TRANSIT", "Delay": "None", "Route": "Shenzhen to Karachi"},
    {"ID": "SHP-884", "ETA": "2024-10-12", "Status": "CUSTOMS_HOLD", "Delay": "Valuation Check", "Route": "Dubai to Karachi"},
    {"ID": "SHP-885", "ETA": "2024-10-10", "Status": "PORT_CONGESTION", "Delay": "Berth Unavailable", "Route": "Shanghai to Karachi"},
    {"ID": "SHP-886", "ETA": "2024-10-08", "Status": "CLEARED", "Delay": "None", "Route": "Ningbo to Karachi"},
    {"ID": "SHP-887", "ETA": "2024-10-01", "Status": "DELIVERED", "Delay": "None", "Route": "Singapore to Karachi"},
    {"ID": "SHP-888", "ETA": "2024-10-20", "Status": "IN_TRANSIT", "Delay": "None", "Route": "Jebel Ali to Karachi"},
])

# -----------------------------------------------------------------------------
# MAIN LAYOUT
# -----------------------------------------------------------------------------
col_left, col_center, col_right = st.columns([1, 2, 1.5], gap="large")

# ==========================================
# LEFT COLUMN — SOURCE PANEL
# ==========================================
with col_left:
    st.markdown(f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:1rem;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{{accent_color}}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg><div class="source-panel-header" style="margin:0; font-size:1.1rem; color:{{text_primary}}; text-transform:none; letter-spacing:0;">CargoSense Intel</div></div>', unsafe_allow_html=True)
    
    # Theme Toggle
    theme_sel = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True)
    if theme_sel != st.session_state.theme:
        st.session_state.theme = theme_sel
        st.rerun()
        
    st.markdown("---")
    
    st.markdown('<div class="source-panel-header">Sources</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Documents", type=["pdf", "jpg", "png", "jpeg"], label_visibility="collapsed")
    if uploaded_file and uploaded_file.name not in st.session_state.uploaded_docs:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            result = upload_document(uploaded_file.getvalue(), uploaded_file.name)
            if result and result.get("status") == "success":
                st.session_state.uploaded_docs.append(uploaded_file.name)
                st.success(f"✅ {uploaded_file.name} ingested.")
                
                # Immediately update metrics and intel from the uploaded document
                ai_response = result.get("extracted_intel", {})
                if ai_response:
                    # 1. Update Left Sidebar (Active Intel)
                    intel = ai_response.get("extracted_intel", {})
                    if isinstance(intel, dict):
                        st.session_state.intel_origin = intel.get("origin", st.session_state.intel_origin)
                        st.session_state.intel_destination = intel.get("destination", st.session_state.intel_destination)
                        st.session_state.intel_hs_code = intel.get("hs_code", st.session_state.intel_hs_code)
                        st.session_state.intel_declared_value = intel.get("declared_value", st.session_state.intel_declared_value)
                        st.session_state.intel_consignee = intel.get("consignee", st.session_state.intel_consignee)
                        st.session_state.intel_shipment_type = intel.get("shipment_type", st.session_state.intel_shipment_type)
                        st.session_state.intel_status = intel.get("status", st.session_state.intel_status)
                    
                    # 2. Update Right Column (Financial Intelligence)
                    if "financial_metrics" in ai_response:
                        metrics = ai_response["financial_metrics"]
                        if metrics.get("total_duty_pkr") != 0:
                            st.session_state.current_metrics = metrics
                            
                    # 3. Update Intelligence Tabs (Risk/Alerts)
                    if "risk_profile" in ai_response:
                        st.session_state.current_risk = ai_response["risk_profile"]
                    if "trade_alerts" in ai_response:
                        st.session_state.current_alerts = ai_response["trade_alerts"]
                        
                    # 4. Update Tactical Map
                    if "route_info" in ai_response:
                        st.session_state.route_info = ai_response["route_info"]
                
                st.rerun()
            else:
                st.error(f"❌ Failed to process {uploaded_file.name}. Is the backend running?")

    if st.session_state.uploaded_docs:
        for doc in st.session_state.uploaded_docs:
            st.markdown(f"<span style='font-size:0.85rem;'>📄 {doc}</span>", unsafe_allow_html=True)
    else:
        st.caption("No sources uploaded yet.")
        
    st.markdown("---")
    
    st.markdown('<div class="source-panel-header">Navigation</div>', unsafe_allow_html=True)
    nav_options = ["AI Chat", "Dashboard", "Duty Calculator", "Route Comparison"]
    selected_nav = st.radio("Menu", nav_options, label_visibility="collapsed", key="nav_radio", index=nav_options.index(st.session_state.nav_selection))
    if selected_nav != st.session_state.nav_selection:
        st.session_state.nav_selection = selected_nav
        st.rerun()
    
    st.markdown(f"""
        <div class="extracted-intel-card">
            <h5 style="margin-top:0; margin-bottom:12px; color:{text_primary};">Active Intel</h5>
            <div class="intel-item"><span class="intel-key">Origin</span><span class="intel-val">{st.session_state.get('intel_origin', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">Destination</span><span class="intel-val">{st.session_state.get('intel_destination', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">HS Code</span><span class="intel-val">{st.session_state.get('intel_hs_code', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">Declared Value</span><span class="intel-val">{st.session_state.get('intel_declared_value', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">Consignee</span><span class="intel-val">{st.session_state.get('intel_consignee', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">Shipment Type</span><span class="intel-val">{st.session_state.get('intel_shipment_type', '—')}</span></div>
            <div class="intel-item"><span class="intel-key">Customs Status</span><span class="intel-val">{st.session_state.get('intel_status', '—')}</span></div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# CENTER COLUMN — AI WORKSPACE
# ==========================================
with col_center:
    st.markdown(f"<h3 style='color: {text_primary}; margin-bottom: 24px;'>{st.session_state.nav_selection}</h3>", unsafe_allow_html=True)
    
    if st.session_state.nav_selection == "Dashboard":
        # Fetch live shipments from backend; fall back to empty table if offline
        live_data = get_shipments()
        if live_data:
            shipments_df = pd.DataFrame(live_data)
        else:
            shipments_df = pd.DataFrame(columns=["id", "status", "eta", "current_location", "origin", "destination"])
            st.warning("⚠️ Backend offline — no shipment data available.")
        st.dataframe(
            shipments_df,
            use_container_width=True,
            hide_index=True
        )
        
    elif st.session_state.nav_selection == "Route Comparison":
        origin = st.session_state.intel_origin if st.session_state.intel_origin != "—" else "Shenzhen"
        dest = st.session_state.intel_destination if st.session_state.intel_destination != "—" else "Karachi"
        
        st.markdown(f"##### Route Alternatives: {origin} to {dest}")
        
        if st.session_state.uploaded_docs:
            with st.spinner("Calculating optimal routes based on documents..."):
                analysis_query = f"Compare shipping routes from {origin} to {dest} based on current document context and provide the most balanced recommendation."
                analysis = send_query(analysis_query)
                st.write(analysis.get("answer", "Analysis unavailable."))
        
        routes = pd.DataFrame([
            {"Route": "Direct Sea", "ETA": "14 Days", "Cost": "$1,200", "Congestion": "Low", "Recommendation": "Optimal"},
            {"Route": "Sea via Colombo", "ETA": "17 Days", "Cost": "$1,000", "Congestion": "High", "Recommendation": "Risk of Delay"},
            {"Route": "Air via Dubai", "ETA": "2 Days", "Cost": "$4,500", "Congestion": "None", "Recommendation": "Fastest"},
        ])
        st.dataframe(routes, use_container_width=True, hide_index=True)
        
        if not st.session_state.uploaded_docs:
            st.info("Analysis: Direct Sea is the most balanced. Air freight is 3.7x more expensive but saves 12 days. Colombo route is cheaper but carries a high risk of port congestion delays.")

    elif st.session_state.nav_selection == "Duty Calculator":
        st.markdown("##### Duty Estimation Parameters")
        with st.form("duty_calc_form"):
            col1, col2 = st.columns(2)
            with col1:
                cif_input = st.number_input("CIF Value (PKR)", value=15000000, step=100000)
                hs_code_input = st.text_input("HS Code", value="8517.13")
            with col2:
                filer_status = st.selectbox("Filer Status", ["Filer (Active)", "Non-Filer"])
                product_desc = st.text_input("Product Description", value="Smartphones")
                
            submitted = st.form_submit_button("Calculate Duties", type="primary")
            
        if submitted:
            is_filer = filer_status == "Filer (Active)"
            response = estimate_duties(cif_input, product_hs_code=hs_code_input, is_filer=is_filer)
            
            if response and "raw_data" in response:
                calculated_duties = response["raw_data"]
                # Update session state metrics
                st.session_state.current_metrics = {
                    "total_duty_pkr": calculated_duties["Total Taxes"],
                    "wht_pkr": calculated_duties["Withholding Tax (WHT)"],
                    "cif_pkr": calculated_duties["CIF Value"],
                    "landed_cost_pkr": calculated_duties["Landed Cost"]
                }
                st.session_state.detailed_duty = calculated_duties
                st.success("Duties recalculated successfully. See Financial Intelligence panel for details.")
            else:
                st.error("Failed to calculate duties. Please check if the backend is running.")
            
        st.markdown("##### Duty Breakdown")
        duty_df = pd.DataFrame(list(st.session_state.detailed_duty.items()), columns=["Tax Component", "Amount (PKR)"])
        duty_df["Amount (PKR)"] = duty_df["Amount (PKR)"].apply(lambda x: format_pkr(x))
        st.dataframe(duty_df, hide_index=True, use_container_width=True)

    else:
        # AI Chat Workspace - Expanded for rich Markdown content
        chat_container = st.container(height=800)
        
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if "citations" in msg and msg["citations"]:
                        st.caption(f"Sources: {', '.join(msg['citations'])}")
        
        if prompt := st.chat_input("Ask about duties, tracking, or documents..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)
                    
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing Intelligence Reports..."):
                        # Get live data from backend
                        raw_response = chat_query(prompt, context={"docs": st.session_state.uploaded_docs})
                        
                        # Defensive parsing
                        if raw_response and isinstance(raw_response, dict):
                            response_data = raw_response
                            answer = response_data.get("answer", "I received a valid data payload but no textual answer was provided.")
                        elif isinstance(raw_response, str):
                            # In case the backend returns a raw string instead of the JSON object
                            answer = raw_response
                            response_data = {"answer": answer}
                        else:
                            answer = "I'm sorry, I'm having trouble connecting to my intelligence base right now. Please verify if the backend is online."
                            response_data = {"answer": answer}

                        st.markdown(answer)
                        if response_data.get("citations"):
                            st.caption(f"Sources: {', '.join(response_data['citations'])}")
                            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": answer,
                "citations": response_data.get("citations", []) if isinstance(response_data, dict) else []
            })
            
            if "route_info" in response_data:
                st.session_state.route_info = response_data["route_info"]
            if "financial_metrics" in response_data:
                st.session_state.current_metrics = response_data["financial_metrics"]
            if "detailed_duty" in response_data:
                st.session_state.detailed_duty = response_data["detailed_duty"]
            if "trade_alerts" in response_data:
                st.session_state.current_alerts = response_data["trade_alerts"]
            if "risk_profile" in response_data:
                st.session_state.current_risk = response_data["risk_profile"]
            if "extracted_intel" in response_data:
                # Handle both direct and nested extraction
                intel = response_data["extracted_intel"]
                if isinstance(intel, dict):
                    st.session_state.intel_origin = intel.get("origin", st.session_state.intel_origin)
                    st.session_state.intel_destination = intel.get("destination", st.session_state.intel_destination)
                    st.session_state.intel_hs_code = intel.get("hs_code", st.session_state.intel_hs_code)
                    st.session_state.intel_declared_value = intel.get("declared_value", st.session_state.intel_declared_value)
                    st.session_state.intel_consignee = intel.get("consignee", st.session_state.intel_consignee)
                    st.session_state.intel_shipment_type = intel.get("shipment_type", st.session_state.intel_shipment_type)
                    st.session_state.intel_status = intel.get("status", st.session_state.intel_status)

            st.rerun()

# ==========================================
# RIGHT COLUMN — TACTICAL INTELLIGENCE
# ==========================================
with col_right:
    # A. Dynamic Map & Legend
    st.markdown('<div class="source-panel-header">Tactical Map</div>', unsafe_allow_html=True)
    m = build_map(st.session_state.route_info)
    st_folium(m, height=250, width=None, returned_objects=[])
    
    st.markdown(f"""
        <div class="legend-strip">
            <div class="legend-item"><div class="legend-color" style="background-color: {danger_color};"></div> High Risk</div>
            <div class="legend-item"><div class="legend-color" style="background-color: {warning_color};"></div> Medium Risk</div>
            <div class="legend-item"><div class="legend-color" style="background-color: {success_color};"></div> Safe</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="threat-overview">
            <h5>Live Threat Overview</h5>
            <ul>
                <li><strong>Gulf of Aden:</strong> Houthi threat active. High rerouting probability.</li>
                <li><strong>Strait of Hormuz:</strong> Heightened military presence.</li>
                <li><strong>Port Qasim:</strong> Minor congestion reported.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # B. Financial Metrics
    st.markdown('<div class="source-panel-header">Financial Intelligence</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f'<div class="metric-container"><div class="metric-label">Total Duty</div><div class="metric-value">{format_pkr(st.session_state.current_metrics["total_duty_pkr"])}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><div class="metric-label">WHT</div><div class="metric-value">{format_pkr(st.session_state.current_metrics["wht_pkr"])}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-container"><div class="metric-label">CIF Value</div><div class="metric-value">{format_pkr(st.session_state.current_metrics["cif_pkr"])}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-container"><div class="metric-label">Landed Cost</div><div class="metric-value accent">{format_pkr(st.session_state.current_metrics["landed_cost_pkr"])}</div></div>', unsafe_allow_html=True)
        
    # C. Intelligence Tabs
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(['Risk Profile', 'Detailed Duty', 'Trade Alerts'])
    
    with tab1:
        st.markdown("##### Live Threat Level")
        risk_level = st.session_state.current_risk.get("level", "Low")
        risk_color = danger_color if risk_level == "High" else (warning_color if risk_level == "Medium" else success_color)
        st.markdown(f"<h4 style='color:{risk_color}; margin-top:0;'>{risk_level}</h4>", unsafe_allow_html=True)
        
        st.markdown("##### Maritime Alerts")
        for alert in st.session_state.current_risk.get("alerts", []):
            st.info(alert)
        
    with tab2:
        st.markdown("##### Line-by-Line Duty Breakdown")
        duty_df = pd.DataFrame(list(st.session_state.detailed_duty.items()), columns=["Tax Component", "Amount (PKR)"])
        duty_df["Amount (PKR)"] = duty_df["Amount (PKR)"].apply(lambda x: format_pkr(x))
        st.dataframe(duty_df, hide_index=True, use_container_width=True)
        
    with tab3:
        st.markdown("##### Trade Policy Updates")
        for alert in st.session_state.current_alerts:
            st.info(f"Update: {alert}")
