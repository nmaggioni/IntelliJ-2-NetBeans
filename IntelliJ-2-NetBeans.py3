#!/usr/bin/env python3
import os
import shutil
from time import sleep
from jinja2 import Template

jarExists = False


# Preliminar checks
def check():
    # Current directory
    if not (os.path.exists("src")) or not (os.path.exists(projectName + ".iml")):
        print("\n[ERR] The current directory is not compatible with the specified project name.")
        quit(1)
    # Existing directories
    if os.path.exists("IntelliJ-2-NetBeans"):
        print("\n[ERR] The conversion temporary folder (IntelliJ-2-NetBeans) already exists.")
        quit(1)
    if os.path.exists(projectName + "_IntelliJ-2-NetBeans"):
        print("\n[ERR] The converted project folder ("+ projectName + "_IntelliJ-2-NetBeans) already exists.")
        quit(1)
    # JAR artifact existence
    if os.path.exists("out"):
        if os.path.exists("out/artifacts"):
            jar_dir = os.listdir("out/artifacts")
            if len(jar_dir) > 0:
                jar_file = os.listdir("out/artifacts/" + jar_dir[0])
                if len(jar_file) > 0:
                    global jarExists
                    jarExists = True


# Directory tree generation
def generate_directories():
    print("\n* Generating directory structure...\r", end='')
    os.mkdir("IntelliJ-2-NetBeans")
    os.mkdir("IntelliJ-2-NetBeans/build")
    os.mkdir("IntelliJ-2-NetBeans/dist")
    os.mkdir("IntelliJ-2-NetBeans/nbproject")
    os.mkdir("IntelliJ-2-NetBeans/nbproject/private")
    sleep(0.25)
    print("* Generating directory structure   \t\t[OK]")


# Project files generation
def generate_files():
    print("* Creating project files...")
    print("     * Generating project.properties...\r", end='')
    template = Template(open(os.path.dirname(os.path.realpath(__file__)) + "/res/project.properties").read())
    project_properties = open("IntelliJ-2-NetBeans/nbproject/project.properties", 'w')
    project_properties.write(template.render(projectName=projectName, mainClass=mainClass))
    project_properties.close()
    sleep(0.25)
    print("     * Generating project.properties   \t\t[OK]")

    print("     * Generating project.xml...\r", end='')
    template = Template(open(os.path.dirname(os.path.realpath(__file__)) + "/res/project.xml").read())
    project_xml = open("IntelliJ-2-NetBeans/nbproject/project.xml", 'w')
    project_xml.write(template.render(projectName=projectName))
    project_xml.close()
    sleep(0.25)
    print("     * Generating project.xml   \t\t[OK]")

    print("     * Generating build.xml...\r", end='')
    template = Template(open(os.path.dirname(os.path.realpath(__file__)) + "/res/build.xml").read())
    build_xml = open("IntelliJ-2-NetBeans/build.xml", 'w')
    build_xml.write(template.render(projectName=projectName))
    build_xml.close()
    sleep(0.25)
    print("     * Generating build.xml   \t\t\t[OK]")

    print("     * Copying manifest.mf...\r", end='')
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + "/res/manifest.mf", "IntelliJ-2-NetBeans/manifest.mf")
    sleep(0.25)
    print("     * Copying manifest.mf   \t\t\t[OK]")

    print("     * Generating build-impl.xml...\r", end='')
    template = Template(open(os.path.dirname(os.path.realpath(__file__)) + "/res/build-impl.xml").read())
    build_impl_xml = open("IntelliJ-2-NetBeans/nbproject/build-impl.xml", 'w')
    build_impl_xml.write(template.render(projectName=projectName))
    build_impl_xml.close()
    sleep(0.25)
    print("     * Generating build-impl.xml   \t\t[OK]")


# Source code copy
def copy_source_code():
    print("* Copying Java source code...\r", end='')
    shutil.copytree("src", "IntelliJ-2-NetBeans/src")
    sleep(0.25)
    print("* Copying Java source code   \t\t\t[OK]")


# JAR copy
def copy_jar_file():
    print("* Copying JAR artifact...\r", end='')
    jar_dir = os.listdir("out/artifacts")
    jar_file = os.listdir("out/artifacts/" + jar_dir[0])
    shutil.copy2('out/artifacts/' + jar_dir[0] + '/' + jar_file[0], 'IntelliJ-2-NetBeans/dist')
    sleep(0.25)
    print("* Copying JAR artifact   \t\t\t[OK]")


# Folder renaming
def rename_project_folder():
    print("* Renaming the project folder...\r", end='')
    os.rename("IntelliJ-2-NetBeans", projectName + "_IntelliJ-2-NetBeans")
    sleep(0.25)
    print("* Renaming the project folder   \t\t[OK]")


def configure():
    generate_directories()
    generate_files()


def make():
    copy_source_code()
    if jarExists:
        copy_jar_file()
    rename_project_folder()


print("""
    ╦┌┐┌┌┬┐┌─┐┬  ┬  ┬ ╦       ╔╗╔┌─┐┌┬┐╔╗ ┌─┐┌─┐┌┐┌┌─┐
    ║│││ │ ├┤ │  │  │ ║── 2 ──║║║├┤  │ ╠╩╗├┤ ├─┤│││└─┐
    ╩┘└┘ ┴ └─┘┴─┘┴─┘┴╚╝       ╝╚╝└─┘ ┴ ╚═╝└─┘┴ ┴┘└┘└─┘
""")

foo, projectName = os.path.split(os.getcwd())
projectNameInput = input(">>> Project name [" + projectName + "]: ")
if projectNameInput.strip():
    projectName = projectNameInput

mainClass = ""
if os.path.exists("src/META-INF/MANIFEST.MF"):
    for line in open("src/META-INF/MANIFEST.MF"):
        if "Main-Class:" in line:
            mainClass = line.replace("Main-Class: ", "").strip()
mainClassInput = input(">>> Main class [" + mainClass + "]: ")
if mainClassInput.strip():
    mainClass = mainClassInput
if not mainClass.strip():
    print("\n[ERR] You must specify a main class.")
    quit(1)

check()
configure()
make()

print("\n* Conversion complete!")
