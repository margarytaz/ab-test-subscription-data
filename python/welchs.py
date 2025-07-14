import pandas as pd
from scipy import stats
import sys

csv_file_path = 'ab_test_dataset.csv'

numerical_column_idx = 5
categorical_column_idx = 6
category_1 = 'Weekday'
category_2 = 'Weekend'

if __name__ == "__main__":
    print(f"Attempting to perform Welch's t-test on numerical data from column {numerical_column_idx + 1} (F) "
          f"comparing '{category_1}' vs. '{category_2}' from categorical data in column {categorical_column_idx + 1} (G) "
          f"using file: '{csv_file_path}'\n")

    try:
        df = pd.read_csv(csv_file_path, header=None)
        if categorical_column_idx in df.columns:
            print(df[categorical_column_idx].unique())
        else:
            print(f"Error: Categorical Column (Index {categorical_column_idx}) not found. "
                  "Please check if your CSV has enough columns.")

        print(f"\nData type of Numerical Column (Index {numerical_column_idx}):")
   
        if numerical_column_idx in df.columns:
            print(df[numerical_column_idx].dtype)
        else:
            print(f"Error: Numerical Column (Index {numerical_column_idx}) not found. "
                  "Please check if your CSV has enough columns.")
        print("----------------------------\n")

    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found. "
              "Please make sure it's in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV file: {e}")
        sys.exit(1)

    if numerical_column_idx not in df.columns or categorical_column_idx not in df.columns:
        print(f"Critical Error: One or both of the required columns (Index {numerical_column_idx}, Index {categorical_column_idx}) "
              "were not found in the CSV file after loading. This usually means your CSV has fewer columns than expected.")
        sys.exit(1)

    df[numerical_column_idx] = pd.to_numeric(df.iloc[:, numerical_column_idx], errors='coerce')

    data_cat1 = df[df[categorical_column_idx] == category_1][numerical_column_idx].dropna()
    data_cat2 = df[df[categorical_column_idx] == category_2][numerical_column_idx].dropna()

    if len(data_cat1) < 2 or len(data_cat2) < 2:
        print("Error: Not enough valid data points in one or both categories to perform Welch's t-test.")
        print(f"  Numerical data for '{category_1}' (from Column G) has {len(data_cat1)} non-NaN values.")
        print(f"  Numerical data for '{category_2}' (from Column G) has {len(data_cat2)} non-NaN values.")
        print("Please ensure each group has at least 2 valid numerical entries for the specified categories.")
        print("\nPossible reasons for this error (check diagnostic info above):")
        print("1. Your CSV does not have a header, and these are indeed the correct column positions.")
        print("2. The category values ('Weekday', 'Weekend') don't exactly match what's in your Column G.")
        print("3. The data in Column F contains non-numeric characters or is empty for these categories.")
        print("4. There are fewer rows than expected, or fewer rows matching the categories.")
        print("5. Your CSV *does* have a header, and you need to tell me the exact header names for columns F and G.")
        sys.exit(1)

    print(f"Comparing numerical values from Column F (Index {numerical_column_idx}):\n")
    print(f"  Mean for '{category_1}' (from Column G): {data_cat1.mean():.2f}")
    print(f"  Mean for '{category_2}' (from Column G): {data_cat2.mean():.2f}\n")

    t_statistic, p_value = stats.ttest_ind(data_cat1, data_cat2, equal_var=False)

    print("-" * 50)
    print(f"Welch's t-statistic: {t_statistic:.4f}")
    print(f"P-value:             {p_value:.4f}")

    alpha = 0.05
    if p_value < alpha:
        print(f"\nConclusion (at significance level alpha={alpha}):")
        print(f"There is a statistically significant difference in subscription durations "
              f"between '{category_1}' and '{category_2}'.")
    else:
        print(f"\nConclusion (at significance level alpha={alpha}):")
        print(f"There is no statistically significant difference in subscription durations "
              f"between '{category_1}' and '{category_2}'.")
