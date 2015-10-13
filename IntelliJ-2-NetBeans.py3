#!/usr/bin/env python3
import os
import shutil
from time import sleep

## Controlli preliminari
global jarExists
jarExists = False
def controlliPreliminari():
    # Controllo directory corrente
    if not (os.path.exists("src")) or not (os.path.exists(nomeProgetto+".iml")):
        print("\n[ERR] La directory corrente non coincide col progetto specificato.")
        quit(1)
    # Esistenza artefatto JAR
    if (os.path.exists("out")):
        if (os.path.exists("out/artifacts")):
            jarDir = os.listdir("out/artifacts")
            if (len(jarDir) > 0):
                jarFile = os.listdir("out/artifacts/"+jarDir[0])
                if (len(jarFile) > 0):
                    global jarExists
                    jarExists = True

## Creazione progetto NetBeans
# Generazione albero
def generaDirectory():
    print("\n* Creo la struttura delle directory...\r", end='')
    os.mkdir("netbeaned")
    os.mkdir("netbeaned/build")
    os.mkdir("netbeaned/dist")
    os.mkdir("netbeaned/nbproject")
    os.mkdir("netbeaned/nbproject/private") # ?
    sleep(0.25)
    print("* Creo la struttura delle directory   \t\t[OK]")

# Generazione file
def generaFile():
    print("* Creo i file del progetto...")
    print("     * Genero project.properties...\r", end='')
    projectProperties = open("netbeaned/nbproject/project.properties", 'w')
    projectProperties.write("""annotation.processing.enabled=true
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
dist.jar=${dist.dir}/"""+nomeProgetto+""".jar
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
main.class="""+classeAvvio+"""
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
    projectProperties.close()
    sleep(0.25)
    print("     * Genero project.properties   \t\t[OK]")

    print("     * Genero project.xml...\r", end='')
    projectXml = open("netbeaned/nbproject/project.xml", 'w')
    projectXml.write("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://www.netbeans.org/ns/project/1">
    <type>org.netbeans.modules.java.j2seproject</type>
    <configuration>
        <data xmlns="http://www.netbeans.org/ns/j2se-project/3">
            <name>"""+nomeProgetto+"""</name>
            <source-roots>
                <root id="src.dir"/>
            </source-roots>
            <test-roots>
                <root id="test.src.dir"/>
            </test-roots>
        </data>
    </configuration>
</project>""")
    projectXml.close()
    sleep(0.25)
    print("     * Genero project.xml   \t\t\t[OK]")

    print("     * Genero build.xml...\r", end='')
    buildXml = open("netbeaned/build.xml", 'w')
    buildXml.write('''<?xml version="1.0" encoding="UTF-8"?>
<project name="'''+nomeProgetto+'''" default="default" basedir=".">
    <description>Builds, tests, and runs the project'''+nomeProgetto+'''.</description>
    <import file="nbproject/build-impl.xml"/>
</project>''')
    buildXml.close()
    sleep(0.25)
    print("     * Genero build.xml   \t\t\t[OK]")

    print("     * Genero manifest.mf...\r", end='')
    manifestMf = open("netbeaned/manifest.mf", 'w')
    manifestMf.write("""Manifest-Version: 1.0
X-COMMENT: Main-Class will be added automatically by build""")
    manifestMf.close()
    sleep(0.25)
    print("     * Genero manifest.mf   \t\t\t[OK]")

    print("     * Genero build-impl.xml...\r", end='')
    shutil.copy(os.path.dirname(os.path.realpath(__file__))+"/build-impl.xml", "netbeaned/nbproject")
    with open("netbeaned/nbproject/build-impl.xml.new", 'wt') as buildOut:
        with open("netbeaned/nbproject/build-impl.xml", 'rt') as buildIn:
            for line in buildIn:
                buildOut.write(line.replace("netbeans_test", nomeProgetto))
    os.remove("netbeaned/nbproject/build-impl.xml")
    os.rename("netbeaned/nbproject/build-impl.xml.new", "netbeaned/nbproject/build-impl.xml")
    sleep(0.25)
    print("     * Genero build-impl.xml   \t\t\t[OK]")

# Copia del sorgente
def copiaSorgente():
    print("* Copio il sorgente Java...\r", end='')
    shutil.copytree("src", "netbeaned/src")
    sleep(0.25)
    print("* Copio il sorgente Java   \t\t\t[OK]")

# Copia JAR
def copiaJAR():
    print("* Copio l'artefatto JAR...\r", end='')
    jarDir = os.listdir("out/artifacts")
    jarFile = os.listdir("out/artifacts/"+jarDir[0])
    shutil.copy2('out/artifacts/'+jarDir[0]+'/'+jarFile[0], 'netbeaned/dist')
    sleep(0.25)
    print("* Copio l'artefatto JAR   \t\t\t[OK]")

# Swap di cartelle
def copiaCartelle():
    print("* Rinomino la cartella del progetto...\r", end='')
    os.rename("netbeaned", nomeProgetto+"_netbeaned")
    sleep(0.25)
    print("* Rinomino la cartella del progetto   \t\t[OK]")

def generaProgetto():
    generaDirectory()
    generaFile()

def copiaProgetto():
    copiaSorgente()
    if (jarExists):
        copiaJAR()
    copiaCartelle()


foo, nomeProgetto = os.path.split(os.getcwd())
nomeProgettoInput = input(">>> Nome del progetto ["+nomeProgetto+"]: ")
if nomeProgettoInput.strip():
    nomeProgetto = nomeProgettoInput

classeAvvio = ""
if (os.path.exists("src/META-INF/MANIFEST.MF")):
    for line in open("src/META-INF/MANIFEST.MF"):
        if "Main-Class:" in line:
            classeAvvio = line.replace("Main-Class: ", "").strip()
classeAvvioInput = input(">>> Classe di avvio ["+classeAvvio+"]: ")
if classeAvvioInput.strip():
    classeAvvio = classeAvvioInput
if not classeAvvio.strip():
    print("\n[ERR] La classe di avvio deve essere specificata.")
    quit(1)

controlliPreliminari()
generaProgetto()
copiaProgetto()

print("\n* Conversione completata!")
