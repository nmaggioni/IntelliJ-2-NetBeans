IntelliJ-2-NetBeans
===================
A Java GUI to convert an IntelliJ IDEA project to a NetBeans one. Designed with Swing.

[![Codacy Badge](https://api.codacy.com/project/badge/10a7e4194f82425688575eb6ece0a615)](https://www.codacy.com/app/nmaggioni/IntelliJ-2-NetBeans)

Usage
-----
+ Set up a [JAR][1] as per [IntelliJ IDEA documentation][2] (a more visual guide can be found [here][3]).
+ Issue ```java -jar /path/to/IntelliJ-2-NetBeans.jar``` from a command line or double click the JAR file if your OS supports it.
+ Specify the project's folder and click the **Convert** button.

A folder named ```<YourProjectName>_IntelliJ-2-NetBeans``` will be created in your project folder, containing your new NetBeans project. The program will generate the needed files and copy over your source code and JAR artifacts.  

[1]: https://www.jetbrains.com/idea/help/create-jar-from-modules-dialog.html
[2]: https://www.jetbrains.com/idea/help/configuring-artifacts.html
[3]: https://blog.jetbrains.com/idea/2010/08/quickly-create-jar-artifact/
