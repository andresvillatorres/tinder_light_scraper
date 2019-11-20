# tinder_light_scraper

Currently developing this as part of a PhD Project, at the moment this is a very basic, sneaky but powerful scraper.

Download or clone repository through the link provided here: https://github.com/andresvillatorres/tinder_light_scraper

In order to use the Tinder Scraper you need to login to the network. And for that you need an account and get your access token. Here are two methods: 

With inspector tool: open Tinder on Firefox. Open inspector with right clicking on mouse or trackpad. Select the “Network” tab. Look for the XHR GET or POST request and unfold one, scroll down until you find the X-Auth-Token which should look something like this: 24762xxx-xxxx-xxxx-xxxx-xxxdf213316d.

With sms verification. Run the python script sms_auth.py inside utils folder. Provide your phone number. Provide the authorisation code you’ll get through sms. It should give you back the same X-Auth-Token.

Once you have retreived your x auth token paste it inside the basic_example.py script on [line 17]   ———>  token = “24762xxx-xxxx-xxxx-xxxx-xxxdf213316d”. 

Save it and run the script on Terminal at the right folder path with: $ python3.7 basic_example.py

The script should print out name, age, gender, distance to you and the bio if available of persons nearby. 

Be aware that you might need to update or install modules that may be missing. Errors in Terminal are self explaining and will guide you through.

Alright, that’s it. Don’t hesitate contacting me if any questions: andres.villa_torres@zhdk.ch or info@andresvillatorres.work
