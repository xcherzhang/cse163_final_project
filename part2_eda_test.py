"""
Cher Zhang
CSE 163 AA
Final Project Part 2 - Exploratory Data Analysis (EDA)

This program tests the exploratory data analysis functions with
small test datasets. It also tests the row dimensions of the
NHANES 2023 and 2020 datasets against expected values
obtained from official NHANES documentation.
"""

# import libraries
import os
import pandas as pd
import part2_eda_main as eda


def test_data_dimensions() -> None:
    """
    Test the row dimensions of the dataframes against expected values
    obtained from official NHANES documentation.
    """
    assert eda.demo_2023["SEQN"].nunique() == 11933
    assert eda.supl_2023["SEQN"].nunique() == 8860
    assert eda.filtered_2023["SEQN"].nunique() == 8860

    assert eda.demo_2023["SEQN"].is_unique is True
    assert eda.supl_2023["SEQN"].is_unique is True
    assert eda.filtered_2023["SEQN"].is_unique is True

    assert eda.demo_2020["SEQN"].nunique() == 15560
    assert eda.supl_2020["SEQN"].nunique() == 15560
    assert eda.filtered_2020["SEQN"].nunique() == 15560

    assert eda.demo_2020["SEQN"].is_unique is True
    assert eda.supl_2020["SEQN"].is_unique is True
    assert eda.filtered_2020["SEQN"].is_unique is True


# small test dataframe
test_df = pd.DataFrame({
    "RIDAGEYR": [20, 30, 40, 50],
    "DSQTVC": [100, 200, 300, 400],
    "DSQTVD": [10, 20, 30, 40],
    "RIAGENDR": [1, 2, 1, 2]
})


def test_missing_value_summary():
    """
    Test missing value counts and percentages.
    """
    df = pd.DataFrame({
        "A": [1, None, 3, None],
        "B": [1, 2, 3, 4]
    })

    result = eda.missing_value_summary(df)

    assert result.loc[0, "Column"] == "A"
    assert result.loc[0, "Missing_Count"] == 2
    assert result.loc[0, "Missing_Percentage"] == 50

    assert result.loc[1, "Column"] == "B"
    assert result.loc[1, "Missing_Count"] == 0
    assert result.loc[1, "Missing_Percentage"] == 0


def test_quantitative_variable_summary():
    """
    Test quantitative summary statistics.
    """
    df = pd.DataFrame({"A": [1, 2, 3, 4]})

    result = eda.quantitative_variable_summary(df, ["A"])

    assert result.loc["A", "Mean"] == 2.5
    assert result.loc["A", "Min"] == 1
    assert result.loc["A", "Q1"] == 1.75
    assert result.loc["A", "Median"] == 2.5
    assert result.loc["A", "Q3"] == 3.25
    assert result.loc["A", "Max"] == 4
    assert abs(result.loc["A", "Std_Dev"] - 1.290994) < 0.001


def test_categorical_variable_summary():
    """
    Test categorical response counts, including missing values.
    """
    df = pd.DataFrame({"Gender": [1, 2, 1, 2, 1]})

    result = eda.categorical_variable_summary(df, "Gender")
    counts = dict(zip(result["Gender"], result["Count"]))

    assert counts[1.0] == 3
    assert counts[2.0] == 2


def test_plot_age_distribution():
    """
    Test that age histogram uses the correct data and displays.
    """
    if os.path.exists("test_age.png"):
        os.remove("test_age.png")

    df = pd.DataFrame({"RIDAGEYR": [20, 30, 40, 50]})

    eda.plot_age_distribution(df, "Test Age", "test_age.png")
    assert os.path.exists("test_age.png")


def test_plot_mean_nutrient_intake():
    """
    Test that mean nutrient intake is calculated and plotted.
    """
    if os.path.exists("test_nutrient.png"):
        os.remove("test_nutrient.png")

    df = pd.DataFrame({"DSQTVC": [100, 200, 300],
                       "DSQTVD": [10, 20, 30]})

    eda.plot_mean_nutrient_intake(df,
                                  ["DSQTVC", "DSQTVD"],
                                  "Test Nutrient",
                                  "test_nutrient.png")
    assert os.path.exists("test_nutrient.png")


def main():
    """
    Run all test functions.
    """
    test_data_dimensions()
    test_missing_value_summary()
    test_quantitative_variable_summary()
    test_categorical_variable_summary()
    test_plot_age_distribution()
    test_plot_mean_nutrient_intake()
    print("All tests passed!")


if __name__ == "__main__":
    main()
