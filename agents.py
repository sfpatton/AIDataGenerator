# agents.py

# Import required libraries
import os  # For operating system related operations
import csv  # For reading and writing CSV files
import logging  # For logging messages and errors
import anthropic  # For interacting with the Anthropic API
from typing import Optional, List, Union, Callable  # For type hinting
from prompts import *  # Import all variables and functions from prompts.py
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables from .env file
load_dotenv()

# Set up logging to track events and errors
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
logger = logging.getLogger(__name__)  # Create a logger instance for this module

# Set up the Anthropic API key
try:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")
    logger.info("ANTHROPIC_API_KEY successfully loaded from .env file.")
except ValueError as ve:
    logger.error(f"Error: {str(ve)}")
    print(f"Error: {str(ve)}")
    exit(1)
except Exception as e:
    logger.error(f"Unexpected error while loading ANTHROPIC_API_KEY: {str(e)}")
    print(f"Unexpected error while loading ANTHROPIC_API_KEY: {str(e)}")
    exit(1)

def read_csv_file(file_path: str) -> Optional[List[List[str]]]:
    """
    Read a CSV file and return its contents as a list of lists.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[List[List[str]]]: A list of lists containing the CSV data, or None if an error occurs.
    """
    try:
        with open(file_path, newline='') as csvfile:  # Open the CSV file
            csv_reader = csv.reader(csvfile)  # Create a CSV reader object
            return list(csv_reader)  # Convert the CSV reader to a list of lists
    except FileNotFoundError:
        logger.error(f"Error: The file {file_path} was not found.")  # Log error if file is not found
    except PermissionError:
        logger.error(f"Error: You don't have permission to read the file {file_path}.")  # Log error if permission is denied
    except csv.Error as e:
        logger.error(f"Error reading CSV file: {e}")  # Log any other CSV-related errors
    return None  # Return None if any error occurs

def save_to_csv(data: str, output_file: str, headers: Optional[List[str]] = None):
    """
    Save data to a CSV file.

    Args:
    data (str): The data to be saved as a string.
    output_file (str): The path to the output CSV file.
    headers (Optional[List[str]]): Optional headers for the CSV file.
    """
    if not data:
        logger.error("Error: No data to save. Skipping CSV write operation.")
        return

    mode = 'w' if headers and not os.path.exists(output_file) else 'a'  # 'w' for write mode if headers are provided and file doesn't exist, 'a' for append mode otherwise
    try:
        with open(output_file, mode, newline='') as f:
            writer = csv.writer(f)  # Create a CSV writer object
            if headers and mode == 'w':
                writer.writerow(headers)  # Write headers if provided and in write mode
            for row in csv.reader(data.splitlines()):  # Use csv.reader to parse the data string
                writer.writerow(row)
    except PermissionError:
        logger.error(f"Error: You don't have permission to write to the file {output_file}.")
    except IOError as e:
        logger.error(f"Error writing to CSV file: {e}")

def get_user_input(prompt: str, default: Union[int, float],
                   validator: Callable[[Union[int, float]], bool]) -> Union[int, float]:
    """
    Get user input with validation and default value.

    Args:
    prompt (str): The prompt to display to the user.
    default (Union[int, float]): The default value if no input is provided.
    validator (Callable[[Union[int, float]], bool]): A function to validate the input.

    Returns:
    Union[int, float]: The validated user input or default value.
    """
    while True:
        try:
            value = input(f"{prompt} (default is {default}): ") or default  # Get user input or use default
            value = type(default)(value)  # Convert input to the same type as the default value
            if validator(value):  # Validate the input
                return value
            raise ValueError  # Raise ValueError if validation fails
        except ValueError:
            logger.error(f"Error: Please enter a valid {type(default).__name__}.")  # Log error for invalid input

def get_model_choice() -> str:
    """
    Prompt the user to choose an AI model.

    Returns:
    str: The chosen model name.
    """
    models = {
        "1": "claude-3-opus-20240229",
        "2": "claude-3-sonnet-20240229",
        "3": "claude-3-haiku-20240307",
        "4": "claude-3-5-sonnet-20240620"
    }
    print("Please select a model:")
    for key, value in models.items():
        print(f"{key}. {value}")
    choice = input("Enter the number of your choice: ")
    return models.get(choice, "claude-3-haiku-20240307")  # Return chosen model or default to claude-3-haiku-20240307

def make_api_call(client: anthropic.Anthropic, model: str, max_tokens: int, temperature: float,
                  system_prompt: str, user_prompt: str) -> Optional[str]:
    """
    Make an API call to the Anthropic service.

    Args:
    client (anthropic.Anthropic): The Anthropic client object.
    model (str): The name of the AI model to use.
    max_tokens (int): The maximum number of tokens for the response.
    temperature (float): The temperature parameter for text generation.
    system_prompt (str): The system prompt to set the context.
    user_prompt (str): The user's input prompt.

    Returns:
    Optional[str]: The generated content from the API, or None if an error occurs.
    """
    try:
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text  # Return the correctly formatted text
    except anthropic.APIError as e:
        logger.error(f"API Error: {str(e)}")  # Log API-specific errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")  # Log any other unexpected errors
    return None  # Return None if any error occurs

