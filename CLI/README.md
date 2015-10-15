IntelliJ-2-NetBeans
===================
A simple Python script to convert an IntelliJ IDEA project to a NetBeans one.

Installation
------------
Grab the *Jinja* templating engine Python3 module (install it using ```pip install jinja2```).

Usage
-----
Open up a terminal and navigate to your IntelliJ IDEA project folder, then run this script from wherever you cloned the repo. It does not need to be in the project folder.

The script will ask for the project's name and main class - the names between the squared brackets are the ones that it deducted by itself, looking at the source tree and at the project's manifest; write nothing and press enter to use them.

A folder named ```<YourProjectName>_IntelliJ-2-NetBeans``` will be created, containing your new NetBeans project. The script will generate the needed files and copy over your source code and JAR artifacts.  
