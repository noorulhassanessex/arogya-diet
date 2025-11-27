# Product Management Log
 
## Project management discussion
Overall, the team has worked exceptionally well together over the course of this project. Generally, communications have consistently been clear allowing everyone to remain focused on their assigned tasks. The team utilised our WhatsApp group chat and Tuleap to share updates and raise any concerns. This allowed the team to remain organised and ensure that any problems that arose were addressed and sorted out effectively. During busy periods our structured approach helped the team remain focused and organised so that we can cohesively work as a team to create a successful project. Furthermore, any team member was also able to get help from fellow team members when needed. Weekly scrum meetings were a crucial part of keeping the project on the right track. However, not everyone regularly attended these meetings which caused them to struggle with the project.  The meetings were useful as it allowed us to review earlier sprints, to review our progress and plan our next steps. Overtime our meetings became more efficient due to our regular progress updates and closely followed scrum structure. This improved our discussions as it allowed us to remain focused and entailed that everyone was aware of their responsibilities. 

At times, responses to messages were slow, or team members completed tasks without clearly communicating which items they had taken on. This occasionally left others unsure about whether certain tasks were being worked on or if they still needed attention. Additionally, some members of the team found their workload to be high due to a lack of contribution from other team members. Although this didn’t stop us from reaching our goals this is an area we recognise still needs improvement, and we aim to address it in future projects.  We did not record our stand-up meetings in Tuleap. Instead, the team held quick stand-ups verbally at the start of each lab session and used our group chat to share daily progress and blockers. This method worked effectively for us because everyone was already present during the lab time, and using the WhatsApp chat allowed team members to update each other when working outside scheduled hours. Although Tuleap provides a useful place to store stand-up logs, our team found that using the WhatsApp for short updates was faster and more practical. For future sprints, we could improve traceability by recording brief stand-up summaries in Tuleap so that progress and blockers are documented more formally.


## Sprint Burndown Charts

1. Sprint 1

![image_alt](https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/raw/master/MVP/Burndown_Chart_sprint_1.png)

2. Sprint 2 

![image_alt](https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/raw/master/MVP/Burndown_Chart_sprint_2.png?ref_type=heads)

3. Sprint 3

![image_alt](https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/raw/master/MVP/Burndown_Chart_sprint_3.png)
## Burndown-Charts Discussion

Across all the three sprints, although the team has put amazing efforts together and completed the planned task, but the progress recorded was not consistent in the Tuleap making it a bit difficut to get the track of the momentum throughout each of the sprints. Ideally, improving in making updates to the remaining efforts on a regular basis, will give a clear picture of the mid-sprint progress and track the team's efforts of being behind or ahead. So, from all of the future sprints, the team can do much more better by using retrospective insights, ensuring perfect and proper task distribution among each one of us, use planning poker to get align to the complexity and the capability can better help each one in the group to maintain in their steady progress. By working in these areas, the team can amend transparency, minimize the workflow obstacles, it would raise more reliability towards the future sprints, and boost more visbility helping us continue building a successful track record of all of our sprint goals.

## **Product Backlog**

These are some of the unique features that's going to be present there in our final product

![image_alt](https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/raw/master/MVP/BackLog_1.png)



![image_alt](https://cseegit.essex.ac.uk/25-26-ce201-col/25-26_CE201-col_team05/-/raw/master/MVP/BackLog_2.png?ref_type=heads)

## Other areas 
### 1. Weekly Calorie Trend Chart
![Weekly Calorie Trend]( weekly_calorie_trend.png)

This chart demonstrates the user’s calorie intake across a seven-day period.  
At the MVP stage, the chart uses sample data to demonstrate functionality.  
In the final version of the product, this graph will update automatically based on the meals logged by the user.  
We also plan to extend the date range options so that users can view daily, weekly, or monthly trends.

---

### 2. How the Graph Was Generated
![Python Graph Code](python_code_-_weekly_calorie_trend.png)

The image above shows the Python script used to generate the weekly calorie trend chart.  
The script uses the `matplotlib` library to plot daily calorie values and save the chart as a PNG file.

Below is the exact code used for generating the graph:

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

# Adjust layout
plt.tight_layout()

# Save the chart
plt.savefig("python_line_chart.png")

# Close the figure
plt.close()
