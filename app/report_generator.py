"""
Report Generator for Data Analysis
"""
import pandas as pd
from datetime import datetime


class ReportGenerator:
    """Generate downloadable reports"""
    
    @staticmethod
    def generate_text_report(df: pd.DataFrame, summary: dict, insights: list = None) -> str:
        """Generate a comprehensive text report"""
        
        report = []
        report.append("=" * 80)
        report.append("DATA ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Analysis Tool: AI Data Analyst Pro v1.0.0")
        report.append(f"Powered by: Python, Pandas, NumPy, SciPy\n")
        
        # Executive Summary
        report.append("\n" + "=" * 80)
        report.append("EXECUTIVE SUMMARY")
        report.append("=" * 80)
        report.append(f"\nDataset Size: {summary['shape']['rows']:,} rows × {summary['shape']['columns']} columns")
        report.append(f"Memory Usage: {summary['memory_mb']:.2f} MB")
        
        missing_pct = (summary['missing_total'] / 
                      (summary['shape']['rows'] * summary['shape']['columns']) * 100)
        report.append(f"Missing Values: {summary['missing_total']:,} ({missing_pct:.2f}%)")
        report.append(f"Duplicate Rows: {summary['duplicates']:,}")
        
        # Data Quality Score
        if missing_pct == 0 and summary['duplicates'] == 0:
            quality = "EXCELLENT ⭐⭐⭐⭐⭐"
        elif missing_pct < 5:
            quality = "GOOD ⭐⭐⭐⭐"
        elif missing_pct < 20:
            quality = "FAIR ⭐⭐⭐"
        else:
            quality = "NEEDS ATTENTION ⭐⭐"
        
        report.append(f"\nData Quality Score: {quality}")
        
        # Column Information
        report.append("\n" + "=" * 80)
        report.append("COLUMN INFORMATION")
        report.append("=" * 80)
        
        types = summary['column_types']
        
        report.append(f"\nNumeric Columns ({len(types['numeric'])}):")
        if types['numeric']:
            for col in types['numeric']:
                report.append(f"  • {col}")
        else:
            report.append("  (none)")
        
        report.append(f"\nCategorical Columns ({len(types['categorical'])}):")
        if types['categorical']:
            for col in types['categorical']:
                report.append(f"  • {col}")
        else:
            report.append("  (none)")
        
        report.append(f"\nDateTime Columns ({len(types['datetime'])}):")
        if types['datetime']:
            for col in types['datetime']:
                report.append(f"  • {col}")
        else:
            report.append("  (none)")
        
        # Statistical Summary
        if types['numeric']:
            report.append("\n" + "=" * 80)
            report.append("STATISTICAL SUMMARY (Numeric Columns)")
            report.append("=" * 80)
            
            stats = df[types['numeric']].describe()
            report.append("\n" + stats.to_string())
        
        # AI Insights
        if insights and len(insights) > 0:
            report.append("\n" + "=" * 80)
            report.append("AI-POWERED INSIGHTS")
            report.append("=" * 80)
            
            for i, insight in enumerate(insights, 1):
                report.append(f"\n{i}. {insight['icon']} {insight['title']}")
                report.append(f"   {insight['description']}")
                report.append(f"   Impact Level: {insight['impact'].upper()}")
        
        # Data Quality Details
        report.append("\n" + "=" * 80)
        report.append("DATA QUALITY DETAILS")
        report.append("=" * 80)
        
        missing = df.isnull().sum()
        missing_cols = missing[missing > 0]
        
        if len(missing_cols) > 0:
            report.append("\nColumns with Missing Values:")
            for col, count in missing_cols.items():
                pct = (count / len(df) * 100)
                report.append(f"  • {col}: {count:,} missing ({pct:.2f}%)")
        else:
            report.append("\n✓ No missing values detected - Excellent data quality!")
        
        if summary['duplicates'] > 0:
            dup_pct = (summary['duplicates'] / len(df) * 100)
            report.append(f"\n⚠ Duplicate Rows: {summary['duplicates']:,} ({dup_pct:.2f}%)")
        else:
            report.append("\n✓ No duplicate rows detected!")
        
        # Top Values for Categorical Columns
        if types['categorical']:
            report.append("\n" + "=" * 80)
            report.append("CATEGORICAL ANALYSIS")
            report.append("=" * 80)
            
            for col in types['categorical'][:3]:  # Top 3 categorical columns
                report.append(f"\nTop 5 Values in '{col}':")
                top_values = df[col].value_counts().head(5)
                for val, count in top_values.items():
                    pct = (count / len(df) * 100)
                    report.append(f"  • {val}: {count:,} ({pct:.1f}%)")
        
        # Recommendations
        report.append("\n" + "=" * 80)
        report.append("RECOMMENDATIONS")
        report.append("=" * 80)
        
        recommendations = []
        
        if missing_pct > 5:
            recommendations.append("ADDRESS MISSING DATA")
            recommendations.append("  • Consider imputation strategies (mean, median, mode)")
            recommendations.append("  • Analyze patterns in missing data (MCAR, MAR, MNAR)")
            recommendations.append("  • Evaluate impact on analysis results")
        
        if summary['duplicates'] > 0:
            recommendations.append("\nHANDLE DUPLICATE RECORDS")
            recommendations.append("  • Review duplicate rows for data entry errors")
            recommendations.append("  • Determine if duplicates are intentional or errors")
            recommendations.append("  • Remove or consolidate duplicate entries")
        
        if len(types['numeric']) >= 2:
            recommendations.append("\nPERFORM CORRELATION ANALYSIS")
            recommendations.append("  • Identify relationships between numeric variables")
            recommendations.append("  • Check for multicollinearity issues")
            recommendations.append("  • Use correlation insights for feature selection")
        
        if len(types['datetime']) > 0:
            recommendations.append("\nCONDUCT TIME SERIES ANALYSIS")
            recommendations.append("  • Analyze trends and seasonality patterns")
            recommendations.append("  • Detect anomalies in time-based data")
            recommendations.append("  • Consider forecasting if applicable")
        
        if len(types['numeric']) > 0:
            recommendations.append("\nOUTLIER DETECTION")
            recommendations.append("  • Use Z-score or IQR methods")
            recommendations.append("  • Investigate causes of outliers")
            recommendations.append("  • Decide on handling strategy (remove, cap, or keep)")
        
        if recommendations:
            for rec in recommendations:
                report.append(f"\n{rec}")
        else:
            report.append("\n✓ Your data looks great! Proceed with analysis.")
        
        # Footer
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated by AI Data Analyst Pro")
        report.append(f"© {datetime.now().year} - Professional Data Analysis Platform")
        report.append("\nFor more features, visit: https://github.com/divya-vj/ai-data-analyst")
        
        return "\n".join(report)