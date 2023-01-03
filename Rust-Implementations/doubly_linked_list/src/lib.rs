use std::marker::PhantomData;
use std::ptr::NonNull;

struct Node<T> {
    val: T,
    prev: Option<NonNull<Node<T>>>,
    next: Option<NonNull<Node<T>>>,
}

impl<T> Node<T> {
    fn new(t: T) -> Node<T> {
        Node {
            val: t,
            prev: None,
            next: None
        }
    }
}

struct LinkedList<T> {
    length: u32,
    head: Option<NonNull<Node<T>>>,
    tail: Option<NonNull<Node<T>>>,
    marker: PhantomData<Box<Node<T>>>,
}

impl<T> Default for LinkedList<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> LinkedList<T> {
    pub fn new() -> Self {
        Self {
            length: 0,
            head: None,
            tail: None,
            marker: PhantomData,
        }
    }

    pub fn insert_at_head(&mut self, value: T) {
        let mut node = Box::new(Node::new(value));
        node.next = self.head;
        node.prev = None;
        let node_ptr = Some(unsafe { NonNull::new_unchecked(Box::into_raw(node)) });
        match self.head {
            None => self.tail = node_ptr,
            Some(head_ptr) => unsafe {
                (*head_ptr.as_ptr()).prev = node_ptr
            },
        }
        self.head = node_ptr;
        self.length += 1;
    }
}