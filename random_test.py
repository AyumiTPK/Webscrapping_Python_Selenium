import random

#Creating time lists
morning_peak = ["7:00", "7:30", "8:00", "8:30", "9:00", "9:30"]
inter_peak = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"]
evening_peak = ["16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]
off_peak = ["00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]


#Creating a function to pick a random time from each list
def random_time(time_list):
    return random.choice(time_list)

#Printing the results
print("Morning Peak:", random_time(morning_peak))
print("Inter Peak:", random_time(inter_peak))
print("Evening Peak:", random_time(evening_peak))
print("Off Peak:", random_time(off_peak))