import streamlit as st

def apply_custom_styling():
    """Apply Zumiez brand styling to the Streamlit dashboard"""
    
    st.markdown("""
    <style>
    /* Zumiez Brand Colors */
    :root {
        --zumiez-orange: #FF6B35;
        --zumiez-dark: #262730;
        --zumiez-light: #F5F5F5;
        --zumiez-white: #FFFFFF;
        --success-green: #4CAF50;
        --warning-orange: #FF9800;
        --danger-red: #F44336;
        --info-blue: #2196F3;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: var(--zumiez-dark) !important;
        font-weight: 600;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: var(--zumiez-white);
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: 100%;
        text-align: center;
        color: var(--zumiez-dark) !important;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--zumiez-light);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--zumiez-orange);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #e55a2b;
        box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        transform: translateY(-2px);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-color: var(--zumiez-orange);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        border-color: var(--zumiez-orange);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 24px;
        background-color: var(--zumiez-light);
        border-radius: 6px;
        color: var(--zumiez-dark);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--zumiez-orange);
        color: white;
    }
    
    /* DataFrame styling */
    .dataframe {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Status badges */
    .status-on-track {
        background-color: var(--success-green);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-at-risk {
        background-color: var(--warning-orange);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-behind {
        background-color: var(--danger-red);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-complete {
        background-color: var(--info-blue);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Card styling for KPIs */
    .kpi-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--zumiez-orange);
        margin-bottom: 1rem;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--zumiez-dark);
        margin-bottom: 0.25rem;
    }
    
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #888;
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background-color: #e8f5e8;
        border-left-color: var(--success-green);
        color: #2e7d32;
    }
    
    .alert-warning {
        background-color: #fff3e0;
        border-left-color: var(--warning-orange);
        color: #e65100;
    }
    
    .alert-danger {
        background-color: #ffebee;
        border-left-color: var(--danger-red);
        color: #c62828;
    }
    
    .alert-info {
        background-color: #e3f2fd;
        border-left-color: var(--info-blue);
        color: #1565c0;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: var(--zumiez-orange);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--zumiez-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--zumiez-orange);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #e55a2b;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .kpi-value {
            font-size: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_status_badge(status):
    """Create a styled status badge"""
    status_classes = {
        'On Track': 'status-on-track',
        'At Risk': 'status-at-risk',
        'Behind': 'status-behind',
        'Complete': 'status-complete'
    }
    
    css_class = status_classes.get(status, 'status-on-track')
    
    return f'<span class="{css_class}">{status}</span>'

def create_kpi_card(title, value, subtitle=None, trend=None):
    """Create a styled KPI card"""
    trend_icon = ""
    if trend:
        if trend == 'up':
            trend_icon = "📈"
        elif trend == 'down':
            trend_icon = "📉"
        else:
            trend_icon = "➡️"
    
    subtitle_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ''
    
    return f"""
    <div class="kpi-card fade-in">
        <div class="kpi-title">{title} {trend_icon}</div>
        <div class="kpi-value">{value}</div>
        {subtitle_html}
    </div>
    """

def create_alert(message, alert_type='info'):
    """Create a styled alert box"""
    return f'<div class="alert alert-{alert_type}">{message}</div>'

def format_currency(amount):
    """Format currency with proper styling"""
    if amount >= 1000000:
        return f"${amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"${amount/1000:.0f}K"
    else:
        return f"${amount:,.0f}"

def format_percentage(value, decimal_places=1):
    """Format percentage with proper styling"""
    return f"{value:.{decimal_places}f}%"
