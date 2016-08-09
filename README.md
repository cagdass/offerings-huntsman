# Offerings Huntsman 

## What dis be?
Get your JSON data of the Bilkent University courses offered in the upcoming semester. 

## *I can't be arsed to this* API:

* For all the data of all the classes:

	GET cgds.me:3000

* Filter by department:

	GET cgds.me:3000?department=CS

* Sample data:
	
```{<br>
  "_id": "57a9966fb93db11e9fba512a",<br>
	  "lectures": <br>
    [
      {<br>
               "hours": ["08:40","09:30"],<br>
	"status": "[S]",<br>
	"day": "Mon",<br>
	"location": "EA-Z01"<br>
      },<br>
      {<br>
	"hours": ["09:40","10:30"],<br>
	"status": "",<br>
	"day": "Mon",<br>
	"location": "EA-Z01"<br>
      },<br>
      {<br>
	"hours": ["10:40","12:30"],<br>
	"status": "",<br>
	"day": "Wed",<br>
	"location":"EA-Z01"<br>
      }
    ],<br>
  "title": "Algorithms for Web-Scale Data",<br>
  "bilkentCredit": "3",<br>
  "section": "1",<br>
  "totalQuota": "60",<br>
  "enrollmentElective": "0",<br>
  "enrollmentTotal": "0",<br>
  "enrollmentMust":"0",<br>
  "courseCode": "425",<br>
  "departmentCode": "CS",<br>
  "instructor": ["Muhammet Mustafa Özdal"],<br>
  "ectsCredit":"6",<br>
  "availableQuota":"60"<br>
}```

Feel free to contribute if you want to add other filters and stuff.

## Requirements 
* [Python 2.7.x](http://docs.python-guide.org/en/latest/starting/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [mongodb](https://docs.mongodb.com/manual/installation/) (Optional, modify the code if not desired)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Usage

	pip install beautifulsoup4 #If you don't have it already.
	pip install pymongo #Optional.
	git clone https://github.com/cagdasoztekin/offerings-huntsman.git
	cd offerings-huntsman
	nano parser/crawler.py #Modify if necessary.
	python parser/crawler.py

## Notes

* Change the boolean to False in line 51 if you do not want to write it to a database.
* Do not forget to modify the default parameters when writing to the database.
- By default, it connects to MongoDB at your localhost, on port 27017.
- Writes the results to the database named 'offerings', all the data for all departments into the same collection, titled 'semester20161'.
- And all this is mutable.
