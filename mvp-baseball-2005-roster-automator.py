import datetime
import sys
import time
import urllib2
from HTMLParser import HTMLParser
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

# Utility
class WebPage(QWebPage):
    m_url = ""
    
    def __init__(self, url):
        self.m_url = url
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished[bool].connect(self.execute)
        self.mainFrame().load(QUrl(self.m_url))
        self.app.exec_()

    def execute(self):
        self.app.quit()

    def read(self):
        return self.mainFrame().toHtml().encode("utf-8")

class Url:
    m_url = ""
    
    def __init__(self, url):
        self.m_url = url

    def toHtml(self, javascript):
        if javascript is True:
            webPage = WebPage(self.m_url)
            webPageSource = webPage.read()
            return webPageSource            
        else:
            webPage = urllib2.urlopen(self.m_url)
            webPageSource = webPage.read()
            return webPageSource

# Parsing    
class MLBRosterParser(HTMLParser):
    b_table = 0
    b_tbody = 0
    b_tr = 0
    b_td = 0
    b_a = 0
    i_td = 0
    n_p = 0
    b_td_data = 0
    
    def __init__(self, abbreviation, export_file):
        HTMLParser.__init__(self)
        self.m_abbreviation = abbreviation
        self.m_write_file = export_file
        
    def handle_starttag(self, tag, attrs):
        if self.b_td == 1:
            if tag == "a":
                self.b_a = 1
        if self.b_tr == 1:
            if tag == "td":
                self.b_td = 1
                self.i_td = self.i_td + 1
                self.b_td_data = 0
        if self.b_tbody == 1:
            if tag == "tr":
                self.b_tr = 1
        if self.b_table == 1:
            if tag == "tbody":
                self.b_tbody = 1
        if tag == "table":
            for attr in attrs:
                if attr[0] == "class":
                    if attr[1] == "team_table_results":
                        self.b_table = 1
    def handle_endtag(self, tag):
        if tag == "a":
            self.b_a = 0
        if tag == "td":
            if self.b_td_data != 1:
                if self.b_td == 1:
                    if self.i_td == 1:
                        self.n_p = self.n_p + 1
                        self.m_write_file.write(self.m_abbreviation[1] + ", " + self.m_abbreviation[2] + ", " + "0" + ", ")
            self.b_td = 0
            self.b_td_data = 0
        if tag == "tr":
            self.b_tr = 0
            self.i_td = 0
        if tag == "tbody":
            self.b_tbody = 0
        if tag == "table":
            self.b_table = 0
    def handle_data(self, data):
        if self.b_a == 1:
            if self.i_td == 2:
                i_space = 0
                for i in range(len(data)):
                    if data[i] == " ":
                        i_space = i
                        break
                i_space_plus = i_space + 1
                first_name = data[:i_space]
                last_name = data[i_space_plus:]
                self.m_write_file.write(first_name + ", ")
                self.m_write_file.write(last_name + ", ")
        if self.b_td == 1:
            if self.i_td == 1:
                self.n_p = self.n_p + 1
                self.m_write_file.write(self.m_abbreviation[1] + ", " + self.m_abbreviation[2] + ", " + data + ", ")
            if self.i_td == 3:
                data_split = data.split("-")
                for data_item in data_split:
                    self.m_write_file.write(data_item + ", ")
            if self.i_td == 4:
                i_double_quote = len(data) - 1
                height = data[:i_double_quote]
                height_split = height.split("'")
                feet = height_split[0]
                inches = height_split[1]
                feet_int = int(feet)
                inches_int = int(inches)
                feet_int = feet_int * 12
                height_int = feet_int + inches_int
                height_str = str(height_int)
                self.m_write_file.write(height_str + ", ")
            if self.i_td == 5:
                self.m_write_file.write(data + ", ")
            if self.i_td == 6:
                #Birthday, days from December 31, 1947
                birthday = data
                birthday_split = birthday.split(", ")
                month_day = birthday_split[0]
                month_day_split = month_day.split()
                month = month_day_split[0]
                day = month_day_split[1]
                year = birthday_split[1]
                month_int = 1
                if month == "Jan":
                    month_int = 1
                elif month == "Feb":
                    month_int = 2
                elif month == "Mar":
                    month_int = 3
                elif month == "Apr":
                    month_int = 4
                elif month == "May":
                    month_int = 5
                elif month == "Jun":
                    month_int = 6
                elif month == "Jul":
                    month_int = 7
                elif month == "Aug":
                    month_int = 8
                elif month == "Sep":
                    month_int = 9
                elif month == "Oct":
                    month_int = 10
                elif month == "Nov":
                    month_int = 11
                elif month == "Dec":
                    month_int = 12
                day_int = int(day)
                year_int = int(year)
                from_date = datetime.date(1947, 12, 31)
                to_date = datetime.date(year_int, month_int, day_int)
                diff_date = to_date - from_date
                diff_days = diff_date.days
                days_str = str(diff_days)
                self.m_write_file.write(days_str + "\n")
        self.b_td_data = 1

