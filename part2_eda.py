# import libraries
import pandas as pd
import matplotlib.pyplot as plt


# global data files
DEMO2023 = "DEMO_L.xpt"
SUPL2023 = "DSQTOT_L.xpt"
DEMO2020 = "P_DEMO.xpt"
SUPL2020 = "P_DSQTOT.xpt"


# columns of interest by question types
demo_columns = ["SEQN", "RIDAGEYR", "RIAGENDR", "RIDRETH3", "DMDEDUC2"]
supl_columns = ["DSD010", "DSQTVC", "DSQTVD", "DSQTCALC", "DSQTMAGN"]


# columns of interest by variable types
categorical_columns = ["RIAGENDR", "RIDRETH3", "DMDEDUC2"]
quantitative_columns = ["RIDAGEYR", "DSD010", "DSQTVC", "DSQTVD", "DSQTCALC", "DSQTMAGN"]


def load_xpt_data(file_path: str) -> pd.DataFrame:
    """
    Take in an xpt file and return a DataFrame.
    """
    return pd.read_sas(file_path)


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on_column: str) -> pd.DataFrame:
    """
    Take in two DataFrames and merge them on a specified column.
    """
    return pd.merge(df1, df2, on=on_column)


def filter_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Take in a DataFrame and a list of columns, and return a DataFrame with only those columns.
    """
    return df[columns]


def data_dimension(df: pd.DataFrame) -> tuple:
    """
    Take in a DataFrame and return its dimensions.
    """
    return df.shape


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Take in a DataFrame and return a DataFrame with the count of missing values for each column.
    """
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["Column", "Missing_Count"]
    missing_df["Missing_Percentage"] = (missing_df["Missing_Count"] / len(df)) * 100
    return missing_df


def quantitative_variable_summary(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Take in a DataFrame and a list of quantitative columns, and return a DataFrame with a seven-number summary
    (mean, standard deviation, minimum, first quartile, median, third quartile, maximum).
    """
    summary_df = df[columns].describe().transpose()
    summary_df = summary_df[["mean", "std", "min", "25%", "50%", "75%", "max"]]
    summary_df.columns = ["Mean", "Std_Dev", "Min", "Q1", "Median", "Q3", "Max"]
    return summary_df


def categorical_variable_summary(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Take in a DataFrame and a categorical column, and return a DataFrame with unique responses
    and their counts.
    """
    result = df[column].value_counts(dropna=False).reset_index()
    result.columns = [column, "Count"]
    return result


def main():
    # load the data
    demo_2023 = load_xpt_data(DEMO2023)
    supl_2023 = load_xpt_data(SUPL2023)
    demo_2020 = load_xpt_data(DEMO2020)
    supl_2020 = load_xpt_data(SUPL2020)

    # merge the dataframes
    merged_2023 = merge_dataframes(demo_2023, supl_2023, on_column="SEQN")
    merged_2020 = merge_dataframes(demo_2020, supl_2020, on_column="SEQN")

    # get dimensions of the merged dataframes
    dim_2023 = data_dimension(merged_2023)
    dim_2020 = data_dimension(merged_2020)

    print(f"Dimensions of merged 2023 data (rows, columns): {dim_2023}")
    print(f"Dimensions of merged 2020 data (rows, columns): {dim_2020}")
    print()

    # get dimensions of the filtered dataframes
    filtered_2023 = filter_columns(merged_2023, demo_columns + supl_columns)
    filtered_2020 = filter_columns(merged_2020, demo_columns + supl_columns)

    dim_filtered_2023 = data_dimension(filtered_2023)
    dim_filtered_2020 = data_dimension(filtered_2020)

    print(f"Dimensions of filtered 2023 data (rows, columns): {dim_filtered_2023}")
    print(f"Dimensions of filtered 2020 data (rows, columns): {dim_filtered_2020}")
    print()

    # get missing value summary for the filtered dataframes
    missing_summary_2023 = missing_value_summary(filtered_2023)
    missing_summary_2020 = missing_value_summary(filtered_2020)

    print("Missing value summary for filtered 2023 data:")
    print(missing_summary_2023)
    print()
    print("Missing value summary for filtered 2020 data:")
    print(missing_summary_2020)
    print()

    # get quantitative variable summary for the filtered dataframes
    quantitative_summary_2023 = quantitative_variable_summary(filtered_2023, quantitative_columns)
    quantitative_summary_2020 = quantitative_variable_summary(filtered_2020, quantitative_columns)

    print("Quantitative variable summary for filtered 2023 data:")
    print(quantitative_summary_2023)
    print()
    print("Quantitative variable summary for filtered 2020 data:")
    print(quantitative_summary_2020)
    print()

    # get categorical variable summary for the filtered dataframes
    print("Categorical variable summary for filtered 2023 data:")
    for column in categorical_columns:
        summary = categorical_variable_summary(filtered_2023, column)
        print(f"- Summary for {column}:")
        print(summary)
    print()
    print("Categorical variable summary for filtered 2020 data:")
    for column in categorical_columns:
        summary = categorical_variable_summary(filtered_2020, column)
        print(f"- Summary for {column}:")
        print(summary)

if __name__ == "__main__":
    main()
