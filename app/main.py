"""Main Streamlit Application"""
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

import streamlit as st
import pandas as pd
import numpy as np
from config import *
from data_loader import DataLoader
from analyzer import DataAnalyzer
from insights import InsightsGenerator

# Page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h2 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'df' not in st.session_state:
    st.session_state.df = None

# Header
st.markdown(f"""
    <div class="main-header">
        <h1>{APP_ICON} {APP_TITLE}</h1>
        <p>{APP_DESCRIPTION}</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">Version {APP_VERSION}</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    show_advanced = st.checkbox("🔬 Advanced Options", value=False)
    
    st.markdown("---")
    
    st.markdown("### 📊 About")
    st.info(f"""
    **{APP_TITLE}**
    
    Professional data analysis platform built with Python and Streamlit.
    
    **Version:** {APP_VERSION}
    
    **Features:**
    - 📁 Multi-format file support
    - 📊 Automatic data profiling
    - 🔍 Outlier detection
    - 📈 Statistical analysis
    - 💡 Smart insights
    """)
    
    st.markdown("---")
    
    st.markdown("### 📚 Tech Stack")
    st.code("""
Python 3.10+
Streamlit
Pandas & NumPy
Matplotlib & Seaborn
SciPy & Scikit-learn
    """, language="text")
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - Upload CSV, Excel, or JSON files
    - Max file size: 200MB
    - Data is processed securely
    - No data is stored
    """)

# Main content area
st.markdown("## 📁 Upload Your Data")

# File upload
uploaded_file = st.file_uploader(
    "Choose a file",
    type=ALLOWED_EXTENSIONS,
    help=f"Supported formats: {', '.join(ALLOWED_EXTENSIONS)} | Max size: {MAX_FILE_SIZE_MB}MB"
)

