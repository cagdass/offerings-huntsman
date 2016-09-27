import urllib2
import json
from bs4 import BeautifulSoup

from parser import Parser
from inserter import Inserter

# Takes about 2 minutes to crunch data of all the departments' offerings

class Department:
    def __init__(self):
        self.departments = ["ACC", "ADA", "AMER", "ARCH", "BF", "BIM", "BTE", "CAA", "CAD", "CHEM", "CI", "CINT", "CITE", "COMD", "CS", "CTE", "CTIS", "CTP", "DIR", "ECON", "EDEB", "EE", "EEE", "ELIT", "ELS", "EM", "EMBA", "ENG", "ETE", "ETS", "FA", "FRE", "FRL", "FRP", "GE", "GER", "GIA", "GRA", "HART", "HCIV", "HIST", "HISTR", "HUM", "IAED", "IE", "IR", "ITA", "JAP", "LAUD", "LAW", "MAN", "MATH", "MBA", "MBG", "ME", "MIAPP", "MSC", "MSG", "MSN", "MTE", "MUS", "MUSS", "NSC", "PE", "PHIL", "PHYS", "PNT", "POLS", "PREP", "PSYC", "RUS", "SFL", "SOC", "SPA", "TE", "TEFL", "THEA", "THM", "THR", "THS", "TRIN", "TRK", "TTP", "TURK"]
        self.count = 0
        self.length = len(self.departments)

    def next(self):
        self.count += 1
        if(self.count > self.length):
            return ''
        else:
            return self.departments[self.count - 1]

def get_pretty_source(departmentCode, semester):
    url = 'https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE='
    url2 = '&SEMESTER='

    page = urllib2.urlopen(url + departmentCode + url2 + semester).read()
    soup = BeautifulSoup(page, 'html.parser')
    soup.prettify()
    return soup

def get_courses(departmentCode, parser):
    pageSource = get_pretty_source(departmentCode, semester)
    trs = pageSource.findAll('tr')
    currentCourses = []

    for i in xrange(2, len(trs)):
        td_list = trs[i].find_all("td")
        parser.set_td_list(td_list)
        currentCourse = parser.get_course()
        currentCourses.append(currentCourse)

    return currentCourses

departments = Department()

# TODO: Add logic to set the semester to spring if the month is January/February, fall if month is July/August/September/October, and May and June for summer.
with open('config.json') as config:
    data = json.load(config)
semester = data['semester']

# Instantiate new Parser
parser = Parser()
writeToMongo = True # Change to False not to write to mongo database.

if writeToMongo:
    # Check for options for initialization of Inserter, options like where to write, db
    inserter = Inserter(collectionName=semester)
    collection = inserter.getCollection()

departmentCode = departments.next()
while departmentCode != '':

    # print departmentCode
    currentCourses = get_courses(departmentCode, parser)

    departmentData = {'currentCourses': currentCourses}
    # print departmentData
    jsonData = json.dumps(departmentData) # All yours

    if writeToMongo:
        for course in currentCourses:
            sectionID = collection.insert_one(course).inserted_id

    departmentCode = departments.next()
