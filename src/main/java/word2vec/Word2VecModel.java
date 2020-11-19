package word2vec;

import org.deeplearning4j.models.paragraphvectors.ParagraphVectors;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.CollectionSentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class Word2VecModel {

    public static List<List<Double>> transformWords(List<String> words, int vectorSize) {
        try {
            SentenceIterator iter = new CollectionSentenceIterator(words);
            iter.setPreProcessor(String::toLowerCase);
            TokenizerFactory t = new DefaultTokenizerFactory();
            Word2Vec vec = new Word2Vec.Builder()
                    .minWordFrequency(1)
                    .iterations(1)
                    .layerSize(vectorSize)
                    .seed(42)
                    .windowSize(5)
                    .iterate(iter)
                    .tokenizerFactory(t)
                    .build();

            vec.fit();
            return words.stream()
                    .filter(vec::hasWord)
                    .map(w -> Arrays.stream(vec.getWordVector(w)).boxed().collect(Collectors.toList()))
                    .collect(Collectors.toList());
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }

    public static Map<String, List<Double>> transformParagraph(Map<String, String> words, int vectorSize) {
        Map<String, List<Double>> resultMap = new HashMap<>();
        try {
            SentenceIterator iter = new CollectionSentenceIterator(words.values());
            TokenizerFactory t = new DefaultTokenizerFactory();
            t.setTokenPreProcessor(new CommonPreprocessor());

            ParagraphVectors vec = new ParagraphVectors.Builder()
                    .minWordFrequency(1)
                    .iterations(5)
                    .layerSize(vectorSize)
                    .learningRate(0.05)
                    .windowSize(5)
                    .iterate(iter)
                    .trainWordVectors(false)
                    .tokenizerFactory(t)
                    .sampling(0)
                    .build();
            vec.fit();

            for (String key : words.keySet()) {
                resultMap.put(key, Arrays.stream(vec.inferVector(words.get(key)).toDoubleVector()).boxed().collect(Collectors.toList()));
            }
            return resultMap;
        } catch (Exception e) {
            e.printStackTrace();
            return resultMap;
        }
    }
}
