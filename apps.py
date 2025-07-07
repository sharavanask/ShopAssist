import streamlit as st
import asyncio
from server.shop import getproduct
import json

# Page configuration
st.set_page_config(
    page_title="Shop Assist - Smart Product Discovery",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
* {
    caret-color: #fff !important;
}
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            
#MainMenu, 
footer, 
.stDeployButton, 
.stDecoration, 
.stToolbar, 
.stStatusWidget, 
.stToast,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"],
header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0 !important;
    position: fixed !important;
    top: -100px !important;
    display: none !important;
}

/* Target the main toolbar container */
.main > div:first-child {
    display: none !important;
}

/* Hide the top toolbar section */
section[data-testid="stSidebar"] + div > div:first-child {
    display: none !important;
}

/* Force hide deploy button and related elements */
button[kind="header"], 
button[data-testid="stDeployButton"],
[data-testid="stToolbar"] button,
.stApp > div:first-child > div:first-child {
    display: none !important;
    visibility: hidden !important;
}

/* Alternative approach - make them dark if they still appear */
.stDeployButton, 
.stToolbar, 
.stStatusWidget,
[data-testid="stToolbar"],
[data-testid="stDeployButton"],
[data-testid="stStatusWidget"] {
    background: var(--dark-bg) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

/* Target any remaining white elements */
.stDeployButton *,
.stToolbar *,
.stStatusWidget *,
[data-testid="stToolbar"] *,
[data-testid="stDeployButton"] *,
[data-testid="stStatusWidget"] * {
    color: var(--text-primary) !important;
    background: transparent !important;
    border-color: var(--border-color) !important;
}


button[kind="primary"],
button[kind="secondary"],
button[kind="header"] {
  background: var(--primary-color) !important;
  color: white !important;
  border: none !important;
  cursor: pointer !important;
  transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease !important;
  outline: none; /* Optional: remove default outline */
}

/* Hover animation - turns green with lift effect */
button[kind="primary"]:hover,
button[kind="secondary"]:hover,
button[kind="header"]:hover {
  background: #28a745 !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 6px 12px rgba(40, 167, 69, 0.3) !important;
}

/* Focus (optional for keyboard nav) */
button[kind="primary"]:focus,
button[kind="secondary"]:focus,
button[kind="header"]:focus {
  outline: 2px solid #28a745 !important; /* Accessible focus ring */
  outline-offset: 2px !important;
}

/* Click animation - darker green with scale effect */
button[kind="primary"]:active,
button[kind="secondary"]:active,
button[kind="header"]:active {
  background: #1e7e34 !important;
  transform: translateY(0) scale(0.97) !important;
  box-shadow: 0 3px 6px rgba(30, 126, 52, 0.4) !important;
}
/* Hide the entire header section */
.stApp > header,
.stApp > div:first-child > div:first-child > div:first-child {
    display: none !important;
}

/* Remove any remaining white backgrounds */
* {
    background-color: transparent !important;
}

/* Ensure app background is maintained */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
}

/* Target the specific toolbar container */
.stApp > div:first-child > div:first-child {
    background: var(--dark-bg) !important;
    color: var(--text-primary) !important;
}

/* Hide any remaining Streamlit chrome */
[data-testid="stAppViewContainer"] > div:first-child {
    display: none !important;
}
/* Root variables */
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #06b6d4;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --dark-bg: #0f172a;
    --card-bg: #1e293b;
    --surface-bg: #334155;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --border-color: #475569;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}

/* Global styles */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    padding-top: 0 !important;
    margin-top: 0 !important;
}
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Force all text to be white */
.stApp, .stApp * {
    color: #fff !important;
}

/* Header styling */
.main-header {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    width: 100vw;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    overflow: hidden;
    padding: 1rem 1rem;
    margin-top: 0 !important;
    margin-bottom: 2rem;
    z-index: 1000;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
}

.main-header h1 {
    font-size: 3rem;
    font-weight: 800;
    color: white !important;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.main-header p {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.9) !important;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* Form styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}

.stTextInput > label,
.stNumberInput > label,
.stTextArea > label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow-md) !important;
    width: 100% !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
    background: linear-gradient(135deg, #5855eb 0%, #7c3aed 100%) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Results container styling */
.results-container {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: var(--shadow-xl);
    border: 1px solid var(--border-color);
    color: #fff !important;
}

.results-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.results-header h3 {
    color: #fff !important;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
}

.results-body {
    color: #fff !important;
}

.search-summary {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    color: var(--text-primary) !important;
}

.search-summary h4 {
    color: var(--primary-color) !important;
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    font-weight: 600;
}

.search-param {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0.5rem 0;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.search-param:last-child {
    border-bottom: none;
}

.search-param-label {
    color: var(--text-secondary) !important;
    font-weight: 500;
}

.search-param-value {
    color: var(--text-primary) !important;
    font-weight: 600;
}

/* Code block styling */
.stCode {
    background: var(--dark-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    color: #fff !important;
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace !important;
}

.stCode > div {
    color: #fff !important;
}

.stCode pre {
    color: #fff !important;
}

.stCode code {
    color: #fff !important;
}

/* Status messages */
.status-message {
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #fff !important;
}

.status-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    color: var(--success-color) !important;
}

.status-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: var(--error-color) !important;
}

.status-warning {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: var(--warning-color) !important;
}

/* Spinner */
.spinner {
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 0.5rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 3rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        padding: 2rem 1rem;
    }
    
    .main-header h1 {
        font-size: 2rem;
    }
    
    .main-card {
        padding: 1.5rem;
    }
    
    .results-body {
        padding: 1.5rem;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--surface-bg);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}

