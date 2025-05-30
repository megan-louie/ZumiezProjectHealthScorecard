import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    
    /* Button styling */
    .stButton > button {
        background-color: var(--zumiez-orange);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Tab styling */
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
            start_date = datetime.now() - timedelta(days=random.randint(30, 180))
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
            'primary': '#FF6B35',
            'secondary': '#262730',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'info': '#2196F3'
        }
    
    def create_status_distribution_chart(self, df):
        """Create project status distribution pie chart"""
        status_counts = df['status'].value_counts()
        
        colors = {
            'On Track': self.colors['success'],
            'At Risk': self.colors['warning'],
            'Behind': self.colors['danger'],
            'Complete': self.colors['info']
        }
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title='Project Status Distribution',
            color_discrete_map=colors
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    def create_department_progress_chart(self, df):
        """Create department progress bar chart"""
        dept_progress = df.groupby('department')['progress'].mean().sort_values(ascending=True)
        
        fig = px.bar(
            x=dept_progress.values,
            y=dept_progress.index,
            orientation='h',
            title='Average Progress by Department',
            color_discrete_sequence=[self.colors['primary']]
        )
        
        fig.update_layout(height=400, xaxis_title='Progress (%)', yaxis_title='Department')
        st.plotly_chart(fig, use_container_width=True)
    
    def create_budget_variance_chart(self, df):
        """Create budget variance chart"""
        dept_budgets = df.groupby('department').agg({
            'budget': 'sum',
            'spent': 'sum'
        }).reset_index()
        
        fig = px.bar(
            dept_budgets,
            x='department',
            y=['budget', 'spent'],
            title='Budget vs Actual Spending by Department',
            barmode='group',
            color_discrete_sequence=[self.colors['info'], self.colors['primary']]
        )
        
        fig.update_layout(height=400, yaxis_title='Amount ($)')
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
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

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
        st.metric("Avg Progress", f"{avg_progress:.1f}%", f"{risk_projects} High Risk")
    
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
    show_columns = st.multiselect(
        "Select Columns to Display",
        options=['project_name', 'status', 'department', 'manager', 'budget', 'spent', 'progress', 'risk_score'],
        default=['project_name', 'status', 'department', 'progress', 'budget', 'risk_score']
    )
    
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
    main()
