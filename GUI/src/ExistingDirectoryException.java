class ExistingDirectoryException extends Exception {
    private final String dirName;

    public ExistingDirectoryException(String dirName) {
        this.dirName = dirName;
    }

    public String getDirName() {
        return dirName;
    }
}
