# Imagine how many lines of code, and hours of innocent lives it would have taken to write this in C.
import re

class Parser:
  def __init__(self):
      self.regex = re.compile('[0-9\[\]]')

  def get_pretty_source(self, departmentCode, semester):
      url = 'https://stars.bilkent.edu.tr/homepage/print/plainOfferings.php?COURSE_CODE='
      url2 = '&SEMESTER='

      page = urllib2.urlopen(url + departmentCode + url2 + semester).read()
      soup = BeautifulSoup(page, 'html.parser')
      soup.prettify()
      return soup

  def set_td_list(self, td_list):
      self.td_list = td_list

  def get_course(self):
    count = 0
    currentCourse = {}

    # Keeping the count of how many td elements have been looked at so far.
    for td in self.td_list:
      try:
        data = td.text
        # For each condition that follows, examples of the data inside will be given from CS425.
        # Course information. Example: 'CS425-1'. Separated into departmentCode: 'CS', courseCode: '425', section: '1'.
        if count == 0:
          departmentCode = str(data.split(" ")[0])
          currentCourse['departmentCode'] = departmentCode
          data = data[len(departmentCode)+1:]
          courseCode = data[:3]
          section = data[4:]
          currentCourse['courseCode'] = str(courseCode)
          currentCourse['section'] = str(section)
        # Course information. Example: 'Algorithms for Web-Scale Data'
        elif count == 1:
          currentCourse['title'] = str(data)
        # Instructor(s). Example: 'Mustafa Ozdal'
        elif count == 2:
          spans = td.find_all('span')
          # Instructor is "Staff" if there are no <span>'s inside <td>
          if len(spans) == 0:
              currentCourse['instructor'] = [data]
          else:
              # Separate them if the course has multiple instructors.
              # Initialize instructors array. Append new instructors from each span as you go.
              instructors = []
              for span in spans:
                  data = span.text
                  instructors.append(data)
              currentCourse['instructor'] = instructors
        # Bilkent credits. Example: '3'
        elif count == 3:
          currentCourse['bilkentCredit'] = str(data)
        # ECTS credits. Example: '6'
        elif count == 4:
          currentCourse['ectsCredit'] = str(data)
        # An array of lecture hours/locations. lectures[0] could be {day: 'Tue', startHour: '15:40', endHour: '16:30', status: '', location: 'EA-Z03'}
        elif count == 5:
          lectures = []
          for line in data.split('\n'):
            datums = line.split(' ')
            if(len(datums) > 1):
              day = str(datums[0])
              hours = str(datums[1]).split('-')
              startHour = str(hours[0])
              endHour = str(hours[1])
              status = ''
              location = str(datums[2]).strip()
              building = ''
              # As far as I gather, all classrooms follow the following format [[building]-[classroom]]. Split on '-' to get the building.
              try:
                  test = location.split("-")[0]
                  if(len(self.regex.findall(test)) == 0):
                      print test
                      building = test
              # Classroom might be empty.
              except IndexError:
                  print 'No building'
              if '[' in location:
                  status = location[-3:]
                  location = location[:-3]
              lectures.append({'day': day, 'hours': hours, 'location': location, 'status': status, 'building': building})
              currentCourse['lectures'] = lectures
        # Total quota of the course. '65' is quite common.
        elif count == 7:
          currentCourse['totalQuota'] = str(data)
        # Number of must enrollments. Equals to total quota if it is a popular course.
        elif count == 8:
          currentCourse['enrollmentMust'] = str(data)
        # Number of elective enrollments. Get out of our CS classes y'all EE people.
        elif count == 9:
          currentCourse['enrollmentElective'] = str(data)
        # Total number of enrollments, must equal to (must + elective) enrollments.
        elif count == 10:
          currentCourse['enrollmentTotal'] = str(data)
          try:
              # Assert the (must + elective) = total equality. Put in try/except to avoid future bugs.
              assert int(currentCourse['enrollmentTotal']) == int(currentCourse['enrollmentMust']) + int(currentCourse['enrollmentElective'])
          except AssertionError:
              print "Problem with total == must + elective"
        # Number of available quota. Usually '0' for popular courses.
        elif count == 12:
          currentCourse['availableQuota'] = str(data)
      except UnicodeEncodeError:
        pass
      count += 1

    return currentCourse
