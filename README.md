# AIDataGenerator
An AI-powered tool that analyzes CSV datasets and generates new synthetic data rows based on the original structure and patterns. Utilizes Anthropic's Claude AI models for data analysis and generation.

# AIDataGenerator

AIDataGenerator is a powerful tool that leverages AI to analyze CSV datasets and generate new synthetic data rows that match the original data's structure and patterns. This project uses Anthropic's Claude AI models to perform intelligent data analysis and generation.

## Features
- Analyzes input CSV files to understand data structure and patterns
- Generates new data rows based on the analysis
- Supports multiple Claude AI models
- Customizable output size and AI parameters
- Docker-ready for easy deployment

## Prerequisites
- Docker
- Anthropic API key

## Quick Start
1. Clone this repository.
2. Create a `.env` file in the project root and add your Anthropic API key.
3. Build the Docker image:
   
   docker build -t aidatagenerator .

4. Run the container:
   
   docker run -it --rm -v /path/to/your/data:/app/data aidatagenerator

Follow the prompts to analyze your CSV file and generate new data.
The tool will guide you through the process of:

Selecting an input CSV file
Choosing an AI model
Setting parameters like max tokens and temperature
Analyzing the data
Generating new rows
Output will be saved to /app/data/new_dataset.csv inside the container.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
