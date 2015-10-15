class BadPathException extends Exception {
    private final String dirPath;

    public BadPathException(String dirPath) {
        this.dirPath = dirPath;
    }

    public String getDirPath() {
        return dirPath;
    }
}
