#!/bin/python
#
###
# This is a Python 2.73 web scraper/browser emulater which uses the 
# timetable.student.curtin.edu.au web app to construct a html
# timetable for all classes in building 314 computer labs.
# It uses a headless browser to interact with the website which means that
# it sometimes encounters errors, often becuase of the internet connection
# or the website being slow. If it fails just try again!
#
# Author: Luke Healy
# Last updated: August 2017
# License: MIT

import sys
import copy
import time
import datetime
from enum import IntEnum
import typing

from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# TODO use config file
webdriver_path = "C:\\chromedriver.exe"

Weekdays = Monday, Tuesday, Wednesday, Thursday, Friday =

##
# Class to store the information for a practical/workshop.
class Prac:
    def __init__(self, name, start_time_one, start_time_two, room, day, color):
        self.day = day
        self.unit_code = ""
        self.start_time_one = start_time_one
        self.start_time_two = start_time_two
        self.color = color
        self.room = room
        self.name = name

    def __str__(self):
        return self.name + ", " + self.day + ", " + str(self.start_time_one) + " - " + str(self.start_time_two) + ", " + self.room



class Room:
    def __init__(self, building, room):
        self.building = building
        self.room = room
        self.level = room[0]


class Browser:
    def __init__(self, url):
        self.driver = webdriver.Chrome(webdriver_path)
        self.url = url

    def setup_window(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1120, 550)

class Session:
    def __init__(self, name, timeslot, room, color):
        self.name = name
        self.start = timeslot.
        self.timeslot = timeslot
        self.room = room
        self.color = color

class Timetable:
    MIN_TIME = 8
    MAX_TIME = 18
    Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    def __init__(self):
        self.week = {}

        for day in Timetable.Days:
            self.week[day] = []

    def day(self, name):
        return self.week[name]

    def add_session(self, session):
        (self.day(session.day)).append(session)

    def remove_session(self, session):
        (self.day(session.day)).remove(session)





# class Day:
#     def __init__(self, day):
#         if day not in Weekdays:
#             raise InvalidDayError(day)
#         self.day = day
#
#         self.timeslots = self.build_timeslots()
#
#     def build_timeslots(self):
#         for time in r
#
#
#     def __repr__(self):
#         return self.day


class Timeslot
    def __init__(self, start, end, day):

        if all([start, end]) not in range(Timetable.MIN_TIME, Timetable.MAX_TIME + 1):
            raise InvalidTimeError([start, end])
        if start >= end:
            raise InvalidDayError([start, end])

        self.start = start
        self.end = end
        self.day = day

    def conflicts_with(self, timeslot):
        conflict = True
        if self.end.time() < timeslot.start.time():
            conflict = False
        elif self.start.time() > timeslot.end.time():
            conflict = False
        return conflict


class Unit:
    def __init__(self, name, code, color):
        self.name = name
        self.code = code
        self.color = color

class InvalidDayError(Exception):
    pass
    #TODO

class InvalidTimeError(Exception):
    pass
    #TODO


class Time:
    def __init__(self, time: str):
        self._time = None
        self.time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = datetime.datetime.strptime(time, "%H:%M")

    @time.getter
    def time(self):
        return self._time.time()




##
# Search for a unit on the website.
def search_unit(unit_code):
    unit_search = driver.find_element_by_id("criteriaEntry:filterUnitCodeOrTitle")
    unit_search.clear()
    unit_search.send_keys(unit_code)
    unit_search.send_keys(Keys.ENTER)

    unit_search.submit()
    driver.find_element_by_id("criteriaEntry:unitSearchButton").click()

##
# Select all units from the dropdown. We are searching by unit code so this
# works fine.
def select_unit():
    go = True
    while go:
        try:
            for o in Select(driver.find_element_by_id("criteriaEntry:allUnits")).options:
                o.click()
            go = False
        except:
            time.sleep(1)

##
# Click a button on the website.
def click_button(element_name):
    go = True
    while go:
        try:
            driver.find_element_by_name(element_name).click()
            go = False
        except:
            time.sleep(1)

##
# Parses the html of the timetable page per unit.
# This will have to be rewritten should the site change.
# It's dirty but tworks.
def parse_html(html, unit_name, color):
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find(id="timetableByUnits:timetable_gridbyunit").contents
    elements = soup.find_all("div", class_="entry")
    classes = []
    for e in elements:
        info = ""
        for i in str(e).split("&lt"):
            if i not in ";/b&gt;;/td&gt;;/tr&gt;;td&gt;;tr nowrap&gt;;br/&gt;;/i&gt;;table width=&quot;100%&quot;&gt;" and "<div" not in i and ";/table&gt;" not in i:
                i = i.replace(";td&gt;", "")
                i = i.replace(";b&gt;", "")
                i = i.replace(";i&gt;", "")
                i = i.replace(";br /&gt;", "")

                info += i + " "
        if "Lecture" not in info:
            classes.append(info.split("Day")[1][2::])

    for c in classes:
        add_class_to_timeslot(c, unit_name, color)

##
# Takes a parsed string containing the class info and puts it
# into an object and into a timeslot.
def add_class_to_timeslot(c, name, color):
    parts = c.split(" ")
    day = parts[0]
    start = int(parts[3].split(":")[0])
    end = int(parts[6].split(":")[0])
    room = parts[11]

    time_slots[day].append(Prac(name, start, end, room, day, color))

