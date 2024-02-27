public class SortedLinkedList implements SortedList {
    private Node last;
    private Node first;

    public SortedLinkedList() {
        // Rightmost.
        this.last = null; 
        // Leftmost.
        this.first = null;
    }

    public static void main(String[] args) {
        SortedLinkedList list = new SortedLinkedList();
        list.add("abC");
        list.add("Beee");
        list.add("bEe");
        list.add("Bc");
        list.add("acd");
        list.print();
        System.out.println(list.size());
    }

    /**
    * Returns the number of Nodes in the linked list.
    *
    * @return      the number of Nodes in the linked list
    */
    @Override
    public int size() {
        int cnt = 0;
        Node nextNode = this.first;

        while (nextNode != null) {
            cnt++;
            nextNode = nextNode.getNext();
        }

        return cnt;
    }

    private void insertNodeAfterGiven(Node curNode, String string){
        Node newNode = new Node(curNode, string);
        Node nextNode = curNode.getNext();
        curNode.setNext(newNode);
        newNode.setNext(nextNode);
        if (nextNode != null) {
            nextNode.setPrev(newNode); 
        } else {
            this.last = curNode;
        }
    }

    private void insertNodeBeforeGiven(Node curNode, String string){
        if (curNode == null) {
            return;
        }
        Node newNode = new Node(string, curNode);
        Node prevNode = curNode.getPrev();
        curNode.setPrev(newNode);
        newNode.setPrev(prevNode);
        if (prevNode != null) {
            prevNode.setNext(newNode); 
        } else {
            this.first = curNode;
        }
    }

    /**
    * Adds a Node with the specified string to the linked list in
    * the appropriate position given the specified alphabetical order
    * (i.e., ascending/descending).
    *
    * @param  string  a String to be added to the linked list
    */
    @Override
    public void add(String string) {
        // TODO: Test and clean up.
        if (this.first != null) {
            Node curNode = this.first;
            int i = 0;
            char stringChar = string.toLowerCase().charAt(i);
            String nodeString = curNode.getString();
            char nodeChar = nodeString.toLowerCase().charAt(i);

            boolean stringIsDuplicate = string.toLowerCase().equals(nodeString.toLowerCase());
            if (stringIsDuplicate) {
                return;
            }

            while (curNode != null) {
                if (stringChar > nodeChar) {
                    this.insertNodeAfterGiven(curNode, string);
                    break;

                } else if (stringChar == nodeChar) {
                    nodeString = curNode.getString();
                    i++;

                    boolean nodeStringIsShorter = i >= nodeString.length();
                    boolean givenStringIsShorter = i >= string.length();
                    if (nodeStringIsShorter) {
                        this.insertNodeAfterGiven(curNode, string);
                        break;
                    } else if (givenStringIsShorter) {
                        this.insertNodeBeforeGiven(curNode, string);
                        break;
                    }

                    stringChar = string.toLowerCase().charAt(i);
                    nodeChar = nodeString.toLowerCase().charAt(i);

                } else {
                    curNode = curNode.getNext();
                }
            }
        } else { 
            Node newNode = new Node(string);
            this.last = newNode;
            this.first = newNode;
        }
    }

    /**
    * Adds a Node to the linked list in the appropriate position
    * given the specified alphabetical order (i.e., ascending/descending).
    *
    * @param  node  a Node to be added to the linked list
    */
    @Override
    public void add(Node node) {
    }

    /**
    * Returns the first Node of the linked list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      the first Node in the linked list
    */
    @Override
    public Node getFirst(){
        return this.first;
    }

    /**
    * Returns the last Node of the linked list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      the last Node in the linked list
    */
    @Override
    public Node getLast(){
        return this.last;
    };

    /**
    * Returns the Node at the specified index assuming indices start
    * at 0 and end with size-1 given the specified alphabetical order
    * (i.e., ascending/descending).
    *
    * @param  index  the index of the Node in the linked list to be retrieved
    * @return      the Node in the linked list at the specified index
    */
    @Override
    public Node get(int index){
        if (index < 0 || index >= this.size()) {
            return null;
        }

        Node nextNode = this.first;
        for (int i = 0; i != index; i++) {
            nextNode = nextNode.getNext();
        }

        return nextNode;
    };

    /**
    * Checks to see if the list contains a Node with the specified
    * string.
    *
    * @param  string  the String to be searched for in the linked list
    * @return       True if the string is present or false if not
    */
    // TODO: Optimize.
    @Override
    public boolean isPresent(String string) {
        Node nextNode = this.first;
        while (nextNode != null) {
            if (nextNode.getString().equals(string)) {
                return true;
            }
            nextNode = nextNode.getNext();
        }
        return false;
    }

    /**
    * Removes the first Node from the list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      Returns true if successful or false if unsuccessful
    */
    @Override
    public boolean removeFirst() {
        if (this.first == null) {
            return false;
        }

        if (this.size() > 1) {
            this.first = this.first.getNext();
            this.first.setPrev(null);
        } else {
            this.first = null;
            this.last = null;
        }

        return true;
    }

    /**
    * Removes the last Node from the list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      Returns true if successful or false if unsuccessful
    */
    @Override
    public boolean removeLast() {
        if (this.last == null) {
            return false;
        }

        if (this.size() > 1) {
            this.last = this.last.getPrev();
            this.last.setNext(null);
        } else {
            this.first = null;
            this.last = null;
        }

        return true;
    }

    /**
    * Removes the Node at the specified index from the list assuming indices
    * start at 0 and end with size-1 given the specified alphabetical order
    * (i.e., ascending/descending)
    *
    * @param  index  the index of the Node in the linked list to be removed
    * @return      Returns true if successful or false if unsuccessful
    */
    @Override
    public boolean remove(int index) {
        return false;
    }

    /**
    * Removes the Node from the list that contains the specified string.
    *
    * @param  string  the string to be removed from the linked list
    * @return      Returns true if successful or false if unsuccessful
    */
    @Override
    public boolean remove(String string) {
        return false;
    }

    /**
    * Orders the linked list in ascending alphabetical order.
    *
    */
    @Override
    public void orderAscending() {}

    /**
    * Orders the linked list in descending alphabetical order.
    *
    */
    @Override
    public void orderDescending() {}

    /**
    * Prints the contents of the linked list in the specified alphabetical order
    * (i.e., ascending/descending) to System.out with each node's string on
    * a new line.
    *
    */
    @Override
    public void print() {
        Node nextNode = this.first;
        while (nextNode != null) {
            System.out.println(nextNode.getString());
            nextNode = nextNode.getNext();
        }
    }
}