/* Form columns */
.form-row {
    display: flex;
    gap: 1rem;
}

.form-row > div {
    flex: 1;
}

@media (max-width: 640px) {
    .form-row {
        flex-direction: column;
        gap: 0;
    }
}

/* Make form section headings white */
.stForm h2, .stForm h3, .stForm h4,
h2, h3, h4, h1, h5, h6 {
    color: #fff !important;
    font-weight: 700 !important;
}

/* All paragraph text white */
p, div, span, li, ul, ol {
    color: #fff !important;
}

/* Streamlit markdown text */
.stMarkdown, .stMarkdown div, .stMarkdown p, .stMarkdown span {
    color: #fff !important;
}

/* Dark mode for Streamlit deploy/run dialogs and overlays */
[data-testid="stDeployButton"], /* Deploy button */
[data-testid="stDeployDialog"], /* Deploy dialog */
[data-testid="stModal"],        /* General modal */
.stModal, .stDialog, .stAlert, .stToast, .stStatusWidget, .stToolbar {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5) !important;
}
[data-testid="stDeployButton"] * {
    color: #f8fafc !important;
}
.stModal h1, .stModal h2, .stModal h3, .stModal h4,
.stDialog h1, .stDialog h2, .stDialog h3, .stDialog h4 {
    color: #f8fafc !important;
}
.stModal button, .stDialog button, .stAlert button {
    background: #334155 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
    border: 1px solid #475569 !important;
}

/* Force dark mode for deploy/run overlays and dialogs */
[data-testid="stDeployButton"], .stDeployButton, .stDeployDialog, .stModal, .stDialog, .stAlert, .stToast, .stStatusWidget, .stToolbar {
    background: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5) !important;
}
[data-testid="stDeployButton"] *, .stDeployButton *, .stDeployDialog *, .stModal *, .stDialog *, .stAlert *, .stToast *, .stStatusWidget *, .stToolbar * {
    color: #f8fafc !important;
    background: transparent !important;
}
.stModal h1, .stModal h2, .stModal h3, .stModal h4,
.stDialog h1, .stDialog h2, .stDialog h3, .stDialog h4 {
    color: #f8fafc !important;
}
.stModal button, .stDialog button, .stAlert button {
    background: #334155 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
    border: 1px solid #475569 !important;
}

/* Force white text in min and max price number input boxes */
.stNumberInput input[type="number"] {
    color: #fff !important;
    background: var(--surface-bg) !important;
    border: 1px solid var(--border-color) !important;
}
.stNumberInput input[type="number"]::placeholder {
    color: #cbd5e1 !important;
    opacity: 1 !important;
}

/* Force white text in all Streamlit elements */
.stSelectbox, .stSelectbox *, 
.stMultiSelect, .stMultiSelect *,
.stCheckbox, .stCheckbox *,
.stRadio, .stRadio *,
.stSlider, .stSlider *,
.stDateInput, .stDateInput *,
.stTimeInput, .stTimeInput *,
.stFileUploader, .stFileUploader *,
.stColorPicker, .stColorPicker *,
.stDataFrame, .stDataFrame *,
.stTable, .stTable *,
.stMetric, .stMetric *,
.stProgress, .stProgress *,
.stSpinner, .stSpinner *,
.stBalloons, .stBalloons *,
.stSnow, .stSnow *,
.stSuccess, .stSuccess *,
.stInfo, .stInfo *,
.stWarning, .stWarning *,
.stError, .stError *,
.stException, .stException * {
    color: #fff !important;
}

/* Specific targeting for results section */
.results-container *,
.results-header *,
.results-body *,
.search-summary *,
.search-param *,
.status-message * {
    color: #fff !important;
}

/* Override any remaining dark text */
* {
    color: #fff !important;
}

/* But keep code syntax highlighting readable */
.stCode {
    color: #fff !important;
}

