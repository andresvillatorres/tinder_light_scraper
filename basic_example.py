# importing stuff from the 
# testing user names
# from tinderAPI import person
import time
import random
from tinderAPI import tinderAPI



# # this location is Zurich
LAT = 47.378564115906364
LON = 8.555179762127182

# # scraping through people nearby
gender = "unknown"
if __name__ == "__main__":
    token = "247628ed-39a5-4fdc-bb7f-8d4df213316d"
    # initializes session
    api = tinderAPI.tinderAPI(token) 
    while True:
        persons = api.nearby_persons_extended(LAT,LON)
        for person in persons:
            print(person.name + " , age: " + str(person.age)  + " , " + str(person.gender) +  ", distance to me in km: " + str(person.distance)  + " , bio:"+ str(person.bio) )
            time.sleep(random.random()*3.25)