// DO NOT CHANGE!
interface SortedList {

    /**
    * Returns the number of Nodes in the linked list.
    *
    * @return      the number of Nodes in the linked list
    */
    public int size();

    /**
    * Adds a Node with the specified string to the linked list in
    * the appropriate position given the specified alphabetical order
    * (i.e., ascending/descending).
    *
    * @param  string  a String to be added to the linked list
    */
    public void add(String string);

    /**
    * Adds a Node to the linked list in the appropriate position
    * given the specified alphabetical order (i.e., ascending/descending).
    *
    * @param  node  a Node to be added to the linked list
    */
    public void add(Node node);

    /**
    * Returns the first Node of the linked list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      the first Node in the linked list
    */
    public Node getFirst();

    /**
    * Returns the last Node of the linked list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      the last Node in the linked list
    */
    public Node getLast();

    /**
    * Returns the Node at the specified index assuming indices start
    * at 0 and end with size-1 given the specified alphabetical order
    * (i.e., ascending/descending).
    *
    * @param  index  the index of the Node in the linked list to be retrieved
    * @return      the Node in the linked list at the specified index
    */
    public Node get(int index);

    /**
    * Checks to see if the list contains a Node with the specified
    * string.
    *
    * @param  string  the String to be searched for in the linked list
    * @return       True if the string is present or false if not
    */
    public boolean isPresent(String string);

    /**
    * Removes the first Node from the list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      Returns true if successful or false if unsuccessful
    */
    public boolean removeFirst();

    /**
    * Removes the last Node from the list given the specified
    * alphabetical order (i.e., ascending/descending).
    *
    * @return      Returns true if successful or false if unsuccessful
    */
    public boolean removeLast();

    /**
    * Removes the Node at the specified index from the list assuming indices
    * start at 0 and end with size-1 given the specified alphabetical order
    * (i.e., ascending/descending)
    *
    * @param  index  the index of the Node in the linked list to be removed
    * @return      Returns true if successful or false if unsuccessful
    */
    public boolean remove(int index);

    /**
    * Removes the Node from the list that contains the specified string.
    *
    * @param  string  the string to be removed from the linked list
    * @return      Returns true if successful or false if unsuccessful
    */
    public boolean remove(String string);

    /**
    * Orders the linked list in ascending alphabetical order.
    *
    */
    public void orderAscending();

    /**
    * Orders the linked list in descending alphabetical order.
    *
    */
    public void orderDescending();

    /**
    * Prints the contents of the linked list in the specified alphabetical order
    * (i.e., ascending/descending) to System.out with each node's string on
    * a new line.
    *
    */
    public void print();
}

// DO NOT CHANGE!
class Node {
    private String name;
    private Node prev;
    private Node next;
    
    public Node(String name) {
        this.prev = null;
        this.name = name;
        this.next = null;
    }
    
    public Node(String name, Node next) {
        this.prev = null;
        this.name = name;
        this.next = next;
    }
    
    public Node(Node prev, String name) {
        this.prev = prev;
        this.name = name;
        this.next = null;
    }
    
    public Node(Node prev, String name, Node next) {
        this.prev = prev;
        this.name = name;
        this.next = next;
    }
    
    public void setString(String name) {
        this.name = name;
    }
    
    public String getString() {
        return this.name;
    }
    
    public void setNext(Node next) {
        this.next = next;
    }
    
    public Node getNext() {
        return this.next;
    }
    
    public void setPrev(Node prev) {
        this.prev = prev;
    }
    
    public Node getPrev() {
        return this.prev;
    }
}
