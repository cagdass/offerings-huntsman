# Offerings Huntsman 

## What dis be?
Get your JSON data of the Bilkent University courses offered in the upcoming semester. 

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
