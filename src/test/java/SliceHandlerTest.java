import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class SliceHandlerTest {
    @Test
    void sliceByLines() {
        String inputDir = "/home/qian/Documents/Work/Data/ModifiedMethod";
        String outputDir = "/home/qian/Documents/Work/Data/OwaspSlice2";
        String lineFile = "/home/qian/Documents/Work/Data/slice2.csv";
        SliceHandler.sliceByLines(inputDir, outputDir, lineFile);
    }
}