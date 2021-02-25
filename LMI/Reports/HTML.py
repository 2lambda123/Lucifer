import os
import time


class HTMLTable:
    def __init__(self, parent):
        self.parent = parent
        self.tableID = "lucTab"

    def __enter__(self):
        self.parent.currentHtml += '<table style="width:100%" class="' + self.tableID + '">\n'
        return self.parent

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parent.currentHtml += '</table>\n<br/><br/>'

    def __call__(self, tableID):
        self.tableID = tableID
        return self


class HTMLReport:
    def __init__(self, name=str(time.time()), path="./reports/"):
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        self.name = name if name.lower().endswith(".html") else (name + ".html")
        self.fullPath = os.path.abspath(os.path.join(path, self.name))
        self.fileHTML = ""
        self.currentHtml = ""
        self.useTable = HTMLTable(self)
        self.defaultReportStyle = """.lucTab {
            background: #ffffff;
        }
    .lucTab tr:nth-child(even) {
      background-color: #eee;
    }
    
    .lucTab tr:nth-child(odd) {
      background-color: #fff;
    }
    .lucTab th {
      color: white;
      background-color: black;
    }
    
    .lucTab caption {
      text-align: center;
      border: 2px solid #cccccc;
      margin-bottom: -0.2%;
      font-size: 180%;
      padding: 5px;
      letter-spacing: 2px;
      font-weight: bold;
      background: #ffffff;
    }
    
    .lucTitle {
        font-size: 100%;
        font-weight: bold;
        color: white;
        border: 3px solid black;
        background: darkred;
        padding: 0em 1.5em;
        border-radius: 10px;
        line-height: 1em;
        width: 50%;
        margin: 0;
    }
    
    .lucTitleCap {
       text-align: center;
       color: black;
       font-size: 0.75em;
       background: lightblue;
       border: 3px solid black;
       border-radius: 10px;
       width: 30em;
    }
    
    .accordion {
      background-color: #eee;
      color: #444;
      cursor: pointer;
      padding: 18px;
      width: 100%;
      border: none;
      text-align: left;
      outline: none;
      font-size: 15px;
      transition: 0.4s;
    }
    
    .active, .accordion:hover {
      background-color: #ccc;
    }
    
    .accordion:after {
      content: '\\002B';
      color: #777;
      font-weight: bold;
      float: right;
      margin-left: 5px;
    }
    
    .active:after {
      content: "\\2212";
    }
    
    .panel {
      padding: 0 18px;
      background: #E3CD81;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.2s ease-out;
    }
    
    body {
        background: #E3CD81;
    }
"""
        self.defaultReportScript = """
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}
"""

    def newReport(self, name):
        self.path = os.path.abspath(self.path)
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)
        self.name = name if name.lower().endswith(".html") else (name + ".html")
        self.fullPath = os.path.abspath(os.path.join(self.path, self.name))
        self.fileHTML = ""
        self.loadFile()

    def loadFile(self):
        if not os.path.exists(self.fullPath):
            self.createNewReport(self.fullPath)
        with open(self.fullPath, "r") as file:
            self.fileHTML = file.read()
        self.removeStyle()

    def createNewReport(self, path):
        os.makedirs((os.sep.join(path.split(os.sep)[:-1]) + os.sep), exist_ok=True)
        with open(path, "a+") as f:
            f.write(
                """<div class="lucTitle">
  <h1>
    Lucifer Report
  </h1>
  <p class="lucTitleCap"> Autogenerated by the Lucifer tool, created by Skiller9090 </p>
</div>\n"""
            )
            f.write("\n\n<style>\n" + self.defaultReportStyle + "</style>\n")

    def saveFile(self):
        if not os.path.exists(self.fullPath):
            self.createNewReport(self.fullPath)
        with open(self.fullPath, "w") as f:
            f.write((self.fileHTML +
                     ("\n\n<style>\n" + self.defaultReportStyle + "</style>\n") +
                     "\n<script>" + self.defaultReportScript + "</script>\n"))

    def removeStyle(self):
        if "<style>" in self.fileHTML:
            self.fileHTML = self.fileHTML[:self.fileHTML.index("<style>")]

    def addTable(self, data):
        title = data[0]
        array2d = data[1]
        headings = array2d.pop(0)
        self.currentHtml = ""
        self.currentHtml += "<button class='accordion'> " + str(title) + " </button>"
        self.currentHtml += "<div class='panel'>\n"
        with self.useTable("lucTab") as _:
            if title != "":
                self.currentHtml += "<caption class='collapsible'>" + str(title) + "</caption>\n"
            self.currentHtml += "<tr>\n"
            if headings:
                for head in headings:
                    self.currentHtml += "<th>" + str(head) + "</th>\n"
            self.currentHtml += "</tr>\n"
            for rowValues in array2d:
                self.currentHtml += "<tr>\n"
                for value in rowValues:
                    self.currentHtml += "<td>" + str(value) + "</td>\n"
                self.currentHtml += "</tr>\n"
        self.currentHtml += "</div>\n"
        self.fileHTML += "\n\n" + self.currentHtml
        self.saveFile()
