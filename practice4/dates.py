#1
import datetime

x = datetime.datetime.now()
print(x)

#2
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#3
import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#4
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

#5
from datetime import datetime

time1 = datetime.strptime("14:30:00", "%H:%M:%S")
time2 = datetime.strptime("18:45:30", "%H:%M:%S")

difference = time2 - time1

print("Time difference:", difference)