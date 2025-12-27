"""
AI-Powered Insights Generator
"""
import pandas as pd
import numpy as np


class InsightsGenerator:
    """Generate intelligent insights from data"""
    
    @staticmethod
    def generate_insights(df: pd.DataFrame, summary: dict) -> list:
        """Generate insights based on data analysis"""
        insights = []
        
        # Data Quality Insights
        missing_pct = (summary['missing_total'] / 
                      (summary['shape']['rows'] * summary['shape']['columns']) * 100)
        
        if missing_pct == 0:
            insights.append({
                'icon': '✅',
                'title': 'Excellent Data Quality',
                'description': 'Your dataset has no missing values. This indicates high-quality data collection.',
                'impact': 'high'
            })
        elif missing_pct < 5:
            insights.append({
                'icon': '👍',
                'title': 'Good Data Quality',
                'description': f'Only {missing_pct:.1f}% of data is missing. Minimal cleaning required.',
                'impact': 'medium'
            })
        else:
            insights.append({
                'icon': '⚠️',
                'title': 'Data Quality Needs Attention',
                'description': f'{missing_pct:.1f}% of data is missing. Consider data imputation strategies.',
                'impact': 'high'
            })
        
        # Duplicate Insights
        dup_pct = (summary['duplicates'] / summary['shape']['rows'] * 100)
        if summary['duplicates'] > 0:
            insights.append({
                'icon': '🔄',
                'title': 'Duplicate Records Found',
                'description': f'Found {summary["duplicates"]:,} duplicate rows ({dup_pct:.1f}%). Consider deduplication.',
                'impact': 'medium'
            })
        
        # Column Type Distribution
        types = summary['column_types']
        total_cols = summary['shape']['columns']
        
        if len(types['numeric']) > total_cols * 0.7:
            insights.append({
                'icon': '🔢',
                'title': 'Numeric-Heavy Dataset',
                'description': f'{len(types["numeric"])} of {total_cols} columns are numeric. Ideal for statistical analysis and ML.',
                'impact': 'high'
            })
        
        if len(types['categorical']) > total_cols * 0.5:
            insights.append({
                'icon': '📋',
                'title': 'Categorical-Rich Data',
                'description': f'{len(types["categorical"])} categorical columns found. Consider one-hot encoding for ML.',
                'impact': 'medium'
            })
        
        # Dataset Size Insights
        rows = summary['shape']['rows']
        if rows < 100:
            insights.append({
                'icon': '⚠️',
                'title': 'Small Dataset',
                'description': f'Only {rows} rows. Results may not be statistically significant.',
                'impact': 'high'
            })
        elif rows > 10000:
            insights.append({
                'icon': '🚀',
                'title': 'Large Dataset Detected',
                'description': f'{rows:,} rows available. Excellent sample size for robust analysis.',
                'impact': 'high'
            })
        
        # Memory Usage
        memory_mb = summary['memory_mb']
        if memory_mb > 100:
            insights.append({
                'icon': '💾',
                'title': 'Large Memory Footprint',
                'description': f'{memory_mb:.1f} MB in memory. Consider data type optimization.',
                'impact': 'low'
            })
        
        # Advanced Analysis Recommendations
        if len(types['numeric']) >= 2:
            insights.append({
                'icon': '📈',
                'title': 'Correlation Analysis Recommended',
                'description': 'Multiple numeric columns detected. Run correlation analysis to find relationships.',
                'impact': 'high'
            })
        
        if len(types['datetime']) > 0:
            insights.append({
                'icon': '📅',
                'title': 'Time Series Analysis Possible',
                'description': f'Found {len(types["datetime"])} datetime column(s). Time-based trends can be analyzed.',
                'impact': 'high'
            })
        
        return insights
    
    @staticmethod
    def generate_numeric_insights(df: pd.DataFrame) -> list:
        """Generate insights for numeric columns"""
        insights = []
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) == 0:
            return insights
        
        # Variance insights
        variances = numeric_df.var()
        low_variance = variances[variances < 0.01].index.tolist()
        
        if low_variance:
            insights.append({
                'icon': '📊',
                'title': 'Low Variance Columns Detected',
                'description': f'Columns {", ".join(low_variance[:3])} have very low variance. May not be useful for analysis.',
                'impact': 'medium'
            })
        
        # Outlier potential
        for col in numeric_df.columns[:3]:  # Check first 3 columns
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1
            outlier_count = ((numeric_df[col] < (q1 - 1.5 * iqr)) | 
                           (numeric_df[col] > (q3 + 1.5 * iqr))).sum()
            
            if outlier_count > len(df) * 0.05:  # More than 5% outliers
                insights.append({
                    'icon': '🎯',
                    'title': f'Outliers in {col}',
                    'description': f'{outlier_count} potential outliers detected ({outlier_count/len(df)*100:.1f}%).',
                    'impact': 'medium'
                })
        
        return insights