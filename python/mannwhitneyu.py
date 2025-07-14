import pandas as pd
from scipy.stats import mannwhitneyu
import sys

CSV_FILE_PATH = 'ab_test_dataset.csv'
CATEGORY_COLUMN = 'category'
MOBILE_CATEGORY_VALUE = 'mobile'
DESKTOP_CATEGORY_VALUE = 'desktop'
DURATION_COLUMN = 'subscription_duration_days'

ALPHA = 0.05

try:
    df = pd.read_csv(CSV_FILE_PATH)
    print(f"Successfully loaded data from '{CSV_FILE_PATH}'")
    print("\nFirst 5 rows of the dataset:")
    print(df.head())
    print("\nDataset Info:")
    df.info()
except FileNotFoundError:
    print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    print("Please ensure the CSV_FILE_PATH variable points to the correct file.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while loading the CSV file: {e}")
    sys.exit(1)

mobile_data = df[df[CATEGORY_COLUMN] == MOBILE_CATEGORY_VALUE][DURATION_COLUMN].dropna()
desktop_data = df[df[CATEGORY_COLUMN] == DESKTOP_CATEGORY_VALUE][DURATION_COLUMN].dropna()

if mobile_data.empty:
    print(f"\nWarning: No data found for '{MOBILE_CATEGORY_VALUE}' in the '{CATEGORY_COLUMN}' column.")
    print("Please check the CATEGORY_COLUMN and MOBILE_CATEGORY_VALUE settings.")
    sys.exit(1)
if desktop_data.empty:
    print(f"\nWarning: No data found for '{DESKTOP_CATEGORY_VALUE}' in the '{CATEGORY_COLUMN}' column.")
    print("Please check the CATEGORY_COLUMN and DESKTOP_CATEGORY_VALUE settings.")
    sys.exit(1)

print(f"\nNumber of mobile user subscriptions: {len(mobile_data)}")
print(f"Number of desktop user subscriptions: {len(desktop_data)}")
print(f"Average subscription duration for mobile: {mobile_data.mean():.2f} days")
print(f"Average subscription duration for desktop: {desktop_data.mean():.2f} days")

# --- Mann-Whitney U Test ---
# Hypotheses:
# H0: There is no statistically significant difference in the average subscription duration between mobile and desktop users.
# H1: There is a statistically significant difference in the average subscription duration between mobile and desktop users.

# Perform the Mann-Whitney U test
# 'two-sided' alternative is used because H1 states a "difference", not a specific direction (e.g., mobile > desktop)
u_statistic, p_value = mannwhitneyu(mobile_data, desktop_data, alternative='two-sided')

print(f"\n--- Mann-Whitney U Test Results ---")
print(f"U-statistic: {u_statistic:.2f}")
print(f"P-value: {p_value:.4f}")
print(f"Significance Level (alpha): {ALPHA}")

print("\n--- Conclusion ---")
if p_value < ALPHA:
    print(f"Since the p-value ({p_value:.4f}) is less than the significance level ({ALPHA}),")
    print("we reject the null hypothesis (H0).")
    print("Conclusion: There is a statistically significant difference in the average subscription duration between mobile and desktop users.")
else:
    print(f"Since the p-value ({p_value:.4f}) is greater than or equal to the significance level ({ALPHA}),")
    print("we fail to reject the null hypothesis (H0).")
    print("Conclusion: There is no statistically significant difference in the average subscription duration between mobile and desktop users.")

print("\n--- Hypotheses Recap ---")
print("H0: There is no statistically significant difference in the average subscription duration between mobile and desktop users.")
print("H1: There is a statistically significant difference in the average subscription duration between mobile and desktop users.")