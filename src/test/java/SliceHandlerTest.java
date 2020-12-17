import org.junit.jupiter.api.Test;

class SliceHandlerTest {
    @Test
    void sliceByLines() {
        String inputDir = "/home/qian/Documents/Work/Data/ModifiedMethod";
        String outputDir = "/home/qian/Documents/Work/Data/OwaspSlice2";
        String lineFile = "/home/qian/Documents/Work/Data/slice2.csv";
        SliceHandler.sliceByLines(inputDir, outputDir, lineFile);
    }
}