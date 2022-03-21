import re as regex

#Check if the string starts with "The" and ends with "Spain":

txt = "/subscription subscribed"
re_available = regex.compile(r'\/subscription\ssubscribed')

print("hello")

if re_available.match(txt) is not None:
    print("YES! We have a match!")
else:
    print("No match")