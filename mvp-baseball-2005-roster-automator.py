import sys
import urllib2
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

# Main 
def main(argc, argv):
    example()
    return 0

if __name__ == "__main__":
    sys.exit(main(len(sys.argv), sys.argv))
