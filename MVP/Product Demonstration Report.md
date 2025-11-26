## Product Demonstration Report

### 1. Weekly Calorie Trend Chart

https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/blob/master/MVP/weekly_calorie_trend.png?ref_type=heads

This chart displays the user’s calorie intake across a seven-day period.  
For the MVP stage, the graph uses sample calorie values to demonstrate how the trend analysis feature will function.  
In the final implementation, this chart will be updated dynamically using real meal data entered by the user.  
Users will also have the option to switch between daily, weekly, and monthly views.

---

### 2. How the Graph Was Generated

https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/blob/master/MVP/python_code_-_weekly_calorie_trend.png?ref_type=heads

The screenshot above displays the Python script used to generate the weekly calorie trend chart.  
This demonstrates the backend process used to create visualisations for nutrient intake.  
The script uses the `matplotlib` library to create a line chart and save it as a PNG file.

Below is the code included for clarity:

```python
import matplotlib.pyplot as plt

# Sample data for nutrient trend (calories per day)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
calories = [1400, 1500, 1600, 1550, 1700, 1650, 1580]

# Create the chart
plt.figure(figsize=(8, 4))
plt.plot(days, calories, marker='o')

# Add titles and labels
plt.title("Weekly Calorie Trend")
plt.xlabel("Day")
plt.ylabel("Calories")

# Add a grid for readability
plt.grid(True)

# Fit layout
plt.tight_layout()

# Save the chart
plt.savefig("python_calories_line_chart.png")

# Close the figure
plt.close()
