"""Data Loading Module"""
import io
from pathlib import Path
from typing import Union, Any
import pandas as pd


class DataLoader:
    """Handles data loading"""
    
    @staticmethod
    def load_file(file_source: Union[str, Path, Any]) -> pd.DataFrame:
        """Load data from file"""
        try:
            # Handle file paths
            if isinstance(file_source, (str, Path)):
                path = Path(file_source)
                suffix = path.suffix.lower()
                
                if suffix == ".csv":
                    return pd.read_csv(path)
                elif suffix in [".xlsx", ".xls"]:
                    return pd.read_excel(path)
                elif suffix == ".json":
                    return pd.read_json(path)
            
            # Handle uploaded files (Streamlit)
            filename = getattr(file_source, "name", "")
            suffix = Path(filename).suffix.lower()
            data = file_source.read()
            
            if isinstance(data, str):
                data = data.encode("utf-8")
            
            buffer = io.BytesIO(data)
            
            if suffix == ".csv":
                buffer.seek(0)
                return pd.read_csv(buffer)
            elif suffix in [".xlsx", ".xls"]:
                buffer.seek(0)
                return pd.read_excel(buffer)
            elif suffix == ".json":
                buffer.seek(0)
                return pd.read_json(buffer)
            
            # Default to CSV
            buffer.seek(0)
            return pd.read_csv(buffer)
            
        except Exception as e:
            raise ValueError(f"Failed to load file: {str(e)}")