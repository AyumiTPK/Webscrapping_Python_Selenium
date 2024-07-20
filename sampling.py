from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import schedule
import time
import random


# Creating lists of times
morning_peak = ["07:00", "07:30", "08:00", "08:30", "09:00", "09:30"]
inter_peak = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00",
              "15:30"]
evening_peak = ["16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]
off_peak = ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30",
            "06:00", "06:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]


# Creating a function to select a random time
def random_time(time_list):
    return random.choice(time_list)


# Creating a function to extract motorway data
def scrap_data():
    # Accessing the website
    driver = webdriver.Chrome()
    driver.get("https://www.trafficengland.com/traffic-report")
    driver.implicitly_wait(10)

    # Selecting a motorway from dropdown
    motorway_dropdown = driver.find_element(By.CSS_SELECTOR, ".tr-menu-motorway")
    motorway_dropdown.click()
    motorway_options = driver.find_elements(By.CSS_SELECTOR, ".tr-menu-motorway option")
    for option in motorway_options:
        if option.text == "M1":
            option.click()
            break

    # Clicking the search button
    search_button = driver.find_element(By.CLASS_NAME, "tr-menu-motorway-search")
    search_button.click()

    # Scrapping data
    driver.implicitly_wait(10)
    junction_numbers = driver.find_elements(By.CSS_SELECTOR, "span.tr-junction-number")
    left_sections = driver.find_elements(By.CSS_SELECTOR, "div.tr-junction-section-content-left")
    right_sections = driver.find_elements(By.CSS_SELECTOR, "div.tr-junction-section-content-right")

    # Extracting data a list
    data = []
    for i in range(len(junction_numbers)):
        # Extracting junction numbers
        current_junction = junction_numbers[i].text.strip()
        if current_junction == "J1":  # Ignoring J1 as there is no speed data
            continue
        # Joining junction names (e.g. J48-J47)
        next_index = i + 1
        if next_index < len(junction_numbers):
            next_junction = junction_numbers[next_index].text.strip()
            junction = f"{current_junction}-{next_junction}"
        else:
            junction = current_junction
        # Extracting speed and event names on both directions
        # Joining event comments as some motorways have multiple events
        left_speed = left_sections[i].find_element(By.CSS_SELECTOR, "span").text.strip() if i < len(
            left_sections) else "No speed"
        left_comments = left_sections[i].find_elements(By.CSS_SELECTOR,
                                                       "div.tr-junction-section-link > div.tr-junction-section-event > a > span.event-name")
        left_comments_text = [comment.text.strip() for comment in left_comments]
        left_comment = ", ".join(left_comments_text) if left_comments_text else "No comment"

        right_speed = right_sections[i].find_element(By.CSS_SELECTOR, "span").text.strip() if i < len(
            right_sections) else "No speed"
        right_comments = right_sections[i].find_elements(By.CSS_SELECTOR,
                                                         "div.tr-junction-section-link > div.tr-junction-section-event > a > span.event-name")
        right_comments_text = [comment.text.strip() for comment in right_comments]
        right_comment = ", ".join(right_comments_text) if right_comments_text else "No comment"
        # Adding date, time, day of the week for easier processing
        current_datetime = datetime.datetime.now()
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

    # Saving the data into a file
    df = pd.DataFrame(data)
    timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{timestamp}.csv"
    df.to_csv(csv_filename, index=False)

    # Quitting the driver
    driver.quit()


# Creating a function to reset daily schedule
def setup_schedule():
    schedule.clear()
    morning_time = random_time(morning_peak)
    inter_time = random_time(inter_peak)
    evening_time = random_time(evening_peak)
    off_time = random_time(off_peak)

    schedule.every().day.at(morning_time).do(scrap_data)
    schedule.every().day.at(inter_time).do(scrap_data)
    schedule.every().day.at(evening_time).do(scrap_data)
    schedule.every().day.at(off_time).do(scrap_data)
    print(f"Execution scheduled at: {morning_time}, {inter_time}, {evening_time}, {off_time}")


# Creating a function to check if midnnight
def check_midnight():
    if datetime.datetime.now().time() == datetime.time(0, 0):
        setup_schedule()


# Setting schedule once
setup_schedule()

# Running the scheduler
while True:
    check_midnight()
    schedule.run_pending()
    time.sleep(1)
