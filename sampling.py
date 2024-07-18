from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import schedule
import time


# Function to extract traffic data
def scrap_data():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get('https://www.trafficengland.com/traffic-report')
    driver.implicitly_wait(10)

    # Find the motorway dropdown and select a motorway
    motorway_dropdown = driver.find_element(By.CSS_SELECTOR, '.tr-menu-motorway')
    motorway_dropdown.click()  # Click to expand the dropdown (if not expanded by default)

    # Select a motorway option (e.g., M1)
    motorway_options = driver.find_elements(By.CSS_SELECTOR, '.tr-menu-motorway option')
    for option in motorway_options:
        if option.text == 'M1':
            option.click()
            break

    # Click the search button
    search_button = driver.find_element(By.CLASS_NAME, "tr-menu-motorway-search")
    search_button.click()

    # Retrieve junction data
    junction_numbers = driver.find_elements(By.CSS_SELECTOR, 'span.tr-junction-number')
    left_sections = driver.find_elements(By.CSS_SELECTOR, 'div.tr-junction-section-content-left')
    right_sections = driver.find_elements(By.CSS_SELECTOR, 'div.tr-junction-section-content-right')

    # Prepare data into a list of dictionaries
    data = []
    for i in range(len(junction_numbers)):
        current_junction = junction_numbers[i].text.strip()
        if current_junction == 'J1':
            continue

        next_index = i + 1
        if next_index < len(junction_numbers):
            next_junction = junction_numbers[next_index].text.strip()
            junction = f"{current_junction}-{next_junction}"
        else:
            junction = current_junction

        left_speed = left_sections[i].find_element(By.CSS_SELECTOR, 'span').text.strip() if i < len(
            left_sections) else "No speed"
        left_comments = left_sections[i].find_elements(By.CSS_SELECTOR,
                                                       'div.tr-junction-section-link > div.tr-junction-section-event > a > span.event-name')
        left_comments_text = [comment.text.strip() for comment in left_comments]
        left_comment = ', '.join(left_comments_text) if left_comments_text else "No comment"

        right_speed = right_sections[i].find_element(By.CSS_SELECTOR, 'span').text.strip() if i < len(
            right_sections) else "No speed"
        right_comments = right_sections[i].find_elements(By.CSS_SELECTOR,
                                                         'div.tr-junction-section-link > div.tr-junction-section-event > a > span.event-name')
        right_comments_text = [comment.text.strip() for comment in right_comments]
        right_comment = ', '.join(right_comments_text) if right_comments_text else "No comment"

        current_datetime = datetime.datetime.now()  # Get the current date and time
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M:%S")
        day_of_week = current_datetime.strftime("%A")

        data.append({
            "Junction": junction,
            "Left Speed": left_speed,
            "Left Comment": left_comment,
            "Right Speed": right_speed,
            "Right Comment": right_comment,
            "Date": current_date,
            "Time": current_time,
            "Day of Week": day_of_week
        })

    # Create a DataFrame from the data and display it
    df = pd.DataFrame(data)
    timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{timestamp}.csv"
    df.to_csv(csv_filename, index=False)

    # Close the browser
    driver.quit()


# Schedule times
schedule.every().day.at("10:38").do(scrap_data)
schedule.every().day.at("11:30").do(scrap_data)
schedule.every().day.at("18:18").do(scrap_data)
schedule.every().day.at("23:00").do(scrap_data)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
