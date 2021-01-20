import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.Arrays;

class SliceHandlerTest {
    @Test
    void sliceByLines() {
        String inputDir = "/home/qian/Documents/Work/Data/ModifiedMethod";
        String outputDir = "/home/qian/Documents/Work/Data/OwaspSlice2";
        String lineFile = "/home/qian/Documents/Work/Data/slice2.csv";
        SliceHandler.sliceByLines(inputDir, outputDir, lineFile);
    }

    @Test
    void sliceFile() {
        File f = new File("/home/qian/Downloads/JFreeChart.java");
        System.out.println(SliceHandler.sliceFile(f, Arrays.asList(584, 590)));
    }
}