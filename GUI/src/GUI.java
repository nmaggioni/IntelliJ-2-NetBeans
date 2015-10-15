import org.apache.commons.io.FileUtils;

import javax.swing.*;
import javax.swing.filechooser.FileFilter;
import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;

@SuppressWarnings("unused")
class GUI extends JFrame {
    private JButton convertButton;
    private JPanel IntelliJ2NetBeans;
    private JTextField projectPathInput;
    private JButton browseButton;
    private JProgressBar progressBar;

    private String projectPath;

    private GUI() {
        super("IntelliJ-2-NetBeans");
        setContentPane(IntelliJ2NetBeans);
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        pack();
        setVisible(true);

        convertButton.addActionListener(e -> {
            if (projectPath != null) {
                Converter converter = null;
                try {
                    converter = new Converter(projectPath, progressBar);
                    while (true) {
                        try {
                            converter.convertProject();
                            JOptionPane.showMessageDialog(this, "Project converted successfully!");
                            break;
                        } catch (IOException | URISyntaxException e1) {
                            e1.printStackTrace();
                            JOptionPane.showMessageDialog(this, "Unknown I/O error.",
                                    "Error", JOptionPane.ERROR_MESSAGE);
                            break;
                        } catch (DirectoryCreationException dirExc) {
                            JOptionPane.showMessageDialog(this,
                                    "Error during directory creation: " + dirExc.getDirName(),
                                    "Error", JOptionPane.ERROR_MESSAGE);
                            break;
                        } catch (MissingFileException missExc) {
                            JOptionPane.showMessageDialog(this, "Needed file not found: " + missExc.getFileName(),
                                    "Error", JOptionPane.ERROR_MESSAGE);
                            break;
                        } catch (ExistingDirectoryException existExc) {
                            int dialogResult = JOptionPane.showConfirmDialog(null,
                                    "Directory exists: " + existExc.getDirName() + "\nDo you want to replace it?",
                                    "Directory deletion", JOptionPane.YES_NO_OPTION);
                            if (dialogResult == JOptionPane.YES_OPTION) {
                                FileUtils.deleteDirectory(new File(projectPath + "/" + existExc.getDirName()));
                            }
                        } catch (BadPathException pathExc) {
                            JOptionPane.showMessageDialog(this, "Invalid path: " + pathExc.getDirPath());
                            break;
                        } catch (MissingDirectoryException missExc) {
                            JOptionPane.showMessageDialog(this, "Missing directory: " + missExc.getDirName());
                            break;
                        }
                    }
                } catch (MissingMainClassException e1) {
                    JOptionPane.showMessageDialog(this, "Cannot find valid main class name! " +
                            "Please check the project's manifest.");
                } catch (IOException e2) {
                    e2.printStackTrace();
                }
            } else {
                JOptionPane.showMessageDialog(this, "Please specify the project path.",
                        "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        browseButton.addActionListener(e -> {
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setAcceptAllFileFilterUsed(false);
            fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
            fileChooser.setFileFilter(new DirFilter());
            fileChooser.showOpenDialog(this);
            projectPath = fileChooser.getSelectedFile().getPath();
            projectPathInput.setText(projectPath);

            if (!progressBar.isStringPainted()) {
                progressBar.setStringPainted(true);
            }
            progressBar.setValue(0);
        });
    }

    public static void main(String[] args) {
        new GUI();
    }

    private class DirFilter extends FileFilter {

        public boolean accept(File file) {
            return file.isDirectory();
        }

        public String getDescription() {
            return "Project directory";
        }
    }
}
