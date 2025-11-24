## User Stories

### User Story 1: Dietary Goals
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9330  
![2025-11-24__11_](/uploads/ca6a85de9333e64ce55d6072a2eb8f3e/2025-11-24__11_.png){width=731 height=387}

**Story Summary (from Tuleap):**  
As a user, I want to set dietary goals so that the system can observe my progress and alert me if I am exceeding my limits.

**Story Description (from Tuleap):**  
The user will be able to define goals for calories, sugars or any other nutrients. These goals will then be saved into the database. If trends exceed their target limit, the system will display a warning. Set goals will appear in the UI and within the PDF report.

**Assigned to:** Person 4  
**Status:** Not started


---

### User Story 2: Developing a Backend Service to Save Meals
**Tuleap URL:**  https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9331
![2025-11-24__12_](/uploads/8256b8f0cc7d14e0d62877bc3c1c93ce/2025-11-24__12_.png){width=728 height=404}

**Story Summary (from Tuleap):**  
As a system, I require a backend API endpoint that will store meals alongside information such as date, meal type and items. This allows frontend meal entries to be saved dependably.

**Story Description (from Tuleap):**  
The system should accept fields for date, meal type and items. The system will validate incoming data and save meals alongside their related items within the database. The system will calculate totals of calories, proteins, carbohydrates, fats and sugars. If validation fails, then the system will return an error message.

**Acceptance Criteria:**  
- The POST endpoint must accept JSON input in the required structure.  
- Missing or invalid fields must return an appropriate error message.  
- Valid data must save the meal and any associated items into the database.

**Assigned to:** Person 1  
**Status:** Not started


---

### User Story 3: Charts and Visualisation
**Tuleap URL:**  https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9332
![2025-11-24__13_](/uploads/b860f31d5092a2cee16b67bee0898947/2025-11-24__13_.png){width=734 height=383}

**Story Summary:**  
As a user, I want to see charts showing calories and nutrients over time so that I can spot trends in my diet and analyse any changes.

**Story Description:**  
The user will be able to select a date range such as daily, weekly or monthly. The system will then display charts for calories, carbs, sugars and fats. These charts will be shown in the UI dashboard and the PDF report.

**Acceptance Criteria:**  
- The user can choose a date range.  
- All charts must show accurate information.  
- Trends should be visible and understandable.  
- Data points must match backend totals.

**Assigned to:** Person 4  
**Status:** In progress


---

### User Story 4: Generating the PDF
**Tuleap URL:**  https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9333
![2025-11-24__14_](/uploads/1724fd2f46aeb94922a880d52eefb5fc/2025-11-24__14_.png){width=735 height=389}

**Story Summary:**  
As a user, I want to be able to generate a PDF report of my diet so that I can show it to a dietician.

**Story Description:**  
The system will assemble any logged data into a clear and concise PDF report. The PDF will include charts, daily totals and summary statistics. The layout must be clean, readable and well formatted. Person 5 will ensure spacing and readability are correct.

**Acceptance Criteria:**  
- The user can choose a meal type: breakfast, lunch, dinner or snacks.  
- The user can select food from a database and specify quantity.  
- The system will calculate calories automatically.  
- Meals will appear in the daily log.

**Assigned to:** Person 5  
**Status:** In progress


---

### User Story 5: Adding Meal Quantities and Food Items
**Tuleap URL:**  https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9334
![2025-11-24__15_](/uploads/17f458da7eaeb149525b454b860037db/2025-11-24__15_.png){width=733 height=404}

**Story Summary:**  
As a user, I want to add food items and quantities to meals so that the system can calculate nutrition and calorie totals.

**Story Description:**  
After creating a meal entry, the user can add individual food items. A searchable list of foods and quantity options will be provided. Once added, the system will calculate calories, proteins, fats, carbs and sugars based on database values.

**Acceptance Criteria:**  
- Users can search for food items and select quantity (servings or grams).  
- Nutrients and calories must be calculated for each item.  
- Meal totals update continuously.  
- Users can remove items.  
- All items must be saved within the database.

**Assigned to:** Person 2  
**Status:** In progress


---

### User Story 6: Selecting Meal Type and Adding Meal Entry
**Tuleap URL:**  https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9335
![2025-11-24__17_](/uploads/e62085baf50bcb97ef290e16c50d52ab/2025-11-24__17_.png){width=732 height=404}

**Story Summary:**  
As a user, I want to choose a meal type (breakfast, lunch, dinner, snacks) so that I can manage my daily food consumption.

**Story Description:**  
The user begins by selecting a meal type. Selecting one creates an empty meal entry for that category. No food items are added at this stage.

**Acceptance Criteria:**  
- The user can choose breakfast, lunch, dinner or snacks.  
- A new empty meal entry is created and timestamped.  
- Entries appear in the daily log even if empty.  
- Food items are not added at this stage.

**Assigned to:** Person 3  
**Status:** In progress


---

## Functional and Non-functional Requirements

### Functional Requirements
- The system should permit the user to select a meal type.  
- The system will allow the user to insert food quantities and items.  
- The system will calculate calories, proteins, fats, carbs and sugars.  
- Meals and items must be stored within the database.  
- The system will display dietary trends using charts and graphs.  
- The system will permit the user to set dietary goals.  
- If the user exceeds their goals, the system will warn them.

