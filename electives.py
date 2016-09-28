from pymongo import MongoClient
import json

# Create another collection to easily fetch the elective classrooms querying by timetables.
# This duderino has a lot of common code with classroom.py, I will do some refactoring inshallah.

def getCollection(host = 'localhost', port = 27017, collectionName = '20161'):
    client = MongoClient(host, port)
    db = client.offerings # @TODO read the db name from config file.
    collection = db['semester' + collectionName]
    return collection

def getDepartmentList(collection):
    return map(str, collection.distinct('departmentCode'))

def getCourseList(collection, departmentCode):
    return map(str, collection.distinct('courseCode', {"departmentCode": departmentCode}))

def getSectionsList(collection, departmentCode, courseCode):
    return map(str, collection.distinct('section', {"departmentCode": departmentCode, "courseCode": courseCode}))

def getCourse(collection, departmentCode, courseCode, section):
    return collection.find({"departmentCode": departmentCode, "courseCode": courseCode, "section": section})

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

electivesCollection = getCollection(collectionName = (semester + 'electives'))
electivesCollection.delete_many({})

departments = getDepartmentList(collection)

count = 0
length = len(departments)
for department in departments:
    count += 1
    print "Processing department " + department + " " + str(count) + "/" + str(length)
    if(len(department) > 0):
        courses = getCourseList(collection, department)
        for course in courses:
            sections = getSectionsList(collection, department, course)
            for section in sections:
                result = getCourse(collection, department, course, section)
                for thatClass in result:
                    try:
                        lectures = thatClass['lectures']

                        timetable = []
                        for lecture in lectures:
                            try:
                                day = lecture['day']
                                hours = lecture['hours']


                                tt = getTimeAndDay(day, hours)
                                for t in tt:
                                    timetable.append(t)

                            except AttributeError:
                                print "No such attribute"

                        electivesCollection.insert({
                            'departmentCode': department,
                            'courseCode': course,
                            'section': section,
                            'hours': timetable,
                            'instructor': thatClass['instructor'],
                            'title': thatClass['title']
                        })
                    except:
                        print "No lectures for " + str(thatClass['departmentCode'] + thatClass['courseCode'] + '-' + thatClass['section'])
