from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import ollama
from fractions import Fraction
from passw import passwrd, openai_key
import time



#Disabling webrtc and log warnings and info in the console
chrome_options = Options()
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--log-level=3")

#Using Chrome from the webdriver
driver = webdriver.Chrome( options = chrome_options)

def check_preferences(pref):
    data = []
    for element in pref:
        text = element.text.strip()
        if text:
            data.append(text)
    print(data)

    preferences = []
    for item in data:
        if "Full-time" in item:
            preferences.append("Full-time")
        elif "skills match" in item:
            skills_match = item.split("skills match")[0].strip()  # Get "2 of 7"
            fraction = skills_match.replace(" of ", "/").strip()  # Convert to "2/7"
            preferences.append(fraction)
    if len(preferences) == 2:
        preferences[1] = Fraction(preferences[1])
    if preferences[0] == "Full-time" and (len(preferences) == 1 or (len(preferences) > 1 and preferences[1].numerator / preferences[1].denominator >= 0.5)):
        return True
    else:
        return False

def check_experience(jd):
    data = []
    for element in jd:
        text = element.text.strip()
        if text:
            data.append(text)
    prompt = f"""
        Extract the required years of experience from the following job description.
        If no experience is mentioned, assume it as 0 years.

        Job Description:
        {data[0]}

        Return only the number of years as an integer.
        """

    response = ollama.run(
        model= 'deepseek-r1:7b',
        prompt = prompt
    )

    # Extract and return the response text
    extracted_experience = response['choices'][0]['message']['content'].strip()

    print(response)
    print(extracted_experience)
    if extracted_experience < 1:
        return True
    else:
        return False



def main():
    driver.get("https://www.linkedin.com/login")

    driver.find_element(By.ID, "username").send_keys("veerakowshikkatam@gmail.com")
    driver.find_element(By.ID, "password").send_keys(passwrd)

    remember_me_checkbox = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
    is_checked = driver.execute_script("return arguments[0].checked;", remember_me_checkbox)
    if is_checked:
        driver.execute_script("arguments[0].checked = false;", remember_me_checkbox)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()


    driver.get("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&f_E=2&f_TPR=r86400&f_AL=true")
    pref = driver.find_elements(By.CLASS_NAME, "job-details-preferences-and-skills__pill")
    jd = driver.find_elements(By.CLASS_NAME, "jobs-description__content")
    print(check_preferences(pref = pref))
    print(check_experience(jd = jd))
    if jd and pref:
        driver.find_element(By.XPATH, "//button[@aria-label='Easy Apply']").click()

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()