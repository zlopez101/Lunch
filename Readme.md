
# Lunch Buddy

I wrote this python application to fix the flood of emails I was receiving from colleagues telling me they were "going to lunch"
and how they were covering others who had gone to lunch. I am sure there are many apps that could easily help with the situation, 
but it was a good excuse to build a Flask App.

I integrated this app with twilio messaging. Twilio is a great platform that allows you to experiment for free all types of
communications technology. 

### Twilio currently won't allow text messages receiving to POST methods to private IP addresses. 
I'd like for users to be able to text their lunch schedule to the twilio number, and that number to make a POST request to the website, where the lunch would be catalogued, graphed, and notification created. Because I haven't set a public domain name, twilio's API won't allow a POST request to private IP address. 

## Design Considerations

* Scheduling Notifications
    * This is a tricky one...I have looked into python's `threading` module 
    * I think the new, "simpler" plan would be to generate a text/email at the time of creation of a LunchTime, 
    * Another possiblities is to set up an internal endpoint that a JS script querys periodically and if any LunchTime start is within a specific window then generate an email/text
    * also start a crontab table on linux deployment...but since developing on a windows system becomes more complicated 
    
* Graphing Lunchs Taken
    * Basically Done
    * Only thing still left to do is displaying names in the bars instead of on the y-axis

* Storing all lunchs taken by users, and auto-completing for recent lunchs taken?

* Prett-ify the website
    * could make the website look more pleasing,

* Prevention of certain LunchTimes
    * Ideally, employees would stagger their lunchs so that everyone wouldn't be off at the same time. However, I could set up an internal monitoring system that manages LunchTime creation. If x % of folks have already taken a lunch between certain hours, no more Lunchs could be taken until the end of some period.

## To-Do 

1. Time-off time parsing
    * Currently only supports military time, need to configure for am/pm time (12 hour clock
    * design a test -> 

2. Text time-off notifications instead of navigating to website
    * need to expose flask development server to web
    * create flask endpoint for twilio receiving
    * this cannot be done with a private ip address...need to serve the app and get a domain name...

    ### Hold on this task

3. 

