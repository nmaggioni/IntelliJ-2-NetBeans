class DirectoryCreationException extends Exception {
    private final String dirName;

    public DirectoryCreationException(String dirName) {
        this.dirName = dirName;
    }

    public String getDirName() {
        return dirName;
    }
}
