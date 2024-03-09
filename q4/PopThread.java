import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;

public class PopThread implements Runnable {
    private ArrayList<String> files;
    public static int total = 0;
    public static int current = 1;

    public PopThread(ArrayList<String> files) {
        this.files = files;
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

    private void processFile(String filename) {
        // Placeholder for reading file content and extracting the order tag
        // You'll need to implement the logic for reading the file's contents
        // and extracting the order from its label
        String contents = getFileContents(filename);
        int len = contents.length();
        if (len < 7) {
            //TODO: Do something.
            return;
        }

        int orderTag = -1;

        try {
            this.total = Integer.parseInt(contents.substring(len-3, len));
            orderTag = Integer.parseInt(contents.substring(len-7, len-4));
        } catch (NumberFormatException e) {
            //TODO: Do something.
            System.out.println("The string did not contain a parsable integer.");
            return;
        }
        // nahhhhh scrap this shiiiiiiiiiiiiiiiiii
        // I want to implement the following logic here:
        // if order tag != this.current then pause the thread (how?)
        // otherwise write the contents to result file and unpause all previous threads.
        // probably have to do it in a loop so that it check the first condition every time the threads are unpaused.
        writeToResultFile(contents, orderTag);
    }
    private static synchronized void writeToResultFile(String contents, int orderTag) {
        while (orderTag != PopThread.current) {
            try {
                System.out.println("current ordertag: ");
                System.out.println(orderTag);
                System.out.println();
                System.out.println("Current static PopThread.current: ");
                System.out.println(PopThread.current);
                PopThread.class.wait(); 
            } catch (InterruptedException e) {
                // Reset the interrupt flag.
                Thread.currentThread().interrupt(); 
            }
        }
        // Perform the action for the current orderTag
        PopThread.current++;
        System.out.println(orderTag);
        PopThread.class.notifyAll(); // Notify other threads waiting on this class object's monitor
    }


    @Override
    public void run() {
        // probably do stuff here
        // go through each file 
        // if u find orderTag matching PopThread.current then write the contents to results
        // otherwise add the file to a queue list
        // if u went through each file and havent found the right orderTag, pause this thread and switch to another
        // after resuming this paused thread go through the queue list and do the same thing if u don't find the right file again
        for (String fileName : files) {
            processFile(fileName);
        }
    }

    public static void main(String[] args) {
        ArrayList<String> listOne = new ArrayList<>();
        ArrayList<String> listTwo = new ArrayList<>();

        listOne.add("1972-12-11.txt");
        listOne.add("1831-06-01.txt");
        listOne.add("1961-04-12.txt");
        listTwo.add("2003-08-27.txt");

        Thread threadTwo = new Thread(new PopThread(listTwo));
        Thread threadOne = new Thread(new PopThread(listOne));

        threadOne.start();
        threadTwo.start();

        try {
            threadOne.join();
            threadTwo.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