##
# The driver code which is the sequence of calls in order to get the data
# for one unit. Call this once for each unit.
# The sleeps are required to let the page update before we do the next
# action.
def lookup(unit_name, unit_code, color):
    max_tries = 5
    sys.stderr.write("Gathering " + unit_name + ".")
    click_button("criteriaEntry:removeAllButton")
    time.sleep(1)
    search_unit(unit_code)
    time.sleep(1)
    select_unit()
    time.sleep(1)
    click_button("criteriaEntry:addButton")
    time.sleep(1)

    go = True
    tries = 0
    while go and tries < max_tries:
        try:
            tries += 1
            click_button("criteriaEntry:timetableForUnitsButton")
            time.sleep(2)
            parse_html(driver.page_source, unit_name, color)
            go = False
        except:
            if tries == max_tries:
                return False
            sys.stderr.write(".")
            time.sleep(1)

    click_button("timetableByUnits:j_idt134")
    time.sleep(1)
    sys.stderr.write("\n")
    return True

##
# Generates a line of html which corresponds to a table cell.
def generate_line(c):
    line = '<td bgcolor="' + c.color + '"> ' + c.name + "</td>"

    return line

def get_index_of_day(day):
    if day == "Monday":
        idx = 1
    if day == "Tuesday":
        idx = 2
    if day == "Wednesday":
        idx = 3
    if day == "Thursday":
        idx = 4
    if day == "Friday":
        idx = 5

    return idx

##
# Generates the html of a table, this is done per room.
def print_html(room_num):
    md_time_table = '<center> <font size="+3">' + room_num + '</font>\n<hr>'
    classes = []
    times = [str(i) for i in range(8, 22)]

    for t in time_slots.values():
        classes.extend(filter(lambda x: x.room == room_num, t))

    md_time_table += \
    """ 
<table bgcolor="#EEEEEE">
    <tr>
        <th>Time</th>
        <th>Monday</th>
        <th>Tuesday</th>
        <th>Wednesday</th>
        <th>Thursday</th>
        <th>Friday</th>
    </tr>\n"""

    table = {}

    for t in times:
        table[t] = []
        table[t].append('<tr><td bgcolor="white" >' + t + ':00</td>')

        for i in range(5):
            table[t].append(generate_line(Prac("", t, str(int(t) + 1), "", "", "white" )))

    for c in classes:
        idx = get_index_of_day(c.day)

        # This generates the html, does two blocks for a two hour prac.
        table[str(c.start_time_one)][idx] = generate_line(c)
        if c.start_time_two - c.start_time_one > 1:
            table[str(c.start_time_one + 1)][idx] = generate_line(c)

    table_str = ""

    for t in sorted(table.keys(), key=lambda x: int(x)):
        for e in table[t]:
            table_str += e
        table_str += "</tr>"

    md_time_table += table_str
    
    md_time_table += "</table>\n</center>\n"
    return md_time_table

##
# Here you need to specify the unit codes, names and colour to be
# included.
def main():
    url = "http://timetable.student.curtin.edu.au/criteriaEntry.jsf"

    init_timeslots()

    units_data = [
    ("UCP", "COMP1000", "#FC8D75"),
    ("OOPD", "COMP1001", "#92FC75"),
    ("DSA", "COMP1002", "#F4FC5B"),
    ("ACC", "CNCO3002", "#75FCD5"),
    ("SET", "CMPE5000", "#5BA4FC"),
    ("Topics", "COMP5004", "#6C5BFC"),
    ("CG", "COMP2004", "#AC5BFC"),
    ("CCSEP", "ISEC3004", "#ABD8C7"),
    ("IDS", "ISEC3005", "#FAB7D5"),
    ("DM", "COMP3009", "#77C6C8"),
    ("DM", "COMP5009", "#77C6C8"),
    ("DS", "ISYS1001", "#5BFCF7"),
    ("EP", "COMP1004", "#D8D6AB"),
    ("CCSEP", "ISEC4001", "#ABD8C7"),
    ("CCSEP", "ISEC4002", "#ABD8C7"),
    ("SET", "CMPE4001", "#5BA4FC"),
    ("FCS", "COMP1006", "#F3B2F6"),
    ("FOP", "COMP1005", "#9CD304"),
    ("FOP", "COMP5005", "#9CD304"),
    ("HCI", "ICTE3002", "#FCC8C5"),
    ("IDS", "ISEC5001", "#FAB7D5"),
    ("MP", "COMP3007", "#2DFC34"),
    ("OOSE", "COMP2003", "#D2D2D2"),
    ("PTD", "ISEC3002", "#FA08FA"),
    ("PL", "COMP2007", "#FFAA00"),
    ("RE", "CMPE2002", "#FF000F"),
    ("SEC", "COMP3003", "#96C4C9"),
    ("SET", "CMPE3008", "#5BA4FC"),
    ("SCC", "CNCO5002", "#C996C6"),
    ("TFCS", "COMP3002", "#AFB906"),
    ("TFCS", "COMP5001", "#AFB906")
    ]

    known_units = []
    for unit_data in units_data:
        unit = Unit(*unit_data)
        known_units.append(unit)




    sys.stderr.write("Gathering timetable information for " +\
     str(len(units)) + " units. This may take some time.\n\n")

    for u in units:
        done = False
        while not done:
            done = lookup(u[0], u[1], u[2])
            if not done:
                sys.stderr.write("Failed to gather " + u[0] + ", retrying.\n")
                driver.quit()
                driver = None
                driver = webdriver.PhantomJS()
                driver.get(url)

    if driver.session_id != None:
        driver.quit()

    f = open("timetable.html", "w")
    f.write(print_html("314.218"))
    f.write(print_html("314.219"))
    f.write(print_html("314.220"))
    f.write(print_html("314.221"))
    f.write(print_html("314.232"))
    f.close()


if __name__ == '__main__':
    main()
