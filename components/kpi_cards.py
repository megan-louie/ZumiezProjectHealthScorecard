import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
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
        # Calculate team utilization
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
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
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
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
