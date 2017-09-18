# CUTS
## Curtin University Timetable Scraper

### What is it
This is simple webscraper written in python 2, which uses selenium to emulate a browser and scrape data from the [Curtin Timetable](timetable.student.curtin.edu.au) website.

It then builds html timetables for each room in building 314 which we use.

### Dependancies
 * Selenium
 * PhantomJS
 * BeautifulSoup

### How to run it
You will need to edit the script and add the unit codes and names to the units list. You also may want to add some colours of your choosing.

Then simply install the dependancies, and run the script with python 2.

### When it doesn't work?
The script is QnD, the web app it interacts with can be slow, so if it fails just run it again! 