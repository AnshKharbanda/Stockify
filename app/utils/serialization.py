import numpy as np
import pandas as pd

def dataframe_to_json(df):
    df = df.copy()

    # Convert datetime columns
    for col in df.select_dtypes(
        include=["datetime64[ns]", "datetimetz"]
    ):
        df[col] = df[col].astype(str)

    # Replace infinities
    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    # Convert dataframe to object type
    df = df.astype(object)

    # Replace NaN with None
    df = df.where(pd.notnull(df), None)

    return df.to_dict(orient="records")