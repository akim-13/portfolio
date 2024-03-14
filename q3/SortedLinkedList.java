public class SortedLinkedList implements SortedList {
    private Node last;
    private Node first;
    private static boolean orderIsAscending = true;

    public SortedLinkedList() {
        this.last = null; 
        this.first = null;
    }

    public static void main(String[] args) {
        SortedLinkedList list = new SortedLinkedList();
        list.add("abc");
        list.add("abccc");
        list.add("abc");
        list.add("abCc");
        Node nd = new Node("zzz");
        list.add(nd);
        list.add(new Node(nd, "hiii"));
        list.print();
        System.out.println(list.size());
        System.out.println();
        System.out.println(list.remove(4));
        System.out.println(list.remove("abc"));
        System.out.println(list.remove("abccc"));
        System.out.println(list.remove("abCc"));
        System.out.println(list.remove("hiii"));
        System.out.println(list.remove("hiii"));
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
        if (curNode == null) {
            return;
        }
        Node newNode = new Node(curNode, string);
        Node nextNode = curNode.getNext();
        curNode.setNext(newNode);
        newNode.setNext(nextNode);
        if (nextNode != null) {
            nextNode.setPrev(newNode); 
        } else {
            this.last = newNode;
        }
    }

    private void insertNodeBeforeGiven(Node curNode, String string) {
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
            this.first = newNode;
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
        if (this.first == null) {
            Node newNode = new Node(string);
            this.last = newNode;
            this.first = newNode;
            return;
        }

        Node curNode = this.first;

        while (curNode != null) {
            int compareResult = string.compareToIgnoreCase(curNode.getString());
            boolean foundPlaceBefore = compareResult < 0;
            boolean stringsAreEqual = compareResult == 0;
            if (foundPlaceBefore) {
                if (SortedLinkedList.orderIsAscending) {
                    insertNodeBeforeGiven(curNode, string);
                } else {
                    insertNodeAfterGiven(curNode, string);
                }
                return;
            } else if (stringsAreEqual) {
                return;
            }
            curNode = curNode.getNext();
        }

        insertNodeAfterGiven(this.last, string);
    }

    /**
    * Adds a Node to the linked list in the appropriate position
    * given the specified alphabetical order (i.e., ascending/descending).
    *
    * @param  node  a Node to be added to the linked list
    */
    @Override
    public void add(Node node) {
        if (node == null) {
            return;
        }

        add(node.getString());

        Node prevNode = node.getPrev();
        while (prevNode != null) {
            add(prevNode.getString());
            prevNode = prevNode.getPrev();
        }

        Node nextNode = node.getNext();
        while (nextNode != null) {
            add(nextNode.getString());
            nextNode = nextNode.getNext();
        }
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
        if (index < 0 || index >= size()) {
            return false;
        }

        if (index == 0) {
            if (size() == 1) {
                this.first = null;
                this.last = null;
                return true;
            }
            Node nextNode = this.first.getNext();
            this.first.setNext(null);
            this.first = nextNode;
            this.first.setPrev(null);
        } else if (index == size() - 1) {
            Node prevNode = this.last.getPrev();
            this.last.setPrev(null);
            this.last = prevNode;
            this.last.setNext(null);
        } else {
            Node curNode = this.first;
            for (int i = 0; i != index; i++) {
                curNode = curNode.getNext();
            }
            Node prevNode = curNode.getPrev();
            Node nextNode = curNode.getNext();
            curNode.setNext(null);
            curNode.setPrev(null);
            prevNode.setNext(nextNode);
            nextNode.setPrev(prevNode);
        }

        return true;
    }

    /**
    * Removes the Node from the list that contains the specified string.
    *
    * @param  string  the string to be removed from the linked list
    * @return      Returns true if successful or false if unsuccessful
    */
    @Override
    public boolean remove(String string) {
        Node curNode = this.first;
        int size = size();
        for (int i = 0; i < size; i++) {
            if (curNode.getString().equals(string)) {
                remove(i);
                return true;
            }
            curNode = curNode.getNext();
        }
        return false;
    }

    public void reverseOrder() {
        Node curNode = this.first;
        while (curNode != null) {
            Node nextNode = curNode.getNext();
            Node prevNode = curNode.getPrev();
            curNode.setPrev(nextNode);
            curNode.setNext(prevNode);
            curNode = nextNode;
        }
        Node firstNode = this.first;
        this.first = this.last;
        this.last = firstNode;
    }

    /**
    * Orders the linked list in ascending alphabetical order.
    *
    */
    @Override
    public void orderAscending() {
        boolean orderIsCorrect = orderIsAscending || size() < 2;
        if (orderIsCorrect) {
            return;
        }

        reverseOrder();
        SortedLinkedList.orderIsAscending = true;
    }

    /**
    * Orders the linked list in descending alphabetical order.
    *
    */
    @Override
    public void orderDescending() {
        boolean orderIsCorrect = !orderIsAscending || size() < 2;
        if (orderIsCorrect) {
            return;
        }

        reverseOrder();
        SortedLinkedList.orderIsAscending = false;
    }

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
