import datetime
# get current minute value
current_time = datetime.datetime.now()
current_minute = current_time.minute

# calculate time until next hour
if current_minute < 60:
    wait_time = ((60 - current_minute) * 60 - current_time.second)+5  #add 5 sec delay prevent .json data is not ready in time
    print(f'next notify in {wait_time/60} minutes')
    