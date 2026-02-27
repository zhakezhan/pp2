import datetime


#Subtract five days from current date
today = datetime.datetime.now()
five_days_ago = today - datetime.timedelta(days=5)
print("Five days ago:", five_days_ago)


#Print yesterday, today, tomorrow
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday.date())
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())


#Drop microseconds
no_microseconds = today.replace(microsecond=0)
print("Without microseconds:", no_microseconds)


#Difference between two dates in seconds
date1 = datetime.datetime(2025, 1, 1)
date2 = datetime.datetime(2025, 3, 1)

difference = date2 - date1
print("Difference in seconds:", difference.total_seconds())