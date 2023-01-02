pub struct DoublyLinkedList {
    head: Box<ListNode>,
    tail: Box<ListNode>,
}

impl DoublyLinkedList {
    pub fn new(value: String) -> DoublyLinkedList {
        let node = ListNode::new(value, None);
        DoublyLinkedList {
            head: Box::new(node),
            tail: Box::new(node),
        }
    }

    pub fn append(&self, value: String) {

    }
}

struct ListNode {
    prev: Option<Box<ListNode>>,
    value: String,
    next: Option<Box<ListNode>>,
}

impl ListNode {
    fn new(value: String, prev: Option<ListNode>) -> ListNode {
        let prev_pointer = match prev {
            None => None,
            Some(node) => Some(Box::new(node)),
        };
        ListNode {
            prev: prev_pointer,
            value,
            next: None,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /*#[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    } */
}