# Example
def example():
    url = 'http://www.github.com'
    urlObject = Url(url)
    htmlWithJavascript = urlObject.toHtml(True)
    htmlWithJavascriptFile = open('htmlWithJavascript.txt', 'w')
    htmlWithJavascriptFile.write(htmlWithJavascript)    
    htmlWithoutJavascript = urlObject.toHtml(False)
    htmlWithoutJavascriptFile = open('htmlWithoutJavascript.txt', 'w')
    htmlWithoutJavascriptFile.write(htmlWithoutJavascript)

def exampleMLBRosterParser():
    abbreviations = [["atl", "Atlanta", "Braves"],
                     ["ari", "Arizona", "Diamondbacks"],
                     ["bal", "Baltimore", "Orioles"],
                     ["bos", "Boston", "Red Sox"],
                     ["chc", "Chicago", "Cubs"],
                     ["cws", "Chicago", "White Sox"],
                     ["cin", "Cinncinnati", "Reds"],
                     ["cle", "Cleveland", "Indians"],
                     ["col", "Colorado", "Rockies"],
                     ["det", "Detroit", "Tigers"],
                     ["hou", "Houston", "Astros"],
                     ["kc", "Kansas City", "Royals"],
                     ["ana", "Los Angeles", "Angels"],
                     ["la", "Los Angeles", "Dodgers"],
                     ["mia", "Miami", "Marlins"],
                     ["mil", "Milwaukee", "Brewers"],
                     ["min", "Minnesota", "Twins"],
                     ["nym", "New York", "Mets"],
                     ["nyy", "New York", "Yankees"],
                     ["oak", "Oakland", "Athletics"],
                     ["phi", "Philadelphia", "Phillies"],
                     ["pit", "Pittsburgh", "Pirates"],
                     ["sd", "San Diego", "Padres"],
                     ["sf", "San Francisco", "Giants"],
                     ["sea", "Seattle", "Mariners"],
                     ["tb", "Tampa Bay", "Rays"],
                     ["tex", "Texas", "Rangers"],
                     ["stl", "St. Louis", "Cardinals"],
                     ["tor", "Toronto", "Blue Jays"],
                     ["was", "Washington", "Nationals"]]

    exampleFilename = "example.txt"
    exampleFile = open(exampleFilename, 'w')
    
    for abbreviation in abbreviations:
        url = "http://mlb.com/team/roster_active.jsp?c_id=" + abbreviation[0]
        urlObject = Url(url)
        webPageSource = urlObject.toHtml(False)
        webPageSource = webPageSource.replace("&#039;", "'")
        parser = MLBRosterParser(abbreviation, exampleFile)
        parser.feed(webPageSource)

# Main 
def main(argc, argv):
    example()
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
