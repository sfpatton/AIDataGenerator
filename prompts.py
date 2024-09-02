# prompts.py
# You are an AI agent that analyzes the CSV provided by the user.
ANALYZER_SYSTEM_PROMPT = """
The focus of your analysis should be on what the data is, how it is formatted, what each column stands for, and how new data should be structured.
"""

# You are an AI agent that generates new CSV rows based on analysis results and sample data.
GENERATOR_SYSTEM_PROMPT = """
Follow the exact formatting and don't output any extra text. You only output formatted data, never any other text.
"""

ANALYZER_USER_PROMPT = """
Analyze the structure and patterns of this sample dataset:
{sample_data}
"""

GENERATOR_USER_PROMPT = """
Provide a concise summary of the following:

1. Formatting of the dataset, be crystal clear when describing the structure of the CSV.
2. What the dataset represents, what each column stands for.
3. How new data should look like, based on the patterns you've identified.

Analysis:
{analysis_result}
Sample Data:
{sample_data}
Generate {num_rows} new CSVd on this analysis and sample data:
Use the exact same formatting as the original data. Output only the generated rows, no extra text.
DO NOT INCLUDE ANY TEXT BEFORE/AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXT!
"""
