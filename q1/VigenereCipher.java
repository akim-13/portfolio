import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
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

    private static int getLetterIndex(char letter) {
        letter = Character.toUpperCase(letter);
        if (letter < 'A' || letter > 'Z') {
            return -1;
        }
        int letterIndex = letter - 'A';
        return letterIndex;
    }

    private static String modifyKey(String key, int messageLength) {
        StringBuilder modifiedKey = new StringBuilder(key);

        if (modifiedKey.length() == 0) {
            return "";
        }

        while (modifiedKey.length() < messageLength) {
            modifiedKey.append(key);
        }

        if (modifiedKey.length() > messageLength) {
            modifiedKey.setLength(messageLength);
        }

        return modifiedKey.toString();
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
            return "";
        }

        String fileContents = stringBuilder.toString().trim();
        return fileContents;
    }

    @Override
    public String encrypt(String messageFilename, String keyFilename) {
        // Read the files.
        String message = VigenereCipher.getFileContents(messageFilename);
        String key = VigenereCipher.getFileContents(keyFilename);

        key = VigenereCipher.modifyKey(key, message.length());

        if (key.equals("")) {
            return message;
        }

        // Encrypt each letter 1 by 1.
        StringBuilder encryptedMessageBuilder = new StringBuilder();
        for (int i = 0; i < message.length(); i++) {
            char currentMessageLetter = message.charAt(i);
            char currentKeyLetter = key.charAt(i);

            int vigenereRowIndex = VigenereCipher.getLetterIndex(currentKeyLetter);
            int vigenereColumnIndex = VigenereCipher.getLetterIndex(currentMessageLetter);

            if (vigenereRowIndex == -1) {
                return "ERROR: Invalid key.";
            }

            if (vigenereColumnIndex != -1) { 
                char encryptedLetter = VigenereCipher.vigenereSquare[vigenereRowIndex].charAt(vigenereColumnIndex);
                encryptedMessageBuilder.append(encryptedLetter);
            } else {
                encryptedMessageBuilder.append(currentMessageLetter);
            }
        }

        String encryptedMessage = encryptedMessageBuilder.toString();
        return encryptedMessage;
    }

    @Override
    public String decrypt(String messageFilename, String keyFilename) {
        String encryptedMessage = VigenereCipher.getFileContents(messageFilename);
        String key = VigenereCipher.getFileContents(keyFilename);

        key = VigenereCipher.modifyKey(key, encryptedMessage.length());

        if (key.equals("")) {
            return encryptedMessage;
        }

        StringBuilder decryptedMessageBuilder = new StringBuilder();
        for (int i = 0; i < encryptedMessage.length(); i++) {
            char currentEncryptedMessageLetter = encryptedMessage.charAt(i);
            char currentKeyLetter = key.charAt(i);

            int vigenereRowIndex = VigenereCipher.getLetterIndex(currentKeyLetter);
            int vigenereColumnIndex = VigenereCipher.getLetterIndex(currentEncryptedMessageLetter);

            if (vigenereRowIndex == -1) {
                return "ERROR: Invalid key.";
            }

            if (vigenereColumnIndex != -1) { 
                int decryptedLetterIndex = VigenereCipher.vigenereSquare[vigenereRowIndex].indexOf(currentEncryptedMessageLetter);
                char decryptedLetter = VigenereCipher.vigenereSquare[0].charAt(decryptedLetterIndex);
                decryptedMessageBuilder.append(decryptedLetter);
            } else {
                decryptedMessageBuilder.append(currentEncryptedMessageLetter);
            }
        }

        String decryptedMessage = decryptedMessageBuilder.toString();
        return decryptedMessage;
    }

    public static void main(String[] args) {
        VigenereCipher cipher = new VigenereCipher();
        String messageFilename = "enc.txt";
        String keyFilename = "key.txt";
        String encryptedMessageCheckFilename = "dec.txt";

        String originalMessage = cipher.getFileContents(messageFilename);
        String encryptedMessage = cipher.encrypt(messageFilename, keyFilename);
        String encryptedMessageCheck = cipher.getFileContents(encryptedMessageCheckFilename);
        String decryptedMessage = cipher.decrypt(encryptedMessageCheckFilename, keyFilename);

        System.out.println("ORIGINAL:\n" + originalMessage);
        System.out.println("\nENCRYPTED:\n" + encryptedMessage);
        System.out.println("\nDECRYPTED:\n" + decryptedMessage);

        if (!encryptedMessage.equals(encryptedMessageCheck)) {
            System.out.println("\nWARNING:\nEncrypted message does not match encrypted check!");
            System.out.println("\nENCRYPTED CHECK:\n" + encryptedMessageCheck);
        }
        if (!decryptedMessage.equals(originalMessage.toUpperCase())) {
            System.out.println("\nWARNING:\nOriginal message does not match decrypted message!");
        }
    }
}
