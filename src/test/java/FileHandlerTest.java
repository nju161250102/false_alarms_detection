import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FileHandlerTest {
    @Test
    void prettyPrint() {
        String inputDir = "/home/qian/Documents/Work/Data/OwaspMethod";
        String outputDir = "/home/qian/Documents/Work/Data/ModifiedMethod";
        FileHandler.prettyPrint(inputDir, outputDir);
    }
}