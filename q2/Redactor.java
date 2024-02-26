public class Redactor {

    public static String redact(String content, String[] redactWords) {
        StringBuilder redactedContent = new StringBuilder(content);
        int startOfWordIndex = -1;

        for (String word : redactWords) {
            startOfWordIndex = redactedContent.toString().toLowerCase().indexOf(word.toLowerCase());

            while (startOfWordIndex != -1) {
                int endOfWordIndex = startOfWordIndex + word.length();
                boolean startIsValid = startOfWordIndex == 0 || !Character.isLetterOrDigit(content.charAt(startOfWordIndex - 1));
                boolean endIsValid = endOfWordIndex == content.length() || !Character.isLetterOrDigit(content.charAt(endOfWordIndex));
                boolean wordIsValid = startIsValid && endIsValid;

                if (wordIsValid) {
                    for (int i = 0; i < word.length(); i++) {
                        redactedContent.setCharAt(startOfWordIndex + i, '*');
                    }
                }

                startOfWordIndex = redactedContent.toString().toLowerCase().indexOf(word.toLowerCase(), startOfWordIndex + word.length());
            }
        }

        return redactedContent.toString();
    }

    public static void main(String[] args) {
        String originalContent = "This is a sensitive document. The secret code password is 1234.";
        String[] wordsToRedact = {"sensitive", "secret", "1234", "pass"};

        String redactedContent = redact(originalContent, wordsToRedact);
        System.out.println(redactedContent);
    }
}
