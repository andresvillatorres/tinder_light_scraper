import datetime
from geopy.geocoders import Nominatim
import requests
import random
import time
import os
import csv
 


TINDER_URL = "https://api.gotinder.com"
geolocator = Nominatim(user_agent="auto-tinder")
PROF_FILE = "./images/unclassified/profiles.txt"
PROF_FILE_EX = "./images/unclassified/profilesExtended.txt"
# DATABASE = "./images/unclassified/dataBase.csv"

class tinderAPI():

    def __init__(self, token):
        self._token = token

    def profile(self):
        data = requests.get(TINDER_URL + "/v2/profile?include=account%2Cuser", headers={"X-Auth-Token": self._token}).json()
        # print(data)
        return data
        # return Profile(data["data"], self)

    def matches(self, limit=100):
        data = requests.get(TINDER_URL + f"/v2/matches?count={limit}", headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda match: Person(match["person"], self), data["data"]["matches"]))

    def like(self, user_id):
        data = requests.get(TINDER_URL + f"/like/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return {
            "is_match": data["match"],
            "liked_remaining": data["likes_remaining"]
        }

    def dislike(self, user_id):
        requests.get(TINDER_URL + f"/pass/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return True

    def nearby_persons(self):
        data = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda user: Person(user["user"], self), data["data"]["results"]))

    def nearby_persons_distance(self):
        furtherData = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
        return list(map(lambda distance_mi: PersonDistance(distance_mi["distance_mi"],self), furtherData["data"]["results"]))

    # a function fetching also distance data 
    def nearby_persons_extended(self,lat,lon):
        data = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
        fD = data
        loc = [lat,lon]
        return list(map(lambda user, distance_mi, location: Person(user["user"], distance_mi["distance_mi"], loc, self), data["data"]["results"] , fD["data"]["results"], loc))


    def set_new_location(self,lat,lon):
        message = requests.post(TINDER_URL + f"/user/ping", {"lat":lat,"lon":lon}, headers={"X-Auth-Token": self._token}).json()
        return print(message)
            

# class Profile(object):
#     def __init__ (self,data,api):
#         self.metadata = data



class PersonDistance(object):
    def __init__(self,d,api):
        self.distance = d





class Person(object):

        # self.distance = furtherData

    def __init__(self,data,fD,loc,api):
        self._api = api
        # rounding the distance after converting it into km
        self.distance = round(fD/1.60934,2)
        self.location = loc
        self.id = data["_id"]
        self.name = data.get("name", "Unknown")
        self.bio = data.get("bio", "")
        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        b_date=datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        today = datetime.date.today()
        self.age = - b_date.year + today.year

        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))
        self.city = data.get("city")

        self.metaData = data
        # if data.get("pos", False):
            # self.location = geolocator.reverse(f'{data["pos"]["lat"]}, {data["pos"]["lon"]}')
        # else:
            # self.location = f"Unknown location ... distance to you : " + str(self.distance) + f" miles" 


    def __repr__(self):
        return f"{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"


    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)


    # inside the Person-class function for downloading images
    def download_images(self, folder=".",sleep_max_for=0):
        with open(PROF_FILE, "r") as f:
            lines = f.readlines()
            if self.id in lines:
                return
            else:
                with open(PROF_FILE_EX, "a") as g:
                    g.write(self.id + ", name: " + self.name + ", age: " +str(self.age)+ "\r\n") 

        with open(PROF_FILE, "a") as f:
            f.write(self.id+"\r\n")


        index = -1


        # newDatePath = os.getcwd() + (folder.replace(".","")) + "/" + str(datetime.date.today())
        newDatePath = os.getcwd() + (folder.replace(".",""))
        if self.gender == 'Female':
            newGenderPath = newDatePath+ "/Female"
            # print(newGenderPath)
        if self.gender == 'Male':
            newGenderPath = newDatePath+ "/Male"
            # print(newGenderPath)
        if self.gender != 'Male' and self.gender != 'Female':
            newGenderPath = newDatePath+ "/Ungendered"
            # print(newGenderPath)    
        newPersonPath = newGenderPath+ "/" + str(self.id)
        print(newPersonPath)

        DATABASE = newDatePath + "/"+ "dataBase.csv"

        if not os.path.exists(newDatePath):
            os.mkdir(newDatePath)
        if not os.path.exists(newGenderPath):
            os.mkdir(newGenderPath)    
        if not os.path.exists(newGenderPath):
            os.mkdir(newGenderPath)
        if not os.path.exists(newPersonPath):
            os.mkdir(newPersonPath)

        with open(DATABASE, 'a') as csv_table:
            csv_writer = csv.writer(csv_table, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([datetime.datetime.now(),self.id, self.name,self.age,self.gender,self.birth_date,self.jobs, self.bio, self.distance, self.metaData])


        with open(newPersonPath + "/" +'personDataBase.csv', 'w') as csv_t:
            csv_w = csv.writer(csv_t,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_w.writerow([datetime.datetime.now(),self.id, self.name,self.age,self.gender,self.birth_date,self.jobs, self.bio, self.distance, self.metaData])
       
        for image_url in self.images:
            index += 1
            print(image_url + f" , image # "  + str(index)  )
            time.sleep(random.random()*sleep_max_for)

            

            req = requests.get(image_url, stream=True)
            if req.status_code == 200:
                with open(f"{newPersonPath}/{self.name}_{self.age}_{index}.jpeg", "wb") as f:
                     f.write(req.content)

            time.sleep(random.random()*sleep_max_for)











