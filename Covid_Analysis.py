import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

filename = "covid-data.csv"
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
source = requests.get(url).text
covid_data = StringIO(source)

covid_df2 = pd.read_csv(covid_data)
value_list = ["Asia", "Europe", "South America", "North America", "European Union"]
countries_exclude = ~covid_df2["location"].isin(value_list)
covid_df = covid_df2[countries_exclude]

group1 = covid_df["new_cases"].groupby(covid_df["continent"])

total_cases = covid_df.groupby("location")["new_cases"].sum()
total_cases = total_cases.sort_values(ascending=False)

most_affected_countries = total_cases[1:11].index
cases = total_cases[1:11].values

total_deaths = covid_df.groupby("location")["new_deaths"].sum()
deaths = total_deaths[most_affected_countries].values

cases_deaths_df = pd.DataFrame(
    {"Country": most_affected_countries, "Total Cases": cases, "Total Deaths": deaths}
)

print(cases_deaths_df)

plot_data = pd.melt(
    cases_deaths_df,
    id_vars=["Country"],
    value_vars=["Total Cases", "Total Deaths"],
    var_name="Metric",
    value_name="Case Count",
)

plt.figure(figsize=(12, 5))
sns.barplot(x="Country", hue="Metric", y="Case Count", data=plot_data)
plt.title("Most Affected Countries (Top 10)")
plt.show

total_tests = covid_df.groupby("location")["new_tests"].sum().values
population = covid_df.groupby("location")["population"].nth(-1)
testing_rate = (total_tests / population).sort_values(ascending=False)[:10]

plt.figure(figsize=(10, 5))

sns.set_color_codes("deep")
sns.barplot(y=testing_rate.index, x=testing_rate.values, orient="h", color="m")

plt.title("Testing Rate (Top 10 Countries)")
plt.xlabel("Total Tests / Total Population")
plt.ylabel("Country")
plt.show()

country1 = "United States"
country1_data = covid_df.loc[covid_df["location"] == country1]

country1_cases = country1_data[["date", "total_cases"]]

country2 = "Canada"
country2_data = covid_df.loc[covid_df["location"] == country2]
country2_cases = country2_data[["date", "total_cases"]]

datewise_cases = country1_cases.merge(country2_cases, how="inner", on="date")
print(datewise_cases.tail())

plt.figure(figsize=(12, 7))
plt.plot(
    datewise_cases["date"].values,
    datewise_cases["total_cases_x"].values,
    color="blue",
    label=country1,
)
plt.plot(
    datewise_cases["date"].values,
    datewise_cases["total_cases_y"].values,
    color="red",
    label=country2,
)

plt.xticks(
    [
        datewise_cases["date"][i] if i % 30 == 0 else ""
        for i in range(len(datewise_cases.index))
    ],
    rotation=45,
)
plt.xlabel("Date")
plt.ylabel("Total Number of Cases")
plt.title("Rate of Total Coronavirus Cases")
plt.legend()
plt.show()

df_corr = pd.DataFrame(most_affected_countries.values, columns=["Country"])
df_corr["Total_cases"] = cases

df_corr.head()