if uploaded_file is None:
    st.info("👆 Upload a CSV, Excel, or JSON file to begin analysis")
    
    # Show examples
    st.markdown("### 💡 What Can You Analyze?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Business Data**
        - Sales reports
        - Customer analytics
        - Financial statements
        - Marketing metrics
        """)
    
    with col2:
        st.markdown("""
        **🔬 Research Data**
        - Survey results
        - Experimental data
        - Statistical studies
        - Scientific measurements
        """)
    
    with col3:
        st.markdown("""
        **📈 Personal Data**
        - Fitness tracking
        - Budget analysis
        - Time management
        - Habit tracking
        """)
    
    st.stop()

# Load data
try:
    with st.spinner("🔄 Loading and analyzing your data..."):
        df = DataLoader.load_file(uploaded_file)
        st.session_state.df = df
    
    st.success(f"✅ Successfully loaded **{uploaded_file.name}** ({len(df):,} rows × {len(df.columns)} columns)")
    
except Exception as e:
    st.error(f"❌ Error loading file: {str(e)}")
    st.info("💡 Please make sure your file is properly formatted and try again.")
    st.stop()

# Data overview section
st.markdown("---")
st.markdown("## 📊 Data Overview")

# Get summary statistics
try:
    summary = DataAnalyzer.get_summary(df)
except Exception as e:
    st.error(f"Error analyzing data: {e}")
    st.stop()

# Display metric cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h2>{summary['shape']['rows']:,}</h2>
            <p>Total Rows</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h2>{summary['shape']['columns']}</h2>
            <p>Columns</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h2>{summary['memory_mb']:.1f} MB</h2>
            <p>Memory Usage</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    missing_pct = (summary['missing_total'] / (summary['shape']['rows'] * summary['shape']['columns']) * 100)
    st.markdown(f"""
        <div class="metric-card">
            <h2>{summary['missing_total']:,}</h2>
            <p>Missing Values ({missing_pct:.1f}%)</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Data quality indicator
if summary['missing_total'] == 0 and summary['duplicates'] == 0:
    st.success("✅ **Data Quality: Excellent** - No missing values or duplicates detected!")
elif missing_pct < 5 and summary['duplicates'] < len(df) * 0.05:
    st.success("👍 **Data Quality: Good** - Minimal data quality issues")
elif missing_pct < 20:
    st.warning(f"⚠️ **Data Quality: Fair** - {summary['missing_total']:,} missing values and {summary['duplicates']:,} duplicates found")
else:
    st.error(f"❌ **Data Quality: Needs Attention** - Significant data quality issues detected")

# AI-Powered Insights Section
st.markdown("### 🤖 AI-Powered Insights")

with st.spinner("Generating intelligent insights..."):
    insights = InsightsGenerator.generate_insights(df, summary)
    numeric_insights = InsightsGenerator.generate_numeric_insights(df)
    all_insights = insights + numeric_insights

# Display insights in a beautiful grid
cols = st.columns(2)
for idx, insight in enumerate(all_insights[:6]):  # Show top 6 insights
    with cols[idx % 2]:
        # Color based on impact
        if insight['impact'] == 'high':
            border_color = "#ff6b6b"
        elif insight['impact'] == 'medium':
            border_color = "#ffa726"
        else:
            border_color = "#66bb6a"
        
        st.markdown(f"""
            <div style="
                border-left: 4px solid {border_color};
                padding: 1rem;
                margin: 0.5rem 0;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <h4 style="margin: 0; color: #2c3e50;">
                    {insight['icon']} {insight['title']}
                </h4>
                <p style="margin: 0.5rem 0 0 0; color: #34495e; font-size: 0.9rem;">
                    {insight['description']}
                </p>
            </div>
        """, unsafe_allow_html=True)

# Column types breakdown
st.markdown("### 📋 Column Types")
col_types = summary['column_types']

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔢 Numeric Columns", len(col_types['numeric']))
    if col_types['numeric']:
        with st.expander("View numeric columns"):
            for col in col_types['numeric']:
                st.text(f"• {col}")

with col2:
    st.metric("📝 Categorical Columns", len(col_types['categorical']))
    if col_types['categorical']:
        with st.expander("View categorical columns"):
            for col in col_types['categorical']:
                st.text(f"• {col}")

with col3:
    st.metric("📅 DateTime Columns", len(col_types['datetime']))
    if col_types['datetime']:
        with st.expander("View datetime columns"):
            for col in col_types['datetime']:
                st.text(f"• {col}")

# Data preview
st.markdown("### 👁️ Data Preview")
with st.expander("Click to view first 100 rows", expanded=False):
    st.dataframe(
        df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Dataset as CSV",
        data=csv,
        file_name=f"{uploaded_file.name.split('.')[0]}_processed.csv",
        mime="text/csv",
        key='download-full'
    )

# Column details
with st.expander("📊 Detailed Column Information"):
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str).values,
        'Non-Null Count': df.count().values,
        'Null Count': df.isnull().sum().values,
        'Null %': (df.isnull().sum() / len(df) * 100).round(2).values,
        'Unique Values': df.nunique().values
    })
    st.dataframe(col_info, use_container_width=True)

# Analysis section
st.markdown("---")
st.markdown("## 🔬 Data Analysis")

# Analysis type selection
analysis_type = st.selectbox(
    "Select Analysis Type",
    [
        "📊 Statistical Summary",
        "🔍 Outlier Detection",
        "📋 Data Types",
        "⚠️ Missing Values Analysis",
        "🔗 Correlation Analysis"
    ],
    help="Choose the type of analysis you want to perform"
)

