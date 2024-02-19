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
    @Override
    public String encrypt(String messageFilename, String keyFilename) {
        return "hi"; // Placeholder implementation
    }

    @Override
    public String decrypt(String messageFilename, String keyFilename) {
        return "hello"; // Placeholder implementation
    }

    public static void main(String[] args) {
        VigenereCipher cipher = new VigenereCipher();
        String keyFilename = "key_check.txt";
        String messageFilename = "encrypt_check.txt";
        String encryptedMessageCheckFilename = "decrypt_check.txt";

        StringBuilder originalMessageBuilder = new StringBuilder();
        
        try {
            File file = new File(messageFilename);
            Scanner scanner = new Scanner(file);
            
            while (scanner.hasNextLine()) {
                originalMessageBuilder.append(scanner.nextLine()).append("\n"); 
            }
            scanner.close(); // Close the scanner
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        // Convert StringBuilder to String and trim the trailing newline
        String originalMessage = originalMessageBuilder.toString().trim();

        String encryptedMessage = cipher.encrypt(originalMessage, keyFilename);
        String decryptedMessage = cipher.decrypt(encryptedMessage, keyFilename);

        System.out.println("Original: " + originalMessage);
        System.out.println("Encrypted: " + encryptedMessage);
        System.out.println("Decrypted: " + decryptedMessage);
    }
}
