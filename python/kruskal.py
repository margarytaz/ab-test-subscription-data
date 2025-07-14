import pandas as pd
from scipy.stats import kruskal
df = pd.read_csv('ab_test_dataset.csv')

region_data = [df['subscription_duration_days'][df['region'] == region].values for region in df['region'].unique()]

region_data_filtered = [data for data in region_data if len(data) > 0]

if len(region_data_filtered) >= 2:
    h_statistic, p_value = kruskal(*region_data_filtered)

    print(f"Kruskal-Wallis H-statistic: {h_statistic:.4f}")
    print(f"P-value: {p_value:.4f}")

    alpha = 0.05
    print(f"\nSignificance level (alpha): {alpha}")

    if p_value < alpha:
        print("Since the p-value is less than the significance level, we reject the null hypothesis (H0).")
        print("Conclusion: There is a statistically significant difference in the median subscription duration between at least two regions.")
    else:
        print("Since the p-value is greater than the significance level, we fail to reject the null hypothesis (H0).")
        print("Conclusion: There is no statistically significant difference in the median subscription duration between the regions.")
else:
    print("Not enough regions with data to perform the Kruskal-Wallis H-test (at least 2 groups are required).")

