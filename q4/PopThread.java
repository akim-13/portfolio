import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;

public class PopThread implements Runnable {
    private ArrayList<String> files;
    public static int total = 1000;
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
        String contents = getFileContents(filename);
        int len = contents.length();
        if (len < 7) {
            return;
        }

        int orderTag;

        try {
            this.total = Integer.parseInt(contents.substring(len-3, len));
            orderTag = Integer.parseInt(contents.substring(len-7, len-4));
        } catch (NumberFormatException e) {
            return;
        }

        if (orderTag == PopThread.current) {
            writeToResultFile(contents, orderTag);
        }
    }

    private static synchronized void writeToResultFile(String contents, int orderTag) {
        // Just to be safe.
        if (orderTag != PopThread.current) {
            return;
        }

        PopThread.current++;

        FileWriter writer;
        String filename = "result.txt";

        try {
            if (orderTag == 1) {
                // Overwrite.
                 writer = new FileWriter(filename);
            } else {
                // Append.
                writer = new FileWriter(filename, true);
            }
            writer.write(contents + "\n");
            writer.close();
        } catch (IOException e) {
            return;
        }
    }

    @Override
    public void run() {
        while (PopThread.current <= PopThread.total) {
            for (String fileName : files) {
                processFile(fileName);
            }
        }
    }

    public static void main(String[] args) {
        ArrayList<String> listOne = new ArrayList<>();
        ArrayList<String> listTwo = new ArrayList<>();
        ArrayList<String> listThree = new ArrayList<>();

        // Thread 1 with 4 files
        listOne.add("1972-12-11.txt");
        listOne.add("1831-06-01.txt");
        listOne.add("1609-09-13.txt");
        listOne.add("1927-05-20.txt");

        // Thread 2 with 5 files
        listTwo.add("1961-04-12.txt");
        listTwo.add("2003-08-27.txt");
        listTwo.add("1990-04-24.txt");
        listTwo.add("2012-08-05.txt");
        listTwo.add("1953-07-29.txt");

        // Thread 3 with 1 file
        listThree.add("2008-08-08.txt");

        Thread threadOne = new Thread(new PopThread(listOne));
        Thread threadTwo = new Thread(new PopThread(listTwo));
        Thread threadThree = new Thread(new PopThread(listThree));

        threadOne.start();
        threadTwo.start();
        threadThree.start();

        try {
            threadOne.join();
            threadTwo.join();
            threadThree.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // Precheck main.
    /* public static void main(String[] args) {
        ArrayList<String> listOne = new ArrayList<>();
        ArrayList<String> listTwo = new ArrayList<>();

        listOne.add("1972-12-11.txt");
        listOne.add("1831-06-01.txt");
        listTwo.add("1961-04-12.txt");
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
    } */
}
