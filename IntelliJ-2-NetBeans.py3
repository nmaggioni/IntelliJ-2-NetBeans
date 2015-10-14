#!/usr/bin/env python3
import os
import shutil
from time import sleep

jarExists = False


# Preliminar checks
def check():
    # Current directory check
    if not (os.path.exists("src")) or not (os.path.exists(projectName + ".iml")):
        print("\n[ERR] The current directory is not compatible with the specified project name.")
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
    project_properties = open("IntelliJ-2-NetBeans/nbproject/project.properties", 'w')
    project_properties.write("""annotation.processing.enabled=true
annotation.processing.enabled.in.editor=false
annotation.processing.processor.options=
annotation.processing.processors.list=
annotation.processing.run.all.processors=true
annotation.processing.source.output=${build.generated.sources.dir}/ap-source-output
build.classes.dir=${build.dir}/classes
build.classes.excludes=**/*.java,**/*.form
# This directory is removed when the project is cleaned:
build.dir=build
build.generated.dir=${build.dir}/generated
build.generated.sources.dir=${build.dir}/generated-sources
# Only compile against the classpath explicitly listed here:
build.sysclasspath=ignore
build.test.classes.dir=${build.dir}/test/classes
build.test.results.dir=${build.dir}/test/results
# Uncomment to specify the preferred debugger connection transport:
#debug.transport=dt_socket
debug.classpath=\
    ${run.classpath}
debug.test.classpath=\
    ${run.test.classpath}
# Files in build.classes.dir which should be excluded from distribution jar
dist.archive.excludes=
# This directory is removed when the project is cleaned:
dist.dir=dist
dist.jar=${dist.dir}/""" + projectName + """.jar
dist.javadoc.dir=${dist.dir}/javadoc
excludes=
includes=**
jar.compress=false
javac.classpath=
# Space-separated list of extra javac options
javac.compilerargs=
javac.deprecation=false
javac.processorpath=\
    ${javac.classpath}
javac.source=1.8
javac.target=1.8
javac.test.classpath=\
    ${javac.classpath}:\
    ${build.classes.dir}
javac.test.processorpath=\
    ${javac.test.classpath}
javadoc.additionalparam=
javadoc.author=false
javadoc.encoding=${source.encoding}
javadoc.noindex=false
javadoc.nonavbar=false
javadoc.notree=false
javadoc.private=false
javadoc.splitindex=true
javadoc.use=true
javadoc.version=false
javadoc.windowtitle=
main.class=""" + mainClass + """
manifest.file=manifest.mf
meta.inf.dir=${src.dir}/META-INF
mkdist.disabled=false
platform.active=default_platform
run.classpath=\
    ${javac.classpath}:\
    ${build.classes.dir}
# Space-separated list of JVM arguments used when running the project.
# You may also define separate properties like run-sys-prop.name=value instead of -Dname=value.
# To set system properties for unit tests define test-sys-prop.name=value:
run.jvmargs=
run.test.classpath=\
    ${javac.test.classpath}:\
    ${build.test.classes.dir}
source.encoding=UTF-8
src.dir=src
test.src.dir=test""")
    project_properties.close()
    sleep(0.25)
    print("     * Generating project.properties   \t\t[OK]")

    print("     * Generating project.xml...\r", end='')
    project_xml = open("IntelliJ-2-NetBeans/nbproject/project.xml", 'w')
    project_xml.write("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://www.netbeans.org/ns/project/1">
    <type>org.netbeans.modules.java.j2seproject</type>
    <configuration>
        <data xmlns="http://www.netbeans.org/ns/j2se-project/3">
            <name>""" + projectName + """</name>
            <source-roots>
                <root id="src.dir"/>
            </source-roots>
            <test-roots>
                <root id="test.src.dir"/>
            </test-roots>
        </data>
    </configuration>
</project>""")
    project_xml.close()
    sleep(0.25)
    print("     * Generating project.xml   \t\t[OK]")

    print("     * Generating build.xml...\r", end='')
    build_xml = open("IntelliJ-2-NetBeans/build.xml", 'w')
    build_xml.write('''<?xml version="1.0" encoding="UTF-8"?>
<project name="''' + projectName + '''" default="default" basedir=".">
    <description>Builds, tests, and runs the project''' + projectName + '''.</description>
    <import file="nbproject/build-impl.xml"/>
</project>''')
    build_xml.close()
    sleep(0.25)
    print("     * Generating build.xml   \t\t\t[OK]")

    print("     * Generating manifest.mf...\r", end='')
    manifest_mf = open("IntelliJ-2-NetBeans/manifest.mf", 'w')
    manifest_mf.write("""Manifest-Version: 1.0
X-COMMENT: Main-Class will be added automatically by build""")
    manifest_mf.close()
    sleep(0.25)
    print("     * Generating manifest.mf   \t\t[OK]")

    print("     * Generating build-impl.xml...\r", end='')
    shutil.copy(os.path.dirname(os.path.realpath(__file__)) + "/build-impl.xml", "IntelliJ-2-NetBeans/nbproject")
    with open("IntelliJ-2-NetBeans/nbproject/build-impl.xml.new", 'wt') as buildOut:
        with open("IntelliJ-2-NetBeans/nbproject/build-impl.xml", 'rt') as buildIn:
            for buildIn_line in buildIn:
                buildOut.write(buildIn_line.replace("netbeans_test", projectName))
    os.remove("IntelliJ-2-NetBeans/nbproject/build-impl.xml")
    os.rename("IntelliJ-2-NetBeans/nbproject/build-impl.xml.new", "IntelliJ-2-NetBeans/nbproject/build-impl.xml")
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