### Non-functional Requirements
- Daily briefs should load within 2 seconds.  
- The user interface must be intuitive for non-technical users.  
- Once data is saved, it must not be lost.  
- The system will validate user input.  
- User data must be secure and inaccessible by other users.  
- The system must be compatible with modern browsers (Chrome, Edge).  
- Unsafe dietary goals must trigger warnings.


---

## Risk Assessment

### Risk 1 – Underestimating the Duration of Tasks
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9353
![2025-11-24__20_](/uploads/2f485df4b0c88ba2368a7b741896a44e/2025-11-24__20_.png){width=737 height=512}

**Summary:**  
The tasks may take longer than initially anticipated, which could cause delays in sprints.

**Description:**  
Tasks that involve integration of both frontend and backend may require more time than expected. This can lead to incomplete sprint work and reduce the team’s overall pace.

**Impact:** High  
**Likelihood:** High  
**Assigned to:** Person 1  
**Status:** In progress

**Mitigation Actions:**  
- Tasks can be broken down into smaller, more manageable items.  
- During sprint planning, the team may need to re-estimate timeframes.  
- The velocity of each sprint can be reviewed and adjusted accordingly.  
- Burndown charts can be monitored weekly.  
- Person 1 must ensure workload allocation is fair and realistic.

**Mitigation Owner:** Person 1


---

### Risk 2 – Merge Conflicts Between Developers
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9359
![2025-11-24__21_](/uploads/e22a31803b6a06940a52c095de237616/2025-11-24__21_.png){width=723 height=475}

**Summary:**  
If multiple developers work on the same files, merge conflicts may arise.

**Description:**  
All team members will be working simultaneously on UI, backend and documentation, which increases the chance of merge conflicts.

**Impact:** Medium  
**Likelihood:** Medium  
**Assigned to:** Person 5  
**Status:** In progress

**Mitigation Actions:**  
- Merge consistency should be reviewed by Person 5.  
- A feature-branch workflow should be implemented.  
- Encourage frequent commits and regular repository updates.  
- Ensure all commit messages are descriptive and clear.

**Mitigation Owner:** Person 5


---

### Risk 3 – Incorrect Nutrient Calculations
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9363 
![2025-11-24__22_](/uploads/bf7457d81e6f42d8c2acd100c12d93f7/2025-11-24__22_.png){width=726 height=474}

**Summary:**  
The system may incorrectly calculate calorie and nutrient totals.

**Description:**  
If there is a flaw in calculations or database values, summaries, charts and reports will be inaccurate. This could lead to users distrusting the tool.

**Impact:** High  
**Likelihood:** Low  
**Assigned to:** Person 2  
**Status:** Not started

**Mitigation Actions:**  
- Automated tests will be implemented by Person 5.  
- Person 2 will review the accuracy of all data.  
- Values can be cross-checked using at least two databases.

**Mitigation Owner:** Person 2 and Person 5


---

### Risk 4 – Misinterpreting Client Expectations
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9369 
**Screenshot:** ![2025-11-24__26_](/uploads/4bd8be4dd6ed0a7ea718d408d010e5a9/2025-11-24__26_.png){width=727 height=466}

**Summary:**  
There is a risk that the development team may misinterpret what the client expects.

**Description:**  
The project contains multiple features such as charts, PDFs and goals. Some expectations may be unclear, leading to misunderstandings.

**Impact:** High  
**Likelihood:** Medium  
**Assigned to:** Person 1  
**Status:** In progress

**Mitigation Actions:**  
- Clarify any unclear requirements immediately.  
- Document all decisions on Tuleap.  
- Hold weekly discussions with a supervisor.

**Mitigation Owner:** Person 1


---

### Risk 5 – Absences and Low Participation of Team Members
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9371 
**Screenshot:** ![2025-11-24__27_](/uploads/1222f095721d33b5aa4b4133763651bf/2025-11-24__27_.png){width=731 height=486}

**Summary:**  
Team members may not contribute enough or may frequently miss lab sessions.

**Description:**  
Low participation or repeated absences can negatively impact task delivery and the project’s overall progress.

**Impact:** High  
**Likelihood:** Low  
**Assigned to:** Person 1  
**Status:** In progress

**Mitigation Actions:**  
- Absences should be communicated clearly and early.  
- Tasks can be reassigned when necessary.

**Mitigation Owner:** Person 1


---

### Risk 6 – Unintuitive User Interface
**Tuleap URL:** https://csee-tuleap.essex.ac.uk/plugins/tracker/?aid=9373
**Screenshot:** ![2025-11-24__29_](/uploads/f7f68ec276d62c0b3ecb95dc876af8fc/2025-11-24__29_.png){width=731 height=464}

**Summary:**  
The user interface may be confusing or difficult for clients to use.

**Description:**  
A poorly designed UI can cause users to struggle with logging meals or interpreting charts, reducing the overall usefulness of the product.

**Impact:** High  
**Likelihood:** Medium  
**Assigned to:** Person 3 and Person 4  
**Status:** In progress

**Mitigation Actions:**  
- Conduct basic user testing.  
- Gather user feedback.  
- Ensure forms and charts are simple and easy to read.

**Mitigation Owner:** Person 3 and Person 4