.stCode .hljs-string { color: #98d982 !important; }
.stCode .hljs-number { color: #d19a66 !important; }
.stCode .hljs-literal { color: #56b6c2 !important; }
.stCode .hljs-keyword { color: #c678dd !important; }
.stCode .hljs-attr { color: #e06c75 !important; }

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🛍️ Shop Assist</h1>
    <p>Smart Product Discovery & Personalized Recommendations</p>
</div>
""", unsafe_allow_html=True)

# Search form
with st.form("professional_shop_form", clear_on_submit=False):
    # Product name input
    st.markdown("### 🔍 Product Search")
    prod = st.text_input(
        "Product Name",
        placeholder="Enter product name (e.g., Wireless Earbuds, Gaming Laptop, iPhone...)",
        help="Describe the product you're looking for"
    )
    
    # Price range inputs
    st.markdown("### 💰 Price Range")
    col1, col2 = st.columns(2)
    with col1:
        minp = st.number_input(
            "Minimum Price ($)",
            min_value=1.0,
            value=1.0,
            step=1.0,
            help="Set your minimum budget"
        )
    with col2:
        maxp = st.number_input(
            "Maximum Price ($)",
            min_value=1.0,
            value=9999999.0,
            step=1.0,
            help="Set your maximum budget"
        )
    
    # Specific features
    st.markdown("## ✨ Your Requirements")
    specific_features = st.text_area(
        "Features & Requirements (Optional)",
        placeholder="Describe specific features you need (e.g., waterproof, wireless charging, 5G support, gaming performance, etc.)",
        help="Add any specific requirements or features you're looking for",
        height=150
    )
    
    # Search button
    submitted = st.form_submit_button("🚀 Search Products")

st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for results
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_params' not in st.session_state:
    st.session_state.search_params = None

# Handle form submission
if submitted:
    if not prod.strip():
        st.markdown("""
        <div class="status-message status-error">
            <i class="fas fa-exclamation-triangle"></i>
            Please enter a product name to search.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Store search parameters
        st.session_state.search_params = {
            'product': prod.strip(),
            'min_price': minp,
            'max_price': maxp,
            'features': specific_features.strip()
        }
        
        # Results container
        st.markdown("""
        <div class="results-header">
            <h3>📦 Search Results</h3>
        </div>
        <div class="results-body">
        """, unsafe_allow_html=True)
        
        # Search summary
        features_text = f"Features: {specific_features}" if specific_features.strip() else "Features: Not specified"
        st.markdown(f"""
        <div class="search-summary">
            <h4>🔍 Search Parameters</h4>
            <div class="search-param">
                <span class="search-param-label">Product:</span>
                <span class="search-param-value">{prod}</span>
            </div>
            <div class="search-param">
                <span class="search-param-label">Price Range:</span>
                <span class="search-param-value">${minp:,.0f} - ${maxp:,.0f}</span>
            </div>
            <div class="search-param">
                <span class="search-param-label">Features:</span>
                <span class="search-param-value">{specific_features if specific_features.strip() else 'Not specified'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Search execution
        try:
            with st.spinner("🔍 Searching for products across multiple platforms..."):
                # Call the product search function
                result = asyncio.run(getproduct(prod, specific_features, minp, maxp))
                
                if result:
                    st.session_state.search_results = result
                    st.markdown("""
                    <div class="status-message status-success">
                        <i class="fas fa-check-circle"></i>
                        Search completed successfully! Found matching products.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display results
                    st.markdown("### 📊 Results")
                    
                    # Try to format JSON if possible
                    try:
                        if isinstance(result, str):
                            formatted_result = json.dumps(json.loads(result), indent=2)
                        else:
                            formatted_result = json.dumps(result, indent=2)
                        st.code(formatted_result, language="json")
                    except:
                        st.code(str(result), language="text")
                        
                else:
                    st.markdown("""
                    <div class="status-message status-warning">
                        <i class="fas fa-exclamation-circle"></i>
                        No products found matching your criteria. Try adjusting your search parameters.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Suggestions
                    st.markdown("""
                    **💡 Suggestions:**
                    - Try using more general keywords
                    - Expand your price range
                    - Remove or modify specific feature requirements
                    - Check your spelling
                    """)
                    
        except Exception as e:
            st.markdown(f"""
            <div class="status-message status-error">
                <i class="fas fa-times-circle"></i>
                An error occurred while searching: {str(e)}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **🔧 Troubleshooting Tips:**
            - Check your internet connection
            - Try again in a few moments
            - Contact support if the problem persists
            """)
        
        

# Display previous results if available
elif st.session_state.search_results and st.session_state.search_params:
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("""
    <div class="results-header">
        <h3>📦 Previous Search Results</h3>
    </div>
    <div class="results-body">
    """, unsafe_allow_html=True)
    
    params = st.session_state.search_params
    st.markdown(f"""
    <div class="search-summary">
        <h4>🔍 Search Parameters</h4>
        <div class="search-param">
            <span class="search-param-label">Product:</span>
            <span class="search-param-value">{params['product']}</span>
        </div>
        <div class="search-param">
            <span class="search-param-label">Price Range:</span>
            <span class="search-param-value">${params['min_price']:,.0f} - ${params['max_price']:,.0f}</span>
        </div>
        <div class="search-param">
            <span class="search-param-label">Features:</span>
            <span class="search-param-value">{params['features'] if params['features'] else 'Not specified'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Results")
    try:
        if isinstance(st.session_state.search_results, str):
            formatted_result = json.dumps(json.loads(st.session_state.search_results), indent=2)
        else:
            formatted_result = json.dumps(st.session_state.search_results, indent=2)
        st.code(formatted_result, language="json")
    except:
        st.code(str(st.session_state.search_results), language="text")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
