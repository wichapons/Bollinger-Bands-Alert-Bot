import datetime

def waitTime():
   current_time = datetime.datetime.now()
   current_minute = current_time.minute # get current minute value
   # calculate time until next quarter hour
   if current_minute < 15:
      wait_time = (15 - current_minute) * 60 - current_time.second
   elif current_minute < 30:
      wait_time = (30 - current_minute) * 60 - current_time.second
   elif current_minute < 45:
      wait_time = (45 - current_minute) * 60 - current_time.second
   else:
      wait_time = (60 - current_minute) * 60 - current_time.second 

   return wait_time

