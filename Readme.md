
# Lunch Buddy

I wrote this python application to fix the flood of emails I was receiving from colleagues telling me they were "going to lunch"
and how they were covering others who had gone to lunch. I am sure there are many apps that could easily help with the situation, 
but it was a good excuse to build a Flask App.

I integreated this app with twilio messaging. Twilio is a great platform that allows you to experiment for free all types of
communications technology. 

## Design Considerations

* Scheduling Notifications
    * This is a tricky one...I have looked into python's `threading` module 
    
* Graphing Lunchs Taken

* Storing all lunchs taken by users, and auto-completing for recent lunchs taken?

## To-Do 

1. Time-off time parsing
    * Currently only supports military time, need to configure for am/pm time (12 hour clock
    * design a test -> 

2. Text time-off notifications instead of navigating to website
    * need to expose flask development server to web
    * create flask endpoint for twilio receiving

3. 

