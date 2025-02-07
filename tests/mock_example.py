import requests
from unittest.mock import patch, MagicMock
import pytest

# The class we are testing
class APIClient:
    def fetch_data_from_api1(self):
        response = requests.get("https://api1.example.com")
        return response.json()

    def fetch_data_from_api2(self):
        response = requests.get("https://api2.example.com")
        return response.json()

    def process_data(self, data):
        # This method processes data
        return {"processed_data": data}

# Independent functions we want to mock
def external_function_1():
    return "Real result from function 1"

def external_function_2():
    return "Real result from function 2"

@pytest.fixture
def api_client():
    return APIClient()

def test_all_mocking(api_client):
    # Patch requests.get to differentiate between the two API calls
    with patch("requests.get") as mock_get, \
         patch.object(APIClient, "process_data", return_value={"processed_data": "mocked_processed_data"}) as mock_process_data, \
         patch("module_name.external_function_1", return_value="mocked_result_from_function_1") as mock_function_1, \
         patch("module_name.external_function_2", return_value="mocked_result_from_function_2") as mock_function_2:

        # Define the mock responses
        mock_response_1 = MagicMock()
        mock_response_1.json.return_value = {"data": "mocked_data_1"}

        mock_response_2 = MagicMock()
        mock_response_2.json.return_value = {"data": "mocked_data_2"}

        # Set up side_effect to return different responses based on URL
        def mock_requests_get(url, *args, **kwargs):
            if url == "https://api1.example.com":
                return mock_response_1
            elif url == "https://api2.example.com":
                return mock_response_2
            else:
                raise ValueError("Unknown URL")

        mock_get.side_effect = mock_requests_get

        # Call the methods to fetch data from the APIs
        result_1 = api_client.fetch_data_from_api1()  # Calls the first API (api1)
        result_2 = api_client.fetch_data_from_api2()  # Calls the second API (api2)

        # Validate the fetched data from both APIs
        assert result_1 == {"data": "mocked_data_1"}
        assert result_2 == {"data": "mocked_data_2"}

        # Ensure `process_data` was called with the correct arguments
        processed_result = api_client.process_data(result_1)
        assert processed_result == {"processed_data": "mocked_processed_data"}

        # Verify the independent functions were called correctly
        assert external_function_1() == "mocked_result_from_function_1"
        assert external_function_2() == "mocked_result_from_function_2"

        # Check if requests.get was called for both APIs
        mock_get.assert_any_call("https://api1.example.com")
        mock_get.assert_any_call("https://api2.example.com")

        # Ensure the functions were called
        mock_function_1.assert_called_once()
        mock_function_2.assert_called_once()
