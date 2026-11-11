# import libraries
import pandas as pd
import matplotlib.pyplot as plt


# global data files
DEMO2023 = "DEMO_L.xpt"
SUPL2023 = "DSQTOT_L.xpt"
DEMO2020 = "P_DEMO.xpt"
SUPL2020 = "P_DSQTOT.xpt"


def load_xpt_data(file_path: str) -> pd.DataFrame:
    """
    Take in an xpt file and return a DataFrame.
    """
    return pd.read_sas(file_path)


def data_dimension(data: pd.DataFrame) -> tuple:
    """
    Take in a DataFrame and return its dimensions.
    """
    return data.shape


