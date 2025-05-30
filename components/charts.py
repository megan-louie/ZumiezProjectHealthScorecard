import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
    
    def create_project_timeline_chart(self, df):
        """Create project timeline overview chart"""
        # Prepare data for timeline
        timeline_df = df.copy()
        timeline_df['start_date'] = pd.to_datetime(timeline_df['start_date'])
        timeline_df['end_date'] = pd.to_datetime(timeline_df['end_date'])
        timeline_df['duration'] = (timeline_df['end_date'] - timeline_df['start_date']).dt.days
        
        # Sort by start date
        timeline_df = timeline_df.sort_values('start_date')
        
        # Take top 10 projects for visibility
        timeline_df = timeline_df.head(10)
        
        fig = go.Figure()
        
        status_colors = {
            'On Track': self.colors['success'],
            'At Risk': self.colors['warning'],
            'Behind': self.colors['danger'],
            'Complete': self.colors['info']
        }
        
        for _, project in timeline_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[project['start_date'], project['end_date']],
                y=[project['project_name'], project['project_name']],
                mode='lines+markers',
                line=dict(width=8, color=status_colors.get(project['status'], self.colors['primary'])),
                marker=dict(size=8),
                name=project['status'],
                showlegend=False,
                hovertemplate=f'<b>{project["project_name"]}</b><br>' +
                            f'Status: {project["status"]}<br>' +
                            f'Progress: {project["progress"]:.1f}%<br>' +
                            f'Duration: {project["duration"]} days<extra></extra>'
            ))
        
        fig.update_layout(
            title={
                'text': 'Project Timeline Overview (Top 10)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Timeline',
            yaxis_title='Projects',
            height=500,
            margin=dict(t=50, b=50, l=300, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_budget_variance_chart(self, df):
        """Create budget variance waterfall chart"""
        # Calculate variances
        total_budget = df['budget'].sum()
        total_spent = df['spent'].sum()
        variance = total_budget - total_spent
        
        # Create department-level variances
        dept_variances = df.groupby('department').agg({
            'budget': 'sum',
            'spent': 'sum'
        }).reset_index()
        dept_variances['variance'] = dept_variances['budget'] - dept_variances['spent']
        
        fig = go.Figure()
        
        # Budget bars
        fig.add_trace(go.Bar(
            name='Budgeted',
            x=dept_variances['department'],
            y=dept_variances['budget'],
            marker_color=self.colors['info'],
            opacity=0.7
        ))
        
        # Spent bars
        fig.add_trace(go.Bar(
            name='Spent',
            x=dept_variances['department'],
            y=dept_variances['spent'],
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
        
        # Format y-axis as currency
        fig.update_layout(yaxis=dict(tickformat='$,.0f'))
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_resource_utilization_chart(self, df):
        """Create resource utilization chart"""
        # Calculate team utilization by department
        dept_resources = df.groupby('department').agg({
            'team_size': 'sum',
            'progress': 'mean'
        }).reset_index()
        
        # Simulate utilization data
        dept_resources['utilization'] = dept_resources['progress'] * np.random.uniform(0.8, 1.2, len(dept_resources))
        dept_resources['utilization'] = np.clip(dept_resources['utilization'], 0, 100)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dept_resources['team_size'],
            y=dept_resources['utilization'],
            mode='markers+text',
            marker=dict(
                size=dept_resources['team_size'] * 3,
                color=dept_resources['progress'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Avg Progress (%)")
            ),
            text=dept_resources['department'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>' +
                        'Team Size: %{x}<br>' +
                        'Utilization: %{y:.1f}%<br>' +
                        '<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': 'Resource Utilization by Department',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Team Size',
            yaxis_title='Utilization (%)',
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_budget_waterfall_chart(self, df):
        """Create budget waterfall chart showing allocation"""
        dept_budgets = df.groupby('department')['budget'].sum().sort_values(ascending=False)
        
        # Create waterfall data
        x_data = ['Total'] + list(dept_budgets.index)
        y_data = [dept_budgets.sum()] + list(-dept_budgets.values)
        
        # Calculate cumulative values
        cumulative = [dept_budgets.sum()]
        for i, val in enumerate(dept_budgets.values):
            cumulative.append(cumulative[-1] - val)
        
        fig = go.Figure()
        
        # Total bar
        fig.add_trace(go.Bar(
            name='Total Budget',
            x=['Total'],
            y=[dept_budgets.sum()],
            marker_color=self.colors['info'],
            text=[f'${dept_budgets.sum():,.0f}'],
            textposition='auto'
        ))
        
        # Department bars
        colors = [self.colors['primary'] if i % 2 == 0 else self.colors['warning'] 
                 for i in range(len(dept_budgets))]
        
        fig.add_trace(go.Bar(
            name='Department Allocation',
            x=list(dept_budgets.index),
            y=list(dept_budgets.values),
            marker_color=colors,
            text=[f'${val:,.0f}' for val in dept_budgets.values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title={
                'text': 'Budget Allocation Waterfall',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Category',
            yaxis_title='Budget ($)',
            height=400,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        fig.update_layout(yaxis=dict(tickformat='$,.0f'))
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_risk_impact_matrix(self, df):
        """Create risk vs impact scatter plot"""
        # Simulate impact scores based on budget and team size
        df_copy = df.copy()
        df_copy['impact'] = (df_copy['budget'] / df_copy['budget'].max() * 5 + 
                           df_copy['team_size'] / df_copy['team_size'].max() * 5)
        
        status_colors = {
            'On Track': self.colors['success'],
            'At Risk': self.colors['warning'],
            'Behind': self.colors['danger'],
            'Complete': self.colors['info']
        }
        
        fig = go.Figure()
        
        for status in df_copy['status'].unique():
            status_data = df_copy[df_copy['status'] == status]
            
            fig.add_trace(go.Scatter(
                x=status_data['risk_score'],
                y=status_data['impact'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=status_colors.get(status, self.colors['primary']),
                    opacity=0.7
                ),
                name=status,
                text=status_data['project_name'],
                hovertemplate='<b>%{text}</b><br>' +
                            'Risk Score: %{x:.1f}<br>' +
                            'Impact Score: %{y:.1f}<br>' +
                            f'Status: {status}<extra></extra>'
            ))
        
        # Add quadrant lines
        fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title={
                'text': 'Risk vs Impact Matrix',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Risk Score',
            yaxis_title='Impact Score',
            height=500,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        fig.update_layout(
            xaxis=dict(range=[0, 10]),
            yaxis=dict(range=[0, 10])
        )
        
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
    
    def create_team_heatmap(self, df):
        """Create team allocation heatmap"""
        # Create matrix of departments vs managers
        heatmap_data = df.pivot_table(
            values='team_size', 
            index='department', 
            columns='manager', 
            aggfunc='sum', 
            fill_value=0
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Oranges',
            text=heatmap_data.values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate='<b>%{y}</b><br>' +
                        'Manager: %{x}<br>' +
                        'Team Size: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': 'Team Allocation Heatmap',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.colors['secondary']}
            },
            xaxis_title='Project Manager',
            yaxis_title='Department',
            height=400,
            margin=dict(t=50, b=50, l=150, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_gantt_chart(self, df):
        """Create simplified Gantt chart"""
        # Take subset for visibility
        gantt_df = df.head(10).copy()
        gantt_df['start_date'] = pd.to_datetime(gantt_df['start_date'])
        gantt_df['end_date'] = pd.to_datetime(gantt_df['end_date'])
        
        fig = px.timeline(
            gantt_df,
            x_start='start_date',
            x_end='end_date',
            y='project_name',
            color='status',
            color_discrete_map={
                'On Track': self.colors['success'],
                'At Risk': self.colors['warning'],
                'Behind': self.colors['danger'],
                'Complete': self.colors['info']
            },
            title='Project Timeline (Gantt Chart)'
        )
        
        fig.update_layout(
            height=500,
            margin=dict(t=50, b=50, l=300, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_milestone_progress(self, df):
        """Create milestone progress chart"""
        # Simulate milestone data
        milestones = []
        for _, project in df.head(8).iterrows():
            for i in range(3):
                milestones.append({
                    'project': project['project_name'][:20] + '...' if len(project['project_name']) > 20 else project['project_name'],
                    'milestone': f'M{i+1}',
                    'completion': min(project['progress'] + np.random.uniform(-20, 20), 100)
                })
        
        milestone_df = pd.DataFrame(milestones)
        
        fig = px.bar(
            milestone_df,
            x='milestone',
            y='completion',
            color='project',
            title='Milestone Completion Progress',
            color_discrete_sequence=self.color_sequence
        )
        
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            yaxis_title='Completion (%)',
            xaxis_title='Milestone'
        )
        
        fig.update_layout(yaxis=dict(range=[0, 100]))
        
        st.plotly_chart(fig, use_container_width=True)
