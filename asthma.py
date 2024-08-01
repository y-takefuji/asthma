import pandas as pd
import matplotlib.pyplot as plt
import re

# Load the data
data = pd.read_csv('data.csv')

# Filter the data
filtered_data = data[(data['LocationAbbr'] == 'US')]

# Save the filtered data to a new CSV file
filtered_data.to_csv('us.csv', index=False)

filtered_data = data[(data['LocationAbbr'] == 'US') & (data['Topic'] == 'Asthma')]

# Show candidates from 'Question' related to asthma
questions = filtered_data['Question'].unique()
print("Select a category from 'Question':")
for i, question in enumerate(questions):
    print(f"{i + 1}. {question}")
question_choice = int(input("Enter the number of your choice: ")) - 1
selected_question = questions[question_choice]

# Show candidates from 'DataValueType' related to asthma
data_value_types = filtered_data['DataValueType'].unique()
print("Select a category from 'DataValueType':")
for i, data_value_type in enumerate(data_value_types):
    print(f"{i + 1}. {data_value_type}")
data_value_type_choice = int(input("Enter the number of your choice: ")) - 1
selected_data_value_type = data_value_types[data_value_type_choice]

# Show candidates from 'StratificationCategory1'
stratification_categories = filtered_data['StratificationCategory1'].unique()
print("Select up to 2 categories from 'StratificationCategory1' (separate numbers with space):")
for i, category in enumerate(stratification_categories):
    print(f"{i + 1}. {category}")
stratification_choices = list(map(int, input("Enter the numbers of your choices: ").split()))
selected_stratifications = [stratification_categories[i - 1] for i in stratification_choices]

# Show candidates from 'Stratification1'
stratifications = filtered_data['Stratification1'].unique()
print("Select up to 4 candidates from 'Stratification1' (separate numbers with space):")
for i, stratification in enumerate(stratifications):
    print(f"{i + 1}. {stratification}")
stratification1_choices = list(map(int, input("Enter the numbers of your choices: ").split()))
selected_stratification1 = [stratifications[i - 1] for i in stratification1_choices]

# Filter the data based on the selected categories
final_data = filtered_data[(filtered_data['Question'] == selected_question) &
                           (filtered_data['DataValueType'] == selected_data_value_type) &
                           (filtered_data['StratificationCategory1'].isin(selected_stratifications)) &
                           (filtered_data['Stratification1'].isin(selected_stratification1))]

# Ensure 'DataValue' is numeric
final_data['DataValue'] = pd.to_numeric(final_data['DataValue'], errors='coerce')

# Plot the graph
plt.figure(figsize=(10, 6))
line_styles = ['-', '--', '-.', ':']
widths = [1, 2]
for i, stratification in enumerate(selected_stratification1):
    strat_data = final_data[final_data['Stratification1'] == stratification]
    plt.hlines(y=strat_data['DataValue'], xmin=strat_data['YearStart'], xmax=strat_data['YearStart'] + 1,
               colors='black', linestyles=line_styles[i % len(line_styles)], linewidth=widths[i % len(widths)],
               label=stratification)

plt.xlabel('Year')
plt.ylabel(selected_question)
plt.title('Asthma Prevalence Trends in the US')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()

# Replace invalid characters in the file name
file_name = re.sub(r'[\\/*?:"<>|]', "", selected_question) + ".png"

# Save the plot as a PNG file
plt.savefig(file_name,dpi=300)

plt.show()

