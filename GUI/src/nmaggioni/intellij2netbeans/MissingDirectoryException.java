package nmaggioni.intellij2netbeans;

class MissingDirectoryException extends Exception {
    private final String dirName;

    @SuppressWarnings("SameParameterValue")
    public MissingDirectoryException(String dirName) {
        this.dirName = dirName;
    }

    public String getDirName() {
        return dirName;
    }
}