# Run analysis button
if st.button("▶️ Run Analysis", type="primary", use_container_width=False):
    with st.spinner("🔄 Analyzing your data..."):
        
        try:
            if analysis_type == "📊 Statistical Summary":
                st.markdown("### Statistical Summary")
                st.write("Descriptive statistics for numeric columns:")
                
                numeric_df = df.select_dtypes(include=[np.number])
                if len(numeric_df.columns) > 0:
                    stats_df = numeric_df.describe().T
                    stats_df['variance'] = numeric_df.var()
                    stats_df = stats_df.round(2)
                    st.dataframe(stats_df, use_container_width=True)
                    
                    # Download statistics
                    csv_stats = stats_df.to_csv().encode('utf-8')
                    st.download_button(
                        "📥 Download Statistics",
                        csv_stats,
                        "statistics.csv",
                        "text/csv"
                    )
                else:
                    st.warning("No numeric columns found in the dataset.")
            
            elif analysis_type == "🔍 Outlier Detection":
                st.markdown("### Outlier Detection (Z-Score Method)")
                st.write(f"Using threshold: Z-score > {OUTLIER_THRESHOLD}")
                
                outliers = DataAnalyzer.detect_outliers(df)
                
                if len(outliers) > 0:
                    outlier_pct = len(outliers) / len(df) * 100
                    st.warning(f"Found **{len(outliers):,} outliers** ({outlier_pct:.2f}% of total data)")
                    
                    st.markdown("#### Outlier Rows (Top 20)")
                    st.dataframe(outliers.head(20), use_container_width=True)
                    
                    # Download outliers
                    csv_outliers = outliers.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download All Outliers",
                        csv_outliers,
                        "outliers.csv",
                        "text/csv"
                    )
                else:
                    st.success("✅ No outliers detected! Your data looks clean.")
            
            elif analysis_type == "📋 Data Types":
                st.markdown("### Data Type Classification")
                
                types = DataAnalyzer.detect_column_types(df)
                
                st.json({
                    "Numeric Columns": types['numeric'],
                    "Categorical Columns": types['categorical'],
                    "DateTime Columns": types['datetime']
                })
                
                # Visualization
                type_counts = {
                    'Numeric': len(types['numeric']),
                    'Categorical': len(types['categorical']),
                    'DateTime': len(types['datetime'])
                }
                
                st.bar_chart(type_counts)
            
            elif analysis_type == "⚠️ Missing Values Analysis":
                st.markdown("### Missing Values Analysis")
                
                missing = df.isnull().sum()
                missing_df = pd.DataFrame({
                    'Column': missing.index,
                    'Missing Count': missing.values,
                    'Percentage': (missing.values / len(df) * 100).round(2),
                    'Data Type': df.dtypes.values
                })
                
                # Show only columns with missing values
                missing_df = missing_df[missing_df['Missing Count'] > 0]
                
                if len(missing_df) > 0:
                    st.warning(f"Found missing values in {len(missing_df)} columns")
                    st.dataframe(
                        missing_df.sort_values('Missing Count', ascending=False),
                        use_container_width=True
                    )
                    
                    # Visualization
                    st.markdown("#### Missing Values Visualization")
                    st.bar_chart(missing_df.set_index('Column')['Missing Count'])
                else:
                    st.success("✅ No missing values found! Your dataset is complete.")
            
            elif analysis_type == "🔗 Correlation Analysis":
                st.markdown("### Correlation Analysis")
                
                numeric_df = df.select_dtypes(include=[np.number])
                
                if len(numeric_df.columns) >= 2:
                    correlation = numeric_df.corr()
                    st.write("Correlation matrix for numeric columns:")
                    st.dataframe(correlation.round(3), use_container_width=True)
                    
                    # Find strong correlations
                    st.markdown("#### Strong Correlations (|r| > 0.7)")
                    strong_corr = []
                    for i in range(len(correlation.columns)):
                        for j in range(i+1, len(correlation.columns)):
                            if abs(correlation.iloc[i, j]) > 0.7:
                                strong_corr.append({
                                    'Variable 1': correlation.columns[i],
                                    'Variable 2': correlation.columns[j],
                                    'Correlation': round(correlation.iloc[i, j], 3)
                                })
                    
                    if strong_corr:
                        st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
                    else:
                        st.info("No strong correlations (|r| > 0.7) found.")
                else:
                    st.warning("Need at least 2 numeric columns for correlation analysis.")
            
            st.success("✅ Analysis complete!")
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.info("Please check your data format and try again.")

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p style='font-size: 1.2rem; font-weight: 600;'>{APP_TITLE} v{APP_VERSION}</p>
        <p>Built with ❤️ using Streamlit and Python</p>
        <p style='font-size: 0.9rem; margin-top: 1rem;'>
            Professional Data Analysis Platform | Secure • Fast • Reliable
        </p>
    </div>
""", unsafe_allow_html=True)