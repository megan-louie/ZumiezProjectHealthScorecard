import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import random

# Page configuration
st.set_page_config(
    page_title="Zumiez Project Health Scorecard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Data Generator Class
class DataGenerator:
    """Generate realistic demonstration data for Zumiez project dashboard"""
    
    def __init__(self):
        """Initialize data generator with realistic Zumiez project scenarios"""
        self.project_categories = {
            'Retail Technology': [
                'Zumiez Mobile App 2.0 Launch',
                'POS System Rollout - Q1 Stores',
                'Inventory Management System Enhancement',
                'E-commerce Platform Mobile Optimization',
                'Customer Data Platform Integration',
                'Digital Receipt System Implementation',
                'Store WiFi Infrastructure Upgrade',
                'Loyalty Program App Development'
            ],
            'Store Operations': [
                'Seattle Flagship Store Renovation',
                'Snowboard Season Merchandising Rollout',
                'New Store Opening: Portland Downtown',
                'Visual Merchandising Standards Update',
                'Store Security System Upgrade',
                'Energy Efficiency Retrofit Program',
                'Store Layout Optimization Project',
                'Holiday Season Store Prep Initiative'
            ],
            'Brand & Marketing': [
                'Summer Campaign: Skateboard Collection',
                'Influencer Partnership Program Launch',
                'Social Media Content Strategy Overhaul',
                'Brand Ambassador Training Program',
                'Digital Marketing Analytics Platform',
                'Customer Experience Research Project',
                'Sustainability Marketing Campaign',
                'Youth Culture Trend Analysis Initiative'
            ],
            'Supply Chain': [
                'West Coast Distribution Center Expansion',
                'Vendor Portal Integration Project',
                'Supply Chain Visibility Platform',
                'Sustainable Packaging Initiative',
                'International Shipping Optimization',
                'Inventory Forecasting System Upgrade',
                'Vendor Performance Management System',
                'Logistics Cost Optimization Program'
            ]
        }
        
        self.project_managers = [
            'Sarah Johnson', 'Mike Chen', 'Emily Rodriguez', 'David Kim',
            'Jessica Williams', 'Alex Thompson', 'Maria Garcia', 'Ryan O\'Connor',
            'Amanda Foster', 'Chris Martinez', 'Nicole Davis', 'Brandon Lee'
        ]
        
        self.statuses = ['On Track', 'At Risk', 'Behind', 'Complete']
        
    def generate_projects_data(self, num_projects=25):
        """Generate realistic project data for demonstration purposes"""
        projects = []
        
        for _ in range(num_projects):
            # Select random category and project
            category = random.choice(list(self.project_categories.keys()))
            project_name = random.choice(self.project_categories[category])
            
            # Generate project details
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>{total_team_size} team members across {active_projects} projects</small>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_quality_score_card(self, kpi, projects_df):
        """Create quality score KPI card"""
        quality_score = kpi['value']
        
        # Determine color
        if quality_score >= 95:
            color = self.colors['success']
            status = "Excellent"
        elif quality_score >= 90:
            color = self.colors['info']
            status = "Good"
        elif quality_score >= 85:
            color = self.colors['warning']
            status = "Acceptable"
        else:
            color = self.colors['danger']
            status = "Needs Improvement"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = quality_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Quality Score", 'font': {'size': 14}},
            number = {'suffix': "%", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 85], 'color': "lightgray"},
                    {'range': [85, 100], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>Based on deliverable quality metrics</small>
        </div>
        """, unsafe_allow_html=True)

# Main Application
@st.cache_data
def load_data():
    """Load and cache project data"""
    generator = DataGenerator()
    return generator.generate_all_data()

def main():
    """Main dashboard application"""
    
    # Apply custom styling
    apply_custom_styling()
    
    # Header Section
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #FF6B35; margin: 0;'>🏂 ZUMIEZ</h1>
            <h2 style='color: #262730; margin: 10px 0;'>Project Health Scorecard</h2>
            <p style='color: #666; margin: 0;'>Executive Dashboard - {}</p>
        </div>
        """.format(datetime.now().strftime("%B %d, %Y at %I:%M %p")), unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    projects_df = data['projects']
    kpi_data = data['kpis']
    
    # Sidebar filters
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Department filter
    departments = ['All'] + list(projects_df['department'].unique())
    selected_dept = st.sidebar.selectbox("Department", departments)
    
    # Status filter
    statuses = st.sidebar.multiselect(
        "Project Status",
        options=projects_df['status'].unique(),
        default=projects_df['status'].unique()
    )
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Project Date Range",
        value=(datetime.now() - timedelta(days=90), datetime.now() + timedelta(days=180)),
        format="YYYY-MM-DD"
    )
    
    # Search functionality
    search_term = st.sidebar.text_input("🔍 Search Projects", "")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Filter data based on selections
    filtered_df = projects_df.copy()
    
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['department'] == selected_dept]
    
    if statuses:
        filtered_df = filtered_df[filtered_df['status'].isin(statuses)]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['project_name'].str.contains(search_term, case=False, na=False)
        ]
    
    # Executive Summary
    st.markdown("### 📊 Executive Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        total_projects = len(filtered_df)
        on_track = len(filtered_df[filtered_df['status'] == 'On Track'])
        st.metric("Active Projects", total_projects, f"{on_track} On Track")
    
    with summary_col2:
        total_budget = filtered_df['budget'].sum()
        spent_budget = filtered_df['spent'].sum()
        utilization = (spent_budget / total_budget * 100) if total_budget > 0 else 0
        st.metric("Budget Utilization", f"{utilization:.1f}%", f"${spent_budget:,.0f} of ${total_budget:,.0f}")
    
    with summary_col3:
        avg_progress = filtered_df['progress'].mean()
        risk_projects = len(filtered_df[filtered_df['risk_score'] >= 7])
        st.metric("Avg Progress", f"{avg_progress:.1f}%", f"{risk_projects} High Risk", delta_color="inverse")
    
    st.divider()
    
    # KPI Cards Section
    st.markdown("### 🎯 Key Performance Indicators")
    kpi_cards = KPICards()
    kpi_cards.display_kpi_cards(kpi_data, filtered_df)
    
    st.divider()
    
    # Charts Section
    st.markdown("### 📈 Project Analytics")
    chart_components = ChartComponents()
    
    # Create tabs for different chart views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "💰 Budget Analysis", "⚠️ Risk Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            chart_components.create_status_distribution_chart(filtered_df)
        
        with col2:
            chart_components.create_department_progress_chart(filtered_df)
    
    with tab2:
        chart_components.create_budget_variance_chart(filtered_df)
    
    with tab3:
        chart_components.create_risk_gauge(filtered_df)
    
    st.divider()
    
    # Project Details Table
    st.markdown("### 📋 Project Details")
    
    # Display options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        show_columns = st.multiselect(
            "Select Columns to Display",
            options=['project_name', 'status', 'department', 'manager', 'budget', 'spent', 'progress', 'risk_score', 'start_date', 'end_date'],
            default=['project_name', 'status', 'department', 'progress', 'budget', 'risk_score']
        )
    
    with col2:
        sort_column = st.selectbox("Sort by", options=show_columns if show_columns else ['project_name'])
    
    with col3:
        sort_order = st.selectbox("Order", ["Ascending", "Descending"])
    
    # Format and display table
    if show_columns:
        display_df = filtered_df[show_columns].copy()
        
        # Format columns for better display
        if 'budget' in display_df.columns:
            display_df['budget'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
        if 'spent' in display_df.columns:
            display_df['spent'] = display_df['spent'].apply(lambda x: f"${x:,.0f}")
        if 'progress' in display_df.columns:
            display_df['progress'] = display_df['progress'].apply(lambda x: f"{x:.1f}%")
        if 'risk_score' in display_df.columns:
            display_df['risk_score'] = display_df['risk_score'].apply(lambda x: f"{x:.1f}")
        
        # Sort data
        ascending = sort_order == "Ascending"
        if sort_column in filtered_df.columns:
            if sort_column in ['budget', 'spent', 'progress', 'risk_score']:
                display_df = display_df.sort_values(
                    by=sort_column, 
                    key=lambda x: filtered_df[sort_column], 
                    ascending=ascending
                )
            else:
                display_df = display_df.sort_values(by=sort_column, ascending=ascending)
        
        # Style the dataframe
        def highlight_status(val):
            if val == 'At Risk':
                return 'background-color: #ffebee'
            elif val == 'Behind':
                return 'background-color: #ffcdd2'
            elif val == 'On Track':
                return 'background-color: #e8f5e8'
            elif val == 'Complete':
                return 'background-color: #c8e6c9'
            return ''
        
        if 'status' in display_df.columns:
            styled_df = display_df.style.map(highlight_status, subset=['status'])
            st.dataframe(styled_df, use_container_width=True, height=400)
        else:
            st.dataframe(display_df, use_container_width=True, height=400)
    
    # Export functionality
    st.markdown("### 📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download CSV", type="secondary"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Project Data",
                data=csv,
                file_name=f"zumiez_projects_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Summary", type="secondary"):
            summary_data = {
                'Total Projects': len(filtered_df),
                'On Track': len(filtered_df[filtered_df['status'] == 'On Track']),
                'At Risk': len(filtered_df[filtered_df['status'] == 'At Risk']),
                'Behind': len(filtered_df[filtered_df['status'] == 'Behind']),
                'Complete': len(filtered_df[filtered_df['status'] == 'Complete']),
                'Total Budget': f"${filtered_df['budget'].sum():,.0f}",
                'Total Spent': f"${filtered_df['spent'].sum():,.0f}",
                'Average Progress': f"{filtered_df['progress'].mean():.1f}%",
                'Average Risk Score': f"{filtered_df['risk_score'].mean():.1f}"
            }
            summary_df = pd.DataFrame(list(summary_data.items()), columns=['Metric', 'Value'])
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="Download Summary",
                data=csv,
                file_name=f"zumiez_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666; padding: 20px;'>"
        f"Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | "
        f"Data Source: Zumiez Project Management System | "
        f"Showing {len(filtered_df)} of {len(projects_df)} projects"
        f"</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()art_date = datetime.now() - timedelta(days=random.randint(30, 180))
            duration_days = random.randint(60, 365)
            end_date = start_date + timedelta(days=duration_days)
            
            # Budget based on project category
            budget_ranges = {
                'Retail Technology': (50000, 2000000),
                'Store Operations': (25000, 800000),
                'Brand & Marketing': (15000, 500000),
                'Supply Chain': (100000, 1500000)
            }
            
            min_budget, max_budget = budget_ranges[category]
            budget = random.randint(min_budget, max_budget)
            
            # Progress and spending
            progress = random.uniform(15, 95)
            spent_ratio = min(progress / 100 + random.uniform(-0.1, 0.2), 1.0)
            spent = budget * spent_ratio
            
            # Risk score based on various factors
            risk_score = self._calculate_risk_score(progress, spent_ratio, start_date, end_date)
            
            # Status based on risk and progress
            status = self._determine_status(progress, risk_score)
            
            project = {
                'project_name': project_name,
                'department': category,
                'manager': random.choice(self.project_managers),
                'status': status,
                'budget': budget,
                'spent': spent,
                'progress': progress,
                'risk_score': risk_score,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'team_size': random.randint(3, 15),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'completion_date': end_date.strftime('%Y-%m-%d') if status == 'Complete' else None
            }
            
            projects.append(project)
        
        return pd.DataFrame(projects)
    
    def _calculate_risk_score(self, progress, spent_ratio, start_date, end_date):
        """Calculate risk score based on multiple factors"""
        # Base risk
        risk = 3.0
        
        # Budget overrun risk
        if spent_ratio > 0.8:
            risk += 2.0
        elif spent_ratio > 0.6:
            risk += 1.0
        
        # Timeline risk
        total_days = (end_date - start_date).days
        elapsed_days = (datetime.now() - start_date).days
        time_progress = elapsed_days / total_days if total_days > 0 else 0
        
        if time_progress > progress / 100 + 0.2:
            risk += 2.5
        elif time_progress > progress / 100 + 0.1:
            risk += 1.5
        
        # Progress risk
        if progress < 30 and time_progress > 0.5:
            risk += 2.0
        elif progress < 50 and time_progress > 0.7:
            risk += 1.0
        
        # Add some randomness
        risk += random.uniform(-0.5, 0.5)
        
        return min(max(risk, 1.0), 10.0)
    
    def _determine_status(self, progress, risk_score):
        """Determine project status based on progress and risk"""
        if progress >= 95:
            return 'Complete'
        elif risk_score >= 7:
            return 'Behind'
        elif risk_score >= 5:
            return 'At Risk'
        else:
            return 'On Track'
    
    def generate_kpi_data(self, projects_df):
        """Generate KPI metrics based on project data"""
        total_projects = len(projects_df)
        
        kpis = {
            'budget_health': {
                'value': 100 - (projects_df['spent'].sum() / projects_df['budget'].sum() * 100 - 70),
                'target': 85,
                'trend': random.choice(['up', 'down', 'stable'])
            },
            'timeline_performance': {
                'value': len(projects_df[projects_df['status'].isin(['On Track', 'Complete'])]) / total_projects * 100,
                'target': 80,
                'trend': random.choice(['up', 'down', 'stable'])
            },
            'risk_level': {
                'value': projects_df['risk_score'].mean(),
                'target': 4.0,
                'trend': random.choice(['up', 'down', 'stable'])
            },
            'team_velocity': {
                'value': projects_df['progress'].mean(),
                'target': 75,
                'trend': random.choice(['up', 'down', 'stable'])
            },
            'resource_utilization': {
                'value': random.uniform(75, 95),
                'target': 85,
                'trend': random.choice(['up', 'down', 'stable'])
            },
            'quality_score': {
                'value': random.uniform(85, 98),
                'target': 90,
                'trend': random.choice(['up', 'down', 'stable'])
            }
        }
        
        return kpis
    
    def generate_all_data(self):
        """Generate complete dataset for dashboard"""
        projects_df = self.generate_projects_data()
        kpi_data = self.generate_kpi_data(projects_df)
        
        return {
            'projects': projects_df,
            'kpis': kpi_data
        }

# Chart Components Class
class ChartComponents:
    """Chart components for the Zumiez dashboard"""
    
    def __init__(self):
        """Initialize chart components with Zumiez brand colors"""
        self.colors = {
            'primary': '#FF6B35',    # Zumiez Orange
            'secondary': '#262730',   # Dark Gray
            'success': '#4CAF50',     # Green
            'warning': '#FF9800',     # Orange
            'danger': '#F44336',      # Red
            'info': '#2196F3',        # Blue
            'light': '#F5F5F5',       # Light Gray
            'white': '#FFFFFF'
        }
        
        self.color_sequence = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['success'],
            self.colors['warning'],
            self.colors['info'],
            self.colors['danger']
        ]
    
    def create_status_distribution_chart(self, df):
        """Create project status distribution pie chart"""
        status_counts = df['status'].value_counts()
        
        colors = {
            'On Track': self.colors['success'],
            'At Risk': self.colors['warning'],
            'Behind': self.colors['danger'],
            'Complete': self.colors['info']
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker_colors=[colors.get(status, self.colors['primary']) for status in status_counts.index],
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': 'Project Status Distribution',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            showlegend=True,
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_department_progress_chart(self, df):
        """Create department progress bar chart"""
        dept_progress = df.groupby('department')['progress'].mean().sort_values(ascending=True)
        
        fig = go.Figure(data=[go.Bar(
            y=dept_progress.index,
            x=dept_progress.values,
            orientation='h',
            marker_color=self.colors['primary'],
            text=[f'{val:.1f}%' for val in dept_progress.values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Average Progress: %{x:.1f}%<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': 'Average Progress by Department',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Progress (%)',
            yaxis_title='Department',
            height=400,
            margin=dict(t=50, b=50, l=150, r=50)
        )
        
        fig.update_layout(xaxis=dict(range=[0, 100]))
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_budget_variance_chart(self, df):
        """Create budget variance chart"""
        dept_budgets = df.groupby('department').agg({
            'budget': 'sum',
            'spent': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        # Budget bars
        fig.add_trace(go.Bar(
            name='Budgeted',
            x=dept_budgets['department'],
            y=dept_budgets['budget'],
            marker_color=self.colors['info'],
            opacity=0.7
        ))
        
        # Spent bars
        fig.add_trace(go.Bar(
            name='Spent',
            x=dept_budgets['department'],
            y=dept_budgets['spent'],
            marker_color=self.colors['primary']
        ))
        
        fig.update_layout(
            title={
                'text': 'Budget vs Actual Spending by Department',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            barmode='group',
            xaxis_title='Department',
            yaxis_title='Amount ($)',
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        fig.update_layout(yaxis=dict(tickformat='$,.0f'))
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_risk_gauge(self, df):
        """Create risk level gauge chart"""
        avg_risk = df['risk_score'].mean()
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = avg_risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Average Risk Level"},
            delta = {'reference': 5.0},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, 3], 'color': self.colors['success']},
                    {'range': [3, 6], 'color': self.colors['warning']},
                    {'range': [6, 10], 'color': self.colors['danger']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
            }
        ))
        
        fig.update_layout(height=400, margin=dict(t=50, b=50, l=50, r=50))
        
        st.plotly_chart(fig, use_container_width=True)

# KPI Cards Class
class KPICards:
    """KPI card components for the dashboard"""
    
    def __init__(self):
        """Initialize KPI cards with styling"""
        self.colors = {
            'primary': '#FF6B35',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'info': '#2196F3',
            'secondary': '#262730'
        }
    
    def display_kpi_cards(self, kpi_data, projects_df):
        """Display KPI cards in a grid layout"""
        
        # Create columns for KPI cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._create_budget_health_card(kpi_data['budget_health'], projects_df)
            self._create_risk_level_card(kpi_data['risk_level'], projects_df)
        
        with col2:
            self._create_timeline_performance_card(kpi_data['timeline_performance'], projects_df)
            self._create_resource_utilization_card(kpi_data['resource_utilization'], projects_df)
        
        with col3:
            self._create_team_velocity_card(kpi_data['team_velocity'], projects_df)
            self._create_quality_score_card(kpi_data['quality_score'], projects_df)
    
    def _create_budget_health_card(self, kpi, projects_df):
        """Create budget health KPI card"""
        total_budget = projects_df['budget'].sum()
        total_spent = projects_df['spent'].sum()
        utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
        
        # Determine color based on performance
        if utilization <= 70:
            color = self.colors['success']
            status = "Excellent"
        elif utilization <= 85:
            color = self.colors['info']
            status = "Good"
        elif utilization <= 95:
            color = self.colors['warning']
            status = "Watch"
        else:
            color = self.colors['danger']
            status = "Over Budget"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = utilization,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Budget Health", 'font': {'size': 14}},
            number = {'suffix': "%", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 100], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add status text
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>${total_spent:,.0f} of ${total_budget:,.0f} spent</small>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_timeline_performance_card(self, kpi, projects_df):
        """Create timeline performance KPI card"""
        on_time_projects = len(projects_df[projects_df['status'].isin(['On Track', 'Complete'])])
        total_projects = len(projects_df)
        performance = (on_time_projects / total_projects * 100) if total_projects > 0 else 0
        
        # Determine color
        if performance >= 80:
            color = self.colors['success']
            status = "Excellent"
        elif performance >= 70:
            color = self.colors['info']
            status = "Good"
        elif performance >= 60:
            color = self.colors['warning']
            status = "Needs Attention"
        else:
            color = self.colors['danger']
            status = "Critical"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = performance,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Timeline Performance", 'font': {'size': 14}},
            number = {'suffix': "%", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 100], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>{on_time_projects} of {total_projects} projects on track</small>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_risk_level_card(self, kpi, projects_df):
        """Create risk level KPI card"""
        avg_risk = projects_df['risk_score'].mean()
        high_risk_count = len(projects_df[projects_df['risk_score'] >= 7])
        
        # Determine color (inverted for risk)
        if avg_risk <= 3:
            color = self.colors['success']
            status = "Low Risk"
        elif avg_risk <= 5:
            color = self.colors['info']
            status = "Moderate Risk"
        elif avg_risk <= 7:
            color = self.colors['warning']
            status = "High Risk"
        else:
            color = self.colors['danger']
            status = "Critical Risk"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Risk Level", 'font': {'size': 14}},
            number = {'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 7], 'color': "yellow"},
                    {'range': [7, 10], 'color': "lightcoral"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>{high_risk_count} projects at high risk</small>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_team_velocity_card(self, kpi, projects_df):
        """Create team velocity KPI card"""
        avg_progress = projects_df['progress'].mean()
        completed_projects = len(projects_df[projects_df['status'] == 'Complete'])
        
        # Determine color
        if avg_progress >= 75:
            color = self.colors['success']
            status = "High Velocity"
        elif avg_progress >= 60:
            color = self.colors['info']
            status = "Good Velocity"
        elif avg_progress >= 45:
            color = self.colors['warning']
            status = "Low Velocity"
        else:
            color = self.colors['danger']
            status = "Very Low"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_progress,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Team Velocity", 'font': {'size': 14}},
            number = {'suffix': "%", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 45], 'color': "lightgray"},
                    {'range': [45, 100], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: {color}20; border-radius: 5px; margin-bottom: 20px;'>
            <strong style='color: {color};'>{status}</strong><br>
            <small>{completed_projects} projects completed</small>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_resource_utilization_card(self, kpi, projects_df):
        """Create resource utilization KPI card"""
        total_team_size = projects_df['team_size'].sum()
        active_projects = len(projects_df[projects_df['status'] != 'Complete'])
        utilization = kpi['value']
        
        # Determine color
        if 80 <= utilization <= 90:
            color = self.colors['success']
            status = "Optimal"
        elif 70 <= utilization < 80 or 90 < utilization <= 95:
            color = self.colors['info']
            status = "Good"
        elif utilization < 70:
            color = self.colors['warning']
            status = "Under-utilized"
        else:
            color = self.colors['danger']
            status = "Over-utilized"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = utilization,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Resource Utilization", 'font': {'size': 14}},
            number = {'suffix': "%", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 70], 'color': "lightgray"},
                    {'range': [70, 100], 'color': "gray"}
                ]
            }
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(t=30, b=0, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st
