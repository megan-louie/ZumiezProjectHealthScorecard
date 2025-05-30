import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Import custom modules
from data_generator import DataGenerator
from components.charts import ChartComponents
from components.kpi_cards import KPICards
from utils.styling import apply_custom_styling

# Page configuration
st.set_page_config(
    page_title="Zumiez Project Health Scorecard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Initialize components
@st.cache_data
def load_data():
    """Load and cache project data"""
    generator = DataGenerator()
    return generator.generate_all_data()

def main():
    """Main dashboard application"""
    
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
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💰 Budget Analysis", "⚠️ Risk Matrix", "📅 Timeline"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            chart_components.create_status_distribution_chart(filtered_df)
        
        with col2:
            chart_components.create_department_progress_chart(filtered_df)
        
        chart_components.create_project_timeline_chart(filtered_df)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            chart_components.create_budget_variance_chart(filtered_df)
        
        with col2:
            chart_components.create_resource_utilization_chart(filtered_df)
        
        chart_components.create_budget_waterfall_chart(filtered_df)
    
    with tab3:
        chart_components.create_risk_impact_matrix(filtered_df)
        
        col1, col2 = st.columns(2)
        with col1:
            chart_components.create_risk_gauge(filtered_df)
        with col2:
            chart_components.create_team_heatmap(filtered_df)
    
    with tab4:
        chart_components.create_gantt_chart(filtered_df)
        chart_components.create_milestone_progress(filtered_df)
    
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
    
    col1, col2, col3 = st.columns(3)
    
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
    main()
