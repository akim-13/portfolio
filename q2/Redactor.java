public class Redactor {
    public static boolean arrayContainsElement(String[] array, String key) {
        for (String element : array) {
            if (element.equalsIgnoreCase(key)) {
                return true;
            }
        }
        return false;
    }

//     public static String redact(String content, String[] redactWords) {
//         String[] words = content.split("[^a-zA-Z]+");
//         StringBuilder redactedContent = new StringBuilder(content);
//
//         for (String word : words) {
//             System.out.println(word);
//             if (arrayContainsElement(redactWords, word)) {
//                 // find `word` in redactedContent and replace it
//             } 
//         }
//
//         return redactedContent.toString().trim(); // Trim to remove the last space
//     }
    public static String repeatAsterisks(int length) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append("*");
        }
        return sb.toString();
    }

    public static String redact(String content, String[] redactWords) {
        for (String word : redactWords) {
            String asterisks = repeatAsterisks(word.length());
            content = content.replace(word, asterisks);
        }
        return content;
    }

    public static void main(String[] args) {
        String originalContent = "This is a sensitive document. The secret code is 1234.";
        String[] wordsToRedact = {"sensitive", "secret", "1234"};
        
        String redactedContent = redact(originalContent, wordsToRedact);
        System.out.println(redactedContent);
    }
}
