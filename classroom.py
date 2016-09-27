from pymongo import MongoClient
import json

def getCollection(host = 'localhost', port = 27017, collectionName = '20161'):
    client = MongoClient(host, port)
    db = client.offerings # Change the database name
    collection = db['semester' + collectionName]
    return collection

def getClassroomList(collection):
    return collection.distinct('lectures.location')

def dayToInt(day):
    if(day == 'Mon'):
        return 0
    elif(day == 'Tue'):
        return 1
    elif(day == 'Wed'):
        return 2
    elif(day == 'Thu'):
        return 3
    elif(day == 'Fri'):
        return 4
    else:
        return -1

def hoursToInt(hours):
    start = str(hours[0])
    end = str(hours[1])

    hoursInt = []

    startInt = int(start.split(':')[0]) - 8
    endInt = int(end.split(':')[0]) - 8
    if(startInt > 12):
        startInt -= 1
        endInt -= 1
    for i in xrange(startInt, endInt):
        hoursInt.append(i)

    return hoursInt


def getTimeAndDay(day, hours):
    hoursInt = hoursToInt(hours)
    dayInt = dayToInt(day)

    schedule = map(lambda hour: dayInt % 5 + (hour * 5), hoursInt)

    return map(str, schedule)

# TODO: Add logic to set the semester to spring if the month is January/February, fall if month is July/August/September/October, and May and June for summer.
with open('config.json') as config:
    data = json.load(config)
semester = data['semester']

collection = getCollection()
classrooms = getClassroomList(collection)

classroomsCollection = getCollection(collectionName = (semester + 'classrooms'))
classroomsCollection.delete_many({})

# print getTimeAndDay('Mon', ['08:40', '10:30'])

count = 0
length = len(classrooms)
for classroom in classrooms:
    count += 1
    print "Processing classroom " + classroom + " " + str(count) + "/" + str(length)
    if(len(classroom) > 0):
        cursor = collection.find({'lectures.location': classroom})
        for result in cursor:
            lectures = result['lectures']
            for lecture in lectures:
                if(lecture['location'] == classroom):
                    currentState = classroomsCollection.find({'location': classroom})
                    currentHours = []
                    for result in currentState:
                        try:
                            currentHours = result['hours']
                            # Classroom found in db
                        except KeyError:
                            currentHours = []
                            # Classroom not found in classroom db
                    newHours = getTimeAndDay(lecture['day'], lecture['hours'])
                    for hour in newHours:
                        currentHours.append(hour)
                    # print "Update location: " + str(lecture['location']) + " new hours: " + str(currentHours)
                    classroomsCollection.update({'location': classroom}, {'location': classroom, 'hours': currentHours, 'building': lecture['building']}, upsert=True)
