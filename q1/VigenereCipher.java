import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
* Cipher interface for use with the CM10228: Principles of Programming 2 coursework.
* 
* This should not be modified by the student.
* 
* @author       Christopher Clarke
* @version      1.0 
*/
interface Cipher {
    /**
    * Encrypts a message using a key.
    *
    * @param  message_filename      the filename of the message to be encrypted
    * @param  key_filename          the filename of the key to be used to encrypt the message
    * @return       The encrypted message
    */
    public String encrypt(String message_filename, String key_filename);
    
    /**
    * Decrypts a message using a key.
    *
    * @param  message_filename      the filename of the message to be decrypted
    * @param  key_filename          the filename of the key to be used to decrypt the message
    * @return       The decrypted message
    */
    public String decrypt(String message_filename, String key_filename);
}

public class VigenereCipher implements Cipher {
    private static final String[] vigenereSquare = {
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "BCDEFGHIJKLMNOPQRSTUVWXYZA",
        "CDEFGHIJKLMNOPQRSTUVWXYZAB",
        "DEFGHIJKLMNOPQRSTUVWXYZABC",
        "EFGHIJKLMNOPQRSTUVWXYZABCD",
        "FGHIJKLMNOPQRSTUVWXYZABCDE",
        "GHIJKLMNOPQRSTUVWXYZABCDEF",
        "HIJKLMNOPQRSTUVWXYZABCDEFG",
        "IJKLMNOPQRSTUVWXYZABCDEFGH",
        "JKLMNOPQRSTUVWXYZABCDEFGHI",
        "KLMNOPQRSTUVWXYZABCDEFGHIJ",
        "LMNOPQRSTUVWXYZABCDEFGHIJK",
        "MNOPQRSTUVWXYZABCDEFGHIJKL",
        "NOPQRSTUVWXYZABCDEFGHIJKLM",
        "OPQRSTUVWXYZABCDEFGHIJKLMN",
        "PQRSTUVWXYZABCDEFGHIJKLMNO",
        "QRSTUVWXYZABCDEFGHIJKLMNOP",
        "RSTUVWXYZABCDEFGHIJKLMNOPQ",
        "STUVWXYZABCDEFGHIJKLMNOPQR",
        "TUVWXYZABCDEFGHIJKLMNOPQRS",
        "UVWXYZABCDEFGHIJKLMNOPQRST",
        "VWXYZABCDEFGHIJKLMNOPQRSTU",
        "WXYZABCDEFGHIJKLMNOPQRSTUV",
        "XYZABCDEFGHIJKLMNOPQRSTUVW",
        "YZABCDEFGHIJKLMNOPQRSTUVWX",
        "ZABCDEFGHIJKLMNOPQRSTUVWXY",
    };

    private static final String alphabetLength = vigenereSquare[0].length();

    private static int getLetterIndex(char letter) {
        int letterIndex = Character.toLowerCase(letter) - 'a';
        // TODO: Check if letter index is in bounds.
        // if (letterIndex < 0 || letterIndex > ...)
        return letterIndex
    }

    @Override
    public String encrypt(String messageFilename, String keyFilename) {
        String message = VigenereCipher.getFileContents(messageFilename);
        String key = VigenereCipher.getFileContents(keyFilename);

        StringBuilder modifiedKey = new StringBuilder(key);
        while (modifiedKey.length() < message.length()) {
            modifiedKey.append(key);
        }

        if (modifiedKey.length() > message.length()) {
            modifiedKey.setLength(message.length());
        }
        key = modifiedKey.toString();

        StringBuilder encryptedMessageBuilder = new StringBuilder();

        for (int i = 0; i < message.length(); i++) {
            char currentMessageLetter = message.charAt(i);
            char currentKeyLetter = key.charAt(i);

            int vigenereRowIndex = VigenereCipher.getLetterIndex(currentKeyLetter);
            int vigenereColumnIndex = VigenereCipher.getLetterIndex(currentMessageLetter);

            if (vigenereRowIndex || vigenereColumnIndex > VigenereCipher.alphabetLength - 1){ }

            char encryptedLetter = VigenereCipher.vigenereSquare[vigenereRowIndex].charAt(vigenereColumnIndex);
            encryptedMessageBuilder.append(encryptedLetter);
        }

        String encryptedMessage = encryptedMessageBuilder.toString();
        return "hi";
    }

    @Override
    public String decrypt(String messageFilename, String keyFilename) {
        return "hello"; // Placeholder implementation
    }

    private static String getFileContents(String filename) {
        StringBuilder stringBuilder = new StringBuilder();
        
        try {
            File file = new File(filename);
            Scanner scanner = new Scanner(file);
            
            while (scanner.hasNextLine()) {
                stringBuilder.append(scanner.nextLine()).append("\n"); 
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String fileContents = stringBuilder.toString().trim();
        return fileContents;
    }

    public static void main(String[] args) {
        VigenereCipher cipher = new VigenereCipher();
        String messageFilename = "encrypt_check.txt";
        String keyFilename = "key_check.txt";
        String encryptedMessageCheckFilename = "decrypt_check.txt";

        String originalMessage = cipher.getFileContents(messageFilename);
        String encryptedMessage = cipher.encrypt(messageFilename, keyFilename);
        String encryptedMessageCheck = cipher.getFileContents(encryptedMessageCheckFilename);
        String decryptedMessage = cipher.decrypt(encryptedMessageCheckFilename, keyFilename);

        System.out.println("ORIGINAL:\n" + originalMessage);
        System.out.println("\nENCRYPTED:\n" + encryptedMessage);
        System.out.println("\nENCRYPTED CHECK:\n" + encryptedMessageCheck);
        System.out.println("\nDECRYPTED:\n" + decryptedMessage);

        if (!encryptedMessage.equals(encryptedMessageCheck)) {
            System.out.println("\nWARNING:\nEncrypted message does not match encrypted check!");
        }
        if (!decryptedMessage.equals(originalMessage)) {
            System.out.println("\nWARNING:\nOriginal message does not match decrypted message!");
        }
    }
}
