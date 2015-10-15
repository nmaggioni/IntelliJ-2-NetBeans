class MissingFileException extends Exception {
    private final String fileName;

    public MissingFileException(String fileName) {
        this.fileName = fileName;
    }

    public String getFileName() {
        return fileName;
    }
}
