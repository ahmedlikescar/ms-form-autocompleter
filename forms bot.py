from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import random

#------------------
# MICROSOFT FORMS AUTO completer
#------------------

# start firefox, used firefox because i dont use the browser and can let it sit in the background, if u wanna use anything else lmk ill add
firefox_options = Options()
firefox_options.headless = False

geckodriver_path = "/opt/homebrew/bin/geckodriver"  # Mac M1/M2/M3
# geckodriver_path = "C:/Windows/System32/geckodriver.exe"  # Windows

try:
    driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)
    print("Browser opened!")
except Exception as e:
    print("Could not open Firefox:", e)
    exit()


def answer_form():

    print("waiating for page to load, its not bugged")
    time.sleep(5)

    # RADIO BUTTONS (multiple choice questions)

    radio_groups = driver.find_elements(By.XPATH, "//div[@role='radiogroup' and not(@data-automation-id='npsContainer')]")
    print(f"Found {len(radio_groups)} radio question(s)")

    for group in radio_groups:
        try:
            options = group.find_elements(By.XPATH, ".//*[@role='radio']")
            if options:
                chosen = random.choice(options)
                driver.execute_script("arguments[0].scrollIntoView(true);", chosen)
                time.sleep(0.5)
                chosen.click()
                time.sleep(0.5)
                print("  answered a radio question")
        except Exception as e:
            print("  skipped? a radio question:", e)


    # NUMBER INPUT BOXES (type a number)

    number_inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
    print(f"Found {len(number_inputs)} number input(s)")

    for field in number_inputs:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", field)
            time.sleep(0.5)
            field.clear()
            value = str(random.randint(0, 10))
            field.send_keys(value)
            time.sleep(0.5)
            print(f"  typed {value} into number field")
        except Exception as e:
            print("  skipped a number field:", e)

    # (the 0-10 clickable grid boxes)
    # they're <td role="presentation"> inside npsContainer

    nps_containers = driver.find_elements(By.XPATH, "//*[@data-automation-id='npsContainer']")
    print(f"Found {len(nps_containers)} NPS scale question(s)")

    for container in nps_containers:
        try:
            cells = container.find_elements(By.XPATH, ".//td[@role='presentation']")
            print(f"  found {len(cells)} cells in scale")

            if cells:
                chosen = random.choice(cells)
                driver.execute_script("arguments[0].scrollIntoView(true);", chosen)
                time.sleep(0.5)

                try:
                    chosen.click()
                    print("  clicked NPS cell!")
                except:
                    # If clicking the cell doesn't work, click what's inside it
                    inner = chosen.find_element(By.XPATH, ".//*")
                    inner.click()
                    print("  clicked inside NPS cell!")

                time.sleep(0.5)

        except Exception as e:
            print("  skipped NPS question:", e)


# ASK HOW MANY TIMES TO SUBMIT

form_url = ""

try:
    num_submissions = int(input("\nenter how many times u wanna submit "))
except:
    print("invalid number. closing, run again")
    driver.quit()
    exit()

# final loop and submit

for i in range(num_submissions):

    print("\nsubmission {i + 1} of {num_submissions}")

    try:
        driver.get(form_url)
        time.sleep(6)

        answer_form()

        # find and click the Submit button
        submitted = False
        submit_xpaths = [
            "//button[contains(., 'Submit')]",
            "//span[contains(text(), 'Submit')]",
            "//button[@type='submit']",
            "//div[@role='button']"
        ]

        for path in submit_xpaths:
            try:
                btn = driver.find_element(By.XPATH, path)
                driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                time.sleep(1)
                btn.click()
                submitted = True
                print(f"submitted ({i + 1} of {num_submissions})")
                break
            except:
                pass

        if not submitted:
            print("could not find the Submit button.")

        time.sleep(3)

    except Exception as e:
        print(f"something went wrong on submission {i + 1}:", e)


print("all submissions completed")
driver.quit()