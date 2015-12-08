package nmaggioni.intellij2netbeans;

import org.apache.commons.io.FileUtils;

import javax.swing.*;
import java.io.*;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

class Converter {
    private final JProgressBar progressBar;
    private float progressBarCompletion = 0f;

    private final String projectPath;
    private final String projectName;
    private String mainClassName;
    private boolean jarExists = false;
    private String jarFilename;

    public Converter(String projectPath, JProgressBar progressBar) {
        this.projectPath = projectPath;
        this.progressBar = progressBar;
        projectName = new File(projectPath).getName();
    }

    private void getMainClassName() throws MissingMainClassException, IOException {
        File manifest = new File(projectPath + "/src/META-INF/MANIFEST.MF");
        if (!manifest.exists() || !manifest.isFile()) {
            throw new MissingMainClassException();
        } else {
            BufferedReader br;
            try {
                br = new BufferedReader(new FileReader(manifest));
                String line;
                while ((line = br.readLine()) != null) {
                    if (line.startsWith("Main-Class:")) {
                        mainClassName = line.replace("Main-Class: ", "").trim();
                        br.close();
                        return;
                    }
                }
                br.close();
            } catch (FileNotFoundException e) {
                throw new MissingMainClassException();
            }
        }
        throw new MissingMainClassException();
    }

    public void convertProject() throws IOException, URISyntaxException,
            DirectoryCreationException, MissingFileException, ExistingDirectoryException,
            BadPathException, MissingMainClassException, MissingDirectoryException {
        preliminaryChecks();
        advanceProgressbar(progressBar);
        createProjectTree();
        advanceProgressbar(progressBar);
        createProjectFiles();
        advanceProgressbar(progressBar);
        copySourceCode();
        advanceProgressbar(progressBar);
        if (jarExists) copyJar();
        advanceProgressbar(progressBar);
        renameProjectFolder();
        advanceProgressbar(progressBar, true);
    }

    private void advanceProgressbar(JProgressBar progressBar) {
        advanceProgressbar(progressBar, false);
    }

    private void advanceProgressbar(JProgressBar progressBar, boolean toMax) {
        if (toMax) {
            progressBarCompletion = 100;
        } else {
            progressBarCompletion += 100 / 6;
        }
        progressBar.setValue((int) progressBarCompletion);
    }

    private void preliminaryChecks() throws ExistingDirectoryException, MissingFileException,
            BadPathException, IOException, MissingMainClassException, MissingDirectoryException {
        // 'src' directory check
        File dir = new File(projectPath + "/src");
        if (!dir.exists() || !dir.isDirectory()) {
            throw new MissingDirectoryException("src");
        }

        // '*.iml' file check
        ExtensionFilter imlFilter = new ExtensionFilter("iml");
        dir = new File(projectPath + "/");
        if (!dir.isDirectory()) {
            throw new BadPathException(projectPath + "/");
        }
        String[] imlList = dir.list(imlFilter);
        if (imlList.length == 0) {
            throw new MissingFileException("iml");
        }

        // 'IntelliJ-2-NetBeans' directory check
        dir = new File(projectPath + "/IntelliJ-2-NetBeans");
        if (dir.exists() && dir.isDirectory()) {
            throw new ExistingDirectoryException("IntelliJ-2-NetBeans");
        }

        // 'PROJECTNAME_IntelliJ-2-NetBeans' directory check
        dir = new File(projectPath + "/" + projectName + "_IntelliJ-2-NetBeans");
        if (dir.exists() && dir.isDirectory()) {
            throw new ExistingDirectoryException(projectName + "_IntelliJ-2-NetBeans");
        }

        // Project manifest existence check
        getMainClassName();

        // Detect JAR existence
        detectJar();
    }

    private void detectJar() {
        File dir = new File(projectPath + "/out/artifacts/" + projectPath.replace(" ", "_") + "_jar/");
        if (dir.exists() && dir.isDirectory()) {
            ExtensionFilter jarFilter = new ExtensionFilter("jar");
            String[] jarList = dir.list(jarFilter);
            if (jarList.length > 0) {
                jarExists = true;
                jarFilename = jarList[0];  // meh
            }
        } else {
            jarExists = false;
        }
    }

