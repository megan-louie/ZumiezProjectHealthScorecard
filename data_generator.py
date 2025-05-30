import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

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
        self.risk_factors = ['Low', 'Medium', 'High', 'Critical']
        
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
    
    def generate_milestone_data(self, projects_df):
        """Generate milestone data for projects"""
        milestones = []
        
        for _, project in projects_df.iterrows():
            num_milestones = random.randint(3, 8)
            project_milestones = []
            
            for i in range(num_milestones):
                milestone = {
                    'project_name': project['project_name'],
                    'milestone': f"Milestone {i+1}",
                    'completion': random.uniform(0, 100),
                    'due_date': datetime.now() + timedelta(days=random.randint(-30, 90))
                }
                project_milestones.append(milestone)
            
            milestones.extend(project_milestones)
        
        return pd.DataFrame(milestones)
    
    def generate_all_data(self):
        """Generate complete dataset for dashboard"""
        projects_df = self.generate_projects_data()
        kpi_data = self.generate_kpi_data(projects_df)
        milestone_data = self.generate_milestone_data(projects_df)
        
        return {
            'projects': projects_df,
            'kpis': kpi_data,
            'milestones': milestone_data
        }
