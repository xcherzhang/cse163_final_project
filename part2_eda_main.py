"""
Cher Zhang
CSE 163 AA
Final Project Part 2 - Exploratory Data Analysis (EDA)

This program performs exploratory data analysis on the
NHANES 2023 and 2020 datasets. It includes functions to load, merge,
filter, and summarize the data, as well as to visualize distributions
and mean nutrient intake.
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# global data files
DEMO2023 = "DEMO_L.xpt"
SUPL2023 = "DSQTOT_L.xpt"
DEMO2020 = "P_DEMO.xpt"
SUPL2020 = "P_DSQTOT.xpt"


# columns of interest by question types
demo_columns = ["SEQN", "RIDAGEYR", "RIAGENDR", "RIDRETH3", "DMDEDUC2"]
supl_columns = ["DSD010", "DSQTVC", "DSQTVD", "DSQTCALC", "DSQTMAGN"]


# load the data
demo_2023 = pd.read_sas(DEMO2023)
supl_2023 = pd.read_sas(SUPL2023)
demo_2020 = pd.read_sas(DEMO2020)
supl_2020 = pd.read_sas(SUPL2020)


# merge the dataframes
merged_2023 = pd.merge(demo_2023, supl_2023, on="SEQN")
merged_2020 = pd.merge(demo_2020, supl_2020, on="SEQN")


# filter dataframes
filtered_2023 = merged_2023[demo_columns + supl_columns]
filtered_2020 = merged_2020[demo_columns + supl_columns]


# columns of interest by variable types
categorical_columns = ["RIAGENDR", "RIDRETH3", "DMDEDUC2", "DSD010"]
quantitative_columns = ["RIDAGEYR", "DSQTVC", "DSQTVD", "DSQTCALC", "DSQTMAGN"]


def missing_value_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Take in a DataFrame and return a DataFrame with the count
    of missing values for each column.
    """
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["Column", "Missing_Count"]
    missing_df["Missing_Percentage"] = (missing_df["Missing_Count"]
                                        / len(df)) * 100
    return missing_df


def quantitative_variable_summary(df: pd.DataFrame,
                                  columns: list) -> pd.DataFrame:
    """
    Take in a DataFrame and a list of quantitative columns,
    and return a DataFrame with a seven-number summary
    (mean, standard deviation, minimum, first quartile,
    median, third quartile, maximum).
    """
    summary_df = df[columns].describe().transpose()
    summary_df = summary_df[["mean", "std", "min",
                             "25%", "50%", "75%", "max"]]
    summary_df.columns = ["Mean", "Std_Dev", "Min",
                          "Q1", "Median", "Q3", "Max"]
    return summary_df


def categorical_variable_summary(df: pd.DataFrame,
                                 column: str) -> pd.DataFrame:
    """
    Take in a DataFrame and a categorical column,
    and return a DataFrame with unique responses and their counts.
    """
    result = df[column].value_counts(dropna=True).reset_index()
    result.columns = [column, "Count"]
    return result


def plot_age_distribution(df: pd.DataFrame, title: str,
                          save_path: str = None) -> None:
    """
    Take in a DataFrame and a column name,
    and plot the distribution of that column.
    """
    sns.histplot(df["RIDAGEYR"].dropna(), bins=30, kde=True)
    plt.title(title)
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close()


def plot_mean_nutrient_intake(df: pd.DataFrame,
                              nutrient_columns: list,
                              title: str,
                              save_path: str = None) -> None:
    """
    Take in a DataFrame and a list of nutrient columns,
    and plot the mean intake of each nutrient.
    """
    mean_intake = df[nutrient_columns].mean().reset_index()
    mean_intake.columns = ["Nutrient", "Mean_Intake"]

    sns.barplot(x="Nutrient", y="Mean_Intake", data=mean_intake)
    plt.title(title)
    plt.xlabel("Nutrient")
    plt.ylabel("Mean Intake")
    if save_path:
        plt.savefig(save_path)
    plt.show()
    plt.close()


def main() -> None:
    # get dimensions of dataframes
    dim_2023 = merged_2023.shape
    dim_2020 = merged_2020.shape

    print(f"Dimensions of merged 2023 data (rows, columns): {dim_2023}")
    print(f"Dimensions of merged 2020 data (rows, columns): {dim_2020}")
    print()

    dim_filtered_2023 = filtered_2023.shape
    dim_filtered_2020 = filtered_2020.shape

    print(f"Dimensions of filtered 2023 data (rows, columns): \
          {dim_filtered_2023}")
    print(f"Dimensions of filtered 2020 data (rows, columns): \
          {dim_filtered_2020}")
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
    quant_summary_2023 = quantitative_variable_summary(filtered_2023,
                                                       quantitative_columns)
    quant_summary_2020 = quantitative_variable_summary(filtered_2020,
                                                       quantitative_columns)

    print("Quantitative variable summary for filtered 2023 data:")
    print(quant_summary_2023)
    print()
    print("Quantitative variable summary for filtered 2020 data:")
    print(quant_summary_2020)
    print()

    # get categorical variable summary for the filtered dataframes
    print("Categorical variable summary for filtered 2023 data:")
    for column in categorical_columns:
        summary = categorical_variable_summary(filtered_2023, column)
        print(f"- Summary for {column}:")
        print(summary)
    print("- Summary for SEQN:")
    print(f"Unique SEQN values: {filtered_2023['SEQN'].unique()}")
    print(f"Unique SEQN value counts: {filtered_2023['SEQN'].nunique()}")
    print()
    print("Categorical variable summary for filtered 2020 data:")
    for column in categorical_columns:
        summary = categorical_variable_summary(filtered_2020, column)
        print(f"- Summary for {column}:")
        print(summary)
    print("- Summary for SEQN:")
    print(f"Unique SEQN values: {filtered_2020['SEQN'].unique()}")
    print(f"Unique SEQN value counts: {filtered_2020['SEQN'].nunique()}")

    # plot age distribution for the filtered dataframes
    plot_age_distribution(filtered_2023,
                          "NHANES 2021-2023 Age Distribution",
                          "2023_age_distribution.png")
    plot_age_distribution(filtered_2020,
                          "NHANES 2017-2020 Age Distribution",
                          "2020_age_distribution.png")

    # plot mean nutrient intake for the filtered dataframes
    plot_mean_nutrient_intake(filtered_2023, supl_columns[1:],
                              "NHANES 2021-2023 Mean Nutrient Intake",
                              "2023_mean_nutrient_intake.png")
    plot_mean_nutrient_intake(filtered_2020, supl_columns[1:],
                              "NHANES 2017-2020 Mean Nutrient Intake",
                              "2020_mean_nutrient_intake.png")


if __name__ == "__main__":
    main()
