from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def check_preferences(pref):
    # data = []
    # for element in pref:
    #     text = element.text.strip()
    #     if text:
    #         data.append(text)
    # print(data)
    #
    # preferences = []
    # for item in data:
    #     if "Full-time" in item:
    #         preferences.append("Full-time")
    #     elif "skills match" in item:
    #         skills_match = item.split("skills match")[0].strip()  # Get "2 of 7"
    #         fraction = skills_match.replace(" of ", "/").strip()  # Convert to "2/7"
    #         preferences.append(fraction)
    # if len(preferences) == 2:
    #     preferences[1] = Fraction(preferences[1])
    # if preferences[0] == "Full-time" and (len(preferences) == 1 or (len(preferences) > 1 and preferences[1].numerator / preferences[1].denominator >= 0.5)):
    #     return True
    # else:
    #     return False
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

    driver.find_element(By.ID, "username").send_keys("veerakowshikkatam@gmail.com")
    driver.find_element(By.ID, "password").send_keys(passwrd)

    remember_me_checkbox = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
    is_checked = driver.execute_script("return arguments[0].checked;", remember_me_checkbox)
    if is_checked:
        driver.execute_script("arguments[0].checked = false;", remember_me_checkbox)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Navigate to job search page
    driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&f_E=2&f_TPR=r86400&f_AL=true")

    while True:
        try:
            # Wait for job cards to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container"))
            )

            # Get all job cards on the current page
            job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")
            print(job_cards)

            for job_card in job_cards:
                try:
                    # Click on each job card to load details in the sidebar
                    driver.execute_script("arguments[0].scrollIntoView();", job_card)
                    job_card.click()
                    time.sleep(2)

                    # Extract preferences and job description
                    company = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name")
                    company_name = company.text
                    pref = driver.find_elements(By.CLASS_NAME, "job-details-preferences-and-skills__pill")
                    jd = driver.find_elements(By.CLASS_NAME, "jobs-description__content")

                    # Check preferences and experience criteria
                    if check_preferences(pref) and check_experience(jd):
                        try:
                            # Click Easy Apply if available
                            print(company_name)
                            # easy_apply_button = driver.find_element(By.XPATH, "//button[@aria-label='Easy Apply']")
                            # easy_apply_button.click()
                            # time.sleep(5)  # Allow Easy Apply process to complete (or handle modal if any)
                        except Exception as e:
                            print(f"No Easy Apply button found for this job: {e}")
                except Exception as e:
                    print(f"Error processing job card: {e}")

            # Check for and click the "Next" button to go to the next page of results
            # try:
            #     next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
            #     if next_button.is_enabled():
            #         next_button.click()
            #         time.sleep(5)  # Allow next page to load
            #     else:
            #         break  # Exit loop if "Next" button is disabled (last page)
            # except Exception as e:
            #     print(f"No Next button found: {e}")
            #     break  # Exit loop if no Next button is found (last page)
        except Exception as e:
            print(f"Error loading jobs: {e}")
            break

    driver.quit()

if __name__ == "__main__":
    main()