    private void createProjectTree() throws DirectoryCreationException {
        List<String> directories = new ArrayList<>();
        directories.add("IntelliJ-2-NetBeans");
        directories.add("IntelliJ-2-NetBeans/build");
        directories.add("IntelliJ-2-NetBeans/dist");
        directories.add("IntelliJ-2-NetBeans/test");
        directories.add("IntelliJ-2-NetBeans/nbproject");
        directories.add("IntelliJ-2-NetBeans/nbproject/private");
        boolean success;
        for (String directory : directories) {
            success = (new File(projectPath + "/" + directory)).mkdir();
            if (!success) throw new DirectoryCreationException(projectPath + "/" + directory);
        }
    }

    private void createProjectFiles() throws URISyntaxException, IOException, MissingFileException {
        String jarFileFolder = new File(getClass().getProtectionDomain().getCodeSource().getLocation().toURI()).getParent();

        String file = jarFileFolder + "/res/build.xml";
        replaceTagsAndCopy(new File(file.substring(file.indexOf(":") + 1)),
                new File(projectPath + "/IntelliJ-2-NetBeans/build.xml"));

        file = jarFileFolder + "/res/manifest.mf";
        FileUtils.copyFile(new File(file.substring(file.indexOf("/file:") + 1)),
                new File(projectPath + "/IntelliJ-2-NetBeans/manifest.mf"));

        file = jarFileFolder + "/res/build-impl.xml";
        replaceTagsAndCopy(new File(file.substring(file.indexOf("/file:") + 1)),
                new File(projectPath + "/IntelliJ-2-NetBeans/nbproject/build-impl.xml"));

        file = jarFileFolder + "/res/project.xml";
        replaceTagsAndCopy(new File(file.substring(file.indexOf("/file:") + 1)),
                new File(projectPath + "/IntelliJ-2-NetBeans/nbproject/project.xml"));

        file = jarFileFolder + "/res/project.properties";
        replaceTagsAndCopy(new File(file.substring(file.indexOf("/file:") + 1)),
                new File(projectPath + "/IntelliJ-2-NetBeans/nbproject/project.properties"));
    }

    private void copySourceCode() throws IOException {
        FileUtils.copyDirectory(new File(projectPath + "/src"), new File(projectPath + "/IntelliJ-2-NetBeans/src"));
    }

    private void copyJar() throws IOException {
        FileUtils.copyFile(new File(projectPath + "/out/artifacts/" + jarFilename),
                new File(projectPath + "/IntelliJ-2-NetBeans/dist/" + jarFilename));
    }

    private void replaceTagsAndCopy(File in, File out) throws MissingFileException, IOException {
        if (!in.exists() || !in.isFile()) {
            throw new MissingFileException(in.getAbsolutePath());
        } else {
            String content = FileUtils.readFileToString(in, "UTF-8");
            content = content.replaceAll("##projectName##", projectName);
            content = content.replaceAll("##mainClass##", mainClassName);
            FileUtils.writeStringToFile(out, content, "UTF-8");
        }
    }

    private void renameProjectFolder() throws DirectoryCreationException {
        String oldProjectFolder = projectPath + "/IntelliJ-2-NetBeans";
        String newProjectFolder = projectPath + "/" + projectName + "_IntelliJ-2-NetBeans";
        try {
            FileUtils.moveDirectory(new File(oldProjectFolder), new File(newProjectFolder));
        } catch (IOException e) {
            throw new DirectoryCreationException(newProjectFolder);
        }
    }

    public class ExtensionFilter implements FilenameFilter {
        private final String ext;

        public ExtensionFilter(String ext) {
            this.ext = ext;
        }

        public boolean accept(File dir, String name) {
            return (name.endsWith(ext));
        }
    }
}
