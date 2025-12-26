"""Data Analysis Module"""
from typing import Dict, List
import pandas as pd
import numpy as np
from scipy import stats
from config import MAX_CATEGORIES, OUTLIER_THRESHOLD

class DataAnalyzer:
    """Data analysis functions"""
    
    @staticmethod
    def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Detect column types"""
        numeric = df.select_dtypes(include=[np.number]).columns.tolist()
        datetime_cols = []
        categorical = []
        
        for col in df.columns:
            if col in numeric:
                continue
            
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                datetime_cols.append(col)
            elif df[col].nunique() <= MAX_CATEGORIES:
                categorical.append(col)
        
        return {
            "numeric": numeric,
            "categorical": categorical,
            "datetime": datetime_cols
        }
    
    @staticmethod
    def get_summary(df: pd.DataFrame) -> Dict:
        """Get data summary"""
        types = DataAnalyzer.detect_column_types(df)
        missing = df.isnull().sum()
        
        return {
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "memory_mb": df.memory_usage(deep=True).sum() / (1024 ** 2),
            "column_types": types,
            "missing_total": int(missing.sum()),
            "duplicates": int(df.duplicated().sum())
        }
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
        """Detect outliers using z-score"""
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if len(numeric_df.columns) == 0:
            return pd.DataFrame()
        
        z_scores = np.abs(stats.zscore(numeric_df))
        outlier_mask = (z_scores > OUTLIER_THRESHOLD).any(axis=1)
        
        return df.loc[outlier_mask].copy()