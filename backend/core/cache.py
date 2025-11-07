from typing import Optional, List
import pandas as pd

class DataCache:
    df: Optional[pd.DataFrame] = None
    columns: List[str] = []
    last_filename: Optional[str] = None

cache = DataCache()