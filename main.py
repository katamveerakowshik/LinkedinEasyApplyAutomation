from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from application_filler import fill_application_fields
# import ollama
from fractions import Fraction
from passw import passwrd
import time


#Disabling webrtc and log warnings and info in the console
chrome_options = Options()
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--log-level=3")

#Using Chrome from the webdriver
driver = webdriver.Chrome( options = chrome_options)


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

def check_preferences(pref):
    data = []
    for element in pref:
        text = element.text.strip()
        if text:
            data.append(text)
    # print(data)

    preferences = []
    for item in data:
        if "Full-time" in item:
            preferences.append("Full-time")
        elif "skills match" in item:
            skills_match = item.split("skills match")[0].strip()  # Get "2 of 7"
            fraction = skills_match.replace(" of ", "/").strip()  # Convert to "2/7"
            preferences.append(fraction)
    print(preferences)
    if len(preferences) == 2:
        preferences[1] = Fraction(preferences[1])
    if preferences[0] == "Full-time" and (len(preferences) == 1 or (len(preferences) > 1 and preferences[1].numerator / preferences[1].denominator >= 0.5)):
        return True
    else:
        return False
    return True

def check_experience(jd):
    # data = []
    # for element in jd:
    #     text = element.text.strip()
    #     if text:
    #         data.append(text)
    # prompt = f"""
    #     Extract the required years of experience from the following job description.
    #     If no experience is mentioned, assume it as 0 years.
    #
    #     Job Description:
    #     {data[0]}
    #
    #     Return only the number of years as an integer.
    #     """
    #
    # response = ollama.run(
    #     model= 'deepseek-r1:1.5b',
    #     prompt = prompt
    # )
    #
    # # Extract and return the response text
    # extracted_experience = response['choices'][0]['message']['content'].strip()
    #
    # print(response)
    # print(extracted_experience)
    # if extracted_experience <= 1:
    #     return True
    # else:
    #     return False
    return True

def main():
    driver.get("https://www.linkedin.com/login")

    # Login
    driver.find_element(By.ID, "username").send_keys("veerakowshikkatam@gmail.com")
    driver.find_element(By.ID, "password").send_keys(passwrd)
    remember_me_checkbox = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
    is_checked = driver.execute_script("return arguments[0].checked;", remember_me_checkbox)
    if is_checked:
        driver.execute_script("arguments[0].checked = false;", remember_me_checkbox)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Navigate to job search page
    driver.get("https://www.linkedin.com/jobs/search/?keywords=machine%20learning%engineer&f_E=2&f_TPR=r86400&f_AL=true")

    while True:
        try:
            # Wait for job cards to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
            )
            job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")

            for job_card in job_cards:
                try:
                    # Click on each job card
                    driver.execute_script("arguments[0].scrollIntoView();", job_card)
                    job_card.click()
                    time.sleep(2)

                    # Extract company name and job details
                    company_name = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name").text
                    print(f"Processing job at {company_name}")
                    pref = driver.find_elements(By.CLASS_NAME, "job-details-preferences-and-skills__pill")
                    jd = driver.find_elements(By.CLASS_NAME, "jobs-description__content")

                    # Check preferences and experience (implement your own logic)
                    if check_preferences(pref) and check_experience(jd):
                        try:
                            easy_apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button")
                            easy_apply_button.click()
                            time.sleep(2)
                            fill_application_fields(driver)
                        except Exception as e:
                            print(f"No Easy Apply button found for {company_name}: {e}")
                            pass
                except Exception as e:
                    print(f"Error processing job card: {e}")
        except Exception as e:
            print(f"Error loading job cards: {e}")
        finally:
            time.sleep(10)
            driver.quit()


if __name__ == "__main__":
    main()