import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import json
import time

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

def calculate_duties(cif_value, hs_code="8517.13", is_filer=True):
    """Pakistan Duty Calculator Engine"""
    cd = cif_value * 0.20
    rd = cif_value * 0.05
    acd = (cif_value + cd + rd) * 0.02
    st_tax = (cif_value + cd + rd + acd) * 0.18
    
    wht_rate = 0.055 if is_filer else 0.09
    wht = (cif_value + cd + rd) * wht_rate
    
    total_duty = cd + rd + acd + st_tax + wht
    landed_cost = cif_value + total_duty
    
    return {
        "CIF Value": cif_value,
        "Customs Duty (CD) @ 20%": cd,
        "Regulatory Duty (RD) @ 5%": rd,
        "Additional Customs Duty (ACD) @ 2%": acd,
        "Sales Tax (ST) @ 18%": st_tax,
        "Withholding Tax (WHT)": wht,
        "Total Taxes": total_duty,
        "Landed Cost": landed_cost
    }

default_cif = 15000000
default_duties = calculate_duties(default_cif, "8517.13", True)

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
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/query",
            json={"query": query, "context": context},
            timeout=1
        )
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError):
        time.sleep(0.5) # Simulate API latency
        intent = classify_intent(query)
        
        cif_val = 15000000 # 15M PKR
        duties = calculate_duties(cif_val, "8517.13", True)
        
        mock_response = {
            "answer": "I have analyzed your request.",
            "citations": ["Commercial_Invoice_001.pdf", "Customs_Tariff_2024.pdf"],
            "route_info": {
                "origin": [22.5431, 114.0579], # Shenzhen
                "destination": [24.8607, 67.0011], # Karachi
                "midpoint": [23.7, 90.5],
                "status": "IN_TRANSIT",
                "threat_level": "Medium"
            },
            "risk_profile": {
                "level": "Medium",
                "alerts": ["Port Qasim Congestion: 48h delay", "Strait of Malacca: Piracy advisory active"]
            },
            "trade_alerts": [
                "SBP reduces LC margins for telecom imports by 10%.",
                "FBR expected to revise Regulatory Duty (RD) on HS 8517.13 in upcoming budget."
            ],
            "shipment_details": {
                "id": "SHP-2024-883",
                "hs_code": "8517.13",
                "declared_value": "$45,000"
            },
            "financial_metrics": {
                "total_duty_pkr": duties["Total Taxes"],
                "wht_pkr": duties["Withholding Tax (WHT)"],
                "cif_pkr": duties["CIF Value"],
                "landed_cost_pkr": duties["Landed Cost"]
            },
            "detailed_duty": duties
        }

        if intent == 'shipment_tracking':
            mock_response['answer'] = "Shipment Status: Your cargo from Shenzhen is currently IN_TRANSIT. It is passing through the Strait of Malacca. Expect a 2-day delay due to congestion at Port Qasim."
        elif intent == 'duty_calculation':
            mock_response['answer'] = f"Duty Calculation for HS 8517.13: Based on a CIF of {format_pkr(cif_val)}, the estimated landed cost is {format_pkr(mock_response['financial_metrics']['landed_cost_pkr'])}. Customs duty applies at 20%."
        elif intent == 'route_recommendation':
            mock_response['answer'] = "Route Analysis: The direct sea route takes 14 days ($1,200). Routing via Colombo adds 3 days but saves $200. Air freight via Dubai takes 2 days but costs $4,500. Recommended: Direct Sea Route."
        elif intent == 'document_question':
            mock_response['answer'] = "Document Analysis: The uploaded Commercial Invoice shows a declared value of $45,000 for mobile phones. The HS code 8517.13 matches the description."
            
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
        st.session_state.uploaded_docs.append(uploaded_file.name)
        
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
            <div class="intel-item"><span class="intel-key">Origin</span><span class="intel-val">Shenzhen</span></div>
            <div class="intel-item"><span class="intel-key">Destination</span><span class="intel-val">Karachi</span></div>
            <div class="intel-item"><span class="intel-key">HS Code</span><span class="intel-val">8517.13</span></div>
            <div class="intel-item"><span class="intel-key">Declared Value</span><span class="intel-val">$45,000</span></div>
            <div class="intel-item"><span class="intel-key">Consignee</span><span class="intel-val">TechCorp PK</span></div>
            <div class="intel-item"><span class="intel-key">Shipment Type</span><span class="intel-val">Electronics</span></div>
            <div class="intel-item"><span class="intel-key">Customs Status</span><span class="intel-val status-badge-transit">IN_TRANSIT</span></div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# CENTER COLUMN — AI WORKSPACE
# ==========================================
with col_center:
    st.markdown(f"<h3 style='color: {text_primary}; margin-bottom: 24px;'>{st.session_state.nav_selection}</h3>", unsafe_allow_html=True)
    
    if st.session_state.nav_selection == "Dashboard":
        st.dataframe(
            mock_shipments.style.map(
                lambda v: f"color: {accent_color};" if v == "IN_TRANSIT" else (f"color: {danger_color};" if v in ["CUSTOMS_HOLD", "PORT_CONGESTION"] else f"color: {success_color};"),
                subset=["Status"]
            ),
            use_container_width=True,
            hide_index=True
        )
        
    elif st.session_state.nav_selection == "Route Comparison":
        st.markdown("##### Route Alternatives: Shenzhen to Karachi")
        routes = pd.DataFrame([
            {"Route": "Direct Sea", "ETA": "14 Days", "Cost": "$1,200", "Congestion": "Low", "Recommendation": "Optimal"},
            {"Route": "Sea via Colombo", "ETA": "17 Days", "Cost": "$1,000", "Congestion": "High", "Recommendation": "Risk of Delay"},
            {"Route": "Air via Dubai", "ETA": "2 Days", "Cost": "$4,500", "Congestion": "None", "Recommendation": "Fastest"},
        ])
        st.dataframe(routes, use_container_width=True, hide_index=True)
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
            calculated_duties = calculate_duties(cif_input, hs_code_input, is_filer)
            
            # Update session state metrics
            st.session_state.current_metrics = {
                "total_duty_pkr": calculated_duties["Total Taxes"],
                "wht_pkr": calculated_duties["Withholding Tax (WHT)"],
                "cif_pkr": calculated_duties["CIF Value"],
                "landed_cost_pkr": calculated_duties["Landed Cost"]
            }
            st.session_state.detailed_duty = calculated_duties
            st.success("Duties recalculated successfully. See Financial Intelligence panel for details.")
            
        st.markdown("##### Duty Breakdown")
        duty_df = pd.DataFrame(list(st.session_state.detailed_duty.items()), columns=["Tax Component", "Amount (PKR)"])
        duty_df["Amount (PKR)"] = duty_df["Amount (PKR)"].apply(lambda x: format_pkr(x))
        st.dataframe(duty_df, hide_index=True, use_container_width=True)

    else:
        # AI Chat Workspace
        chat_container = st.container(height=600)
        
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if "citations" in msg and msg["citations"]:
                        st.caption(f"Citations: {', '.join(msg['citations'])}")
        
        if prompt := st.chat_input("Ask about duties, tracking, or documents..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)
                    
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing intelligence..."):
                        response_data = send_query(prompt, context={"docs": st.session_state.uploaded_docs})
                        st.write(response_data["answer"])
                        if response_data.get("citations"):
                            st.caption(f"Citations: {', '.join(response_data['citations'])}")
                            
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response_data["answer"],
                "citations": response_data.get("citations", [])
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
