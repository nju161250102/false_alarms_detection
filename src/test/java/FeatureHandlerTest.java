import org.junit.Test;

public class FeatureHandlerTest {
    @Test
    public void extractFiles() {
//        String inputDir = "/home/qian/Documents/Work/Data/OwaspMethod";
//        String outputDir = "/home/qian/Documents/Work/Data/MethodFeature";
        String sliceInputDir = "/home/qian/Documents/Work/Data/OwaspSlice2/";
        String sliceOutputDir = "/home/qian/Documents/Work/Data/SliceFeature/";
//        FeatureHandler.extractFiles(inputDir, outputDir);
        FeatureHandler.extractFiles(sliceInputDir, sliceOutputDir);
    }

    @Test
    public void extractBytes() {
        String inputDir = "/home/qian/Documents/Work/mangrove/data/slices/owasp";
        String outputDir = "/home/qian/Documents/Work/Data/SliceFeature";
        FeatureHandler.extractSliceFile(inputDir, outputDir);
    }
}