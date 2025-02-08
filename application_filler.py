from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from main import driver

predefined_answers = {
    'email': 'veerakowshikkatam@gmail.com',
    'First Name': "Katam",
    "Last Name": "Veera Kowshik",
    'Mobile Number': '9390367226'
}


# chrome_options = Options()
# chrome_options.add_argument("--disable-webrtc")
# chrome_options.add_argument("--log-level=3")
#
# driver = webdriver.Chrome( options = chrome_options)

def fill_application_fields(driver):
    """
    Check if application fields are already filled. If not, prompt for manual input.
    Navigate through all pages by clicking Next until reaching Review, then Submit.
    """
    try:
        while True:  # Loop to handle multiple pages
            # Locate all input fields on the current page
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for input_field in inputs:
                # Check if the field already has a value
                existing_value = input_field.get_attribute("value")
                if existing_value:  # If a value exists, skip filling this field
                    print(f"Field '{input_field.get_attribute('name')}' is already filled with: {existing_value}")
                else:
                    # Prompt user for input if the field is empty
                    field_name = input_field.get_attribute("name")
                    answer = input(f"Field '{field_name}' is empty. Please enter a value: ")
                    input_field.send_keys(answer)

            # Try to click on the "Next" button
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
                next_button.click()
                print("Clicked on Next button.")
                time.sleep(2)  # Wait for the next page to load
            except Exception:
                print("No Next button found. Moving to Review and Submit.")
                break  # Exit loop if no "Next" button is found

        # Click on Review button
        review_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Review')]")
        review_button.click()
        print("Clicked on Review button.")
        time.sleep(2)  # Wait for the Review page to load

        # Click on Submit button
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        print("Clicked on Submit button.")

    except Exception as e:
        print(f"Error processing application fields: {e}")

