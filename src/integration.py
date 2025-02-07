import os
import json
import logging
import requests
from pydantic import BaseModel, EmailStr, ValidationError

# Configure logging for production-grade observability
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define a Pydantic model for user data
class User(BaseModel):
    name: str
    email: EmailStr
    user_id: int

def load_users(file_path: str):
    """
    Load and validate users from a JSON file.
    Each user is validated using Pydantic.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {e}")
        return []

    users = []
    for user_data in data:
        try:
            user = User(**user_data)
            users.append(user)
        except ValidationError as e:
            logging.error(f"Validation error for data {user_data}: {e}")
    return users

def fetch_additional_info(user: User):
    """
    Call an external API to fetch additional info for the user.
    For demonstration purposes, we use a placeholder API.
    """
    api_url = f"https://jsonplaceholder.typicode.com/users/{user.user_id}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP issues
        additional_data = response.json()
        logging.info(f"Fetched additional data for {user.name}")
        return additional_data
    except requests.RequestException as e:
        logging.error(f"Error fetching data for user {user.user_id}: {e}")
        return {}

def merge_user_data(user: User, additional_info: dict):
    """
    Merge the validated user data with additional API data.
    """
    merged_data = user.dict()  # Get the Pydantic model as a dictionary
    merged_data.update(additional_info)
    return merged_data

def main():
    # Load and validate user data from a JSON file
    users = load_users("users.json")
    if not users:
        logging.error("No valid users loaded. Exiting.")
        return

    # Process each user: fetch additional details and print merged results
    for user in users:
        additional_info = fetch_additional_info(user)
        merged_data = merge_user_data(user, additional_info)
        print(merged_data)

if __name__ == "__main__":
    main()
