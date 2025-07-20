import pandas as pd

# Load your Excel file and the specific sheet
file_path = 'G:/NMIT/research project a/CODE/7_Cognitive_Map_Graph_Processing.xlsx'
sheet_name = 'sentences'  # Specify the correct sheet name

# Read the Excel sheet into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract necessary columns (modify these if your Excel columns have different names)
# Assuming 'CMG Auto with GPT' contains data in "Head: <head> Relation: <relation> Tail: <tail>" format
df['CMG Auto with GPT'] = df['CMG Auto with GPT'].dropna()

# Initialize lists to store parsed data
heads = []
relations = []
tails = []

# Regular expression to extract head, relation, and tail from the structured text
import re
pattern = re.compile(r"Head:\s*(.*?)\s*Relation:\s*(.*?)\s*Tail:\s*(.*)")

# Loop through each entry in the 'CMG Auto with GPT' column
for entry in df['CMG Auto with GPT']:
    match = pattern.search(entry)
    if match:
        head, relation, tail = match.groups()
        heads.append(head.strip())
        relations.append(relation.strip())
        tails.append(tail.strip())

# Create a new DataFrame with the extracted columns
data = {
    'Head': heads,
    'Relation': relations,
    'Tail': tails
}
df_output = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_path = 'bipolar_knowledge_graph.csv'
df_output.to_csv(output_path, index=False)

print(f'CSV file saved successfully at {output_path}')