def analyzer_agent(sample_data: str, model: str, max_tokens: int, temperature: float) -> Optional[str]:
    """
    Run the analyzer agent to analyze the sample data.

    Args:
    sample_data (str): The sample data to be analyzed.
    model (str): The name of the AI model to use.
    max_tokens (int): The maximum number of tokens for the response.
    temperature (float): The temperature parameter for text generation.

    Returns:
    Optional[str]: The analysis result, or None if an error occurs.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)  # Create an Anthropic client

    return make_api_call(client, model, max_tokens, temperature,
                         ANALYZER_SYSTEM_PROMPT,
                         ANALYZER_USER_PROMPT.format(sample_data=sample_data))  # Make API call and return result

def generator_agent(analysis_result: str, sample_data: str, num_rows: int, model: str, max_tokens: int, temperature: float) -> Optional[str]:
    """
    Run the generator agent to generate new data based on the analysis and sample data.

    Args:
    analysis_result (str): The result from the analyzer agent.
    sample_data (str): The original sample data.
    num_rows (int): The number of rows to generate.
    model (str): The name of the AI model to use.
    max_tokens (int): The maximum number of tokens for the response.
    temperature (float): The temperature parameter for text generation.

    Returns:
    Optional[str]: The generated data, or None if an error occurs.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)  # Create an Anthropic client

    return make_api_call(client, model, max_tokens, temperature,
                         GENERATOR_SYSTEM_PROMPT,
                         GENERATOR_USER_PROMPT.format(analysis_result=analysis_result, sample_data=sample_data, num_rows=num_rows))  # Make API call and return result

# Main execution flow
while True:
    file_path = input("\nEnter the name of your CSV file (or 'q' to quit): ")  # Get input CSV file name from user
    if file_path.lower() == 'q':
        print("Quitting the application...")
        exit(0)
    if file_path:
        file_path = os.path.join('/app/data', file_path)  # Construct full file path
        break
    else:
        print("Error: You must enter a CSV file name. Please try again.")

try:
    desired_rows = int(input("Enter the number of rows you want in the new dataset: "))  # Get desired number of rows from user
except ValueError:
    logger.warning("Error: Invalid input for number of rows. Using default value of 30.")  # Log warning for invalid input
    desired_rows = 30  # Set default value if input is invalid

model = get_model_choice()  # Get user's choice of model
max_tokens = int(get_user_input("Enter the maximum number of tokens", 1500, lambda x: x > 0))  # Get max tokens from user
temperature = get_user_input("Enter the temperature (between 0 and 1)", 0.7, lambda x: 0 <= x <= 1)  # Get temperature from user

sample_data = read_csv_file(file_path)  # Read the input CSV file
if sample_data is None:
    logger.error("Error: Failed to read the input CSV file. Exiting.")  # Log error if file reading fails
    exit(1)  # Exit the program with an error code

sample_data_str = "\n".join([",".join(row) for row in sample_data])  # Convert sample data to string format
logger.info("\nLaunching team of Agents...")  # Log info about launching agents

analysis_result = analyzer_agent(sample_data_str, model, 400, 0.1)  # Run the analyzer agent with default values
if analysis_result is None:
    logger.error("Error: Analyzer Agent failed to produce output. Exiting.")  # Log error if analyzer fails
    exit(1)  # Exit the program with an error code

logger.info("#### Analyzer Agent output: ####\n")  # Log analyzer output header
logger.info(analysis_result)  # Log the analysis result
logger.info("\n-----------------------------------\nGenerating new data...")  # Log separator and info about data generation

# Set up the output file
output_file = os.path.join('/app/data', 'new_dataset.csv')  # Set the output file path
headers = sample_data[0] if sample_data else None  # Use the first row of sample data as headers, check if sample_data is not empty
if not os.path.exists(output_file):
    save_to_csv(",".join(headers) if headers else "", output_file, headers)  # Create the output file with headers if it doesn't exist

batch_size = 30  # Set batch size for generating data
generated_rows = 0  # Counter to keep track of how many rows have been generated

# Generate data in batches until we reach the desired number of rows
while generated_rows < desired_rows:
    rows_to_generate = min(batch_size, desired_rows - generated_rows)  # Calculate rows to generate in this batch
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate, model, max_tokens, temperature)  # Generate data

    if generated_data is None:
        logger.warning("Error: Failed to generate data in this batch. Retrying...")  # Log warning if batch generation fails
        continue  # Retry generation

    logger.info("\nVerifying newly generated data:")  # Log info about verifying new data
    logger.info(generated_data)  # Log the newly generated data

    # Remove any header rows from the generated data
    generated_data_lines = generated_data.splitlines()
    if headers and generated_data_lines and generated_data_lines[0] == ",".join(headers):
        generated_data_lines = generated_data_lines[1:]
    generated_data = "\n".join(generated_data_lines)

    save_to_csv(generated_data, output_file)  # Save the new batch of data
    generated_rows += len(generated_data_lines)  # Update generated row count
    logger.info(f"Generated {generated_rows} rows out of {desired_rows}")  # Log progress

logger.info(f"\nGenerated data has been saved to {output_file}")  # Log final success message
