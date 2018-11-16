# Ph360 Assignment 1: Singly Linked List
# Jing Jiang

#functionality part
class Node(object):
    """the Node class"""
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList(object):
    """the Linked List class"""
    def __init__(self):
        self.head = None

    def show(self):
        """print all the nodes in a linked list, if empty, print that it is empty"""
        list_index = self.head
        if list_index is None:
            print("this list is empty!")
        while list_index is not None:
            print(list_index.data, end='')
            if list_index.next is None:
                print()
            else:
                print(" --> ", end='')
            list_index = list_index.next

    def __len__(self):
        list_index = self.head
        length = 0
        while list_index is not None:
            length += 1
            list_index = list_index.next
        return length

    def add_to_head(self, data):
        """add item to the head of the list"""
        node = Node(data)
        node.next = self.head
        self.head = node

    def append(self, data):
        """add item to the tail of the list"""
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            list_index = self.head
            while list_index.next is not None:
                list_index = list_index.next
            list_index.next = node

    def insert(self, index, data):
        """insert an item to a certain index in the list"""
        node = Node(data)
        if index > len(self) or index < 0:
            print("input invalid for insert func!")
            return False
        if index == 0:
            node.next = self.head
            self.head = node
        if index == len(self):
            self.append(data)
            return node
        p = self.head
        j = 0
        while p.next is not None:
            p_temp = p
            p = p.next
            j += 1
            if index == j:
                temp_next = p_temp.next
                p_temp.next = node
                node.next = temp_next
                break
        return node

    def delete(self, index):
        """delete an item at a certain index in the list"""
        if abs(index + 1) > len(self) or index < 0:
            print("input invalid for delete func!")
            return False
        if index == 0:
            self.head = self.head.next
        p = self.head
        j = 0
        while p.next is not None:
            p_temp = p
            p = p.next
            j += 1
            if index == j:
                p_temp.next = p_temp.next.next
                break
        return p.next

    def clone(self):
        """deep copy of the list (imported the copy module)"""
        from copy import deepcopy
        return deepcopy(self)

    def get_reversed(self):
        """reverse the list"""
        def reverse(pre_node, node):
            if pre_node is self.head:
                pre_node.next = None
            if node:
                next_node = node.next
                node.next = pre_node
                return reverse(node, next_node)
            else:
                self.head = pre_node

        return reverse(self.head, self.head.next)

    def clear_all(self):
        """clear all by setting head to None"""
        self.head = None


#output part
if __name__ == '__main__':
    ls = SinglyLinkedList()
    ls.append("A")
    ls.append("B")
    ls.append("C")
    ls.append("D")
    ls.append("E")
    ls.append("F")
    ls.append("G")
    ls.append("H")
    ls.append("I")
    ls.append("J")

    import sys

    with open("assignment1_JingJiang_output.txt", "w") as f:
        sys.stdout = f

        print("now a 10-item linked list will be created")
        ls.show()
        print("\n")
        ls.insert(3, "K")
        print("now K will be inserted as the 3rd node (counting from 0, or the 4th node if counting from 1)")
        ls.show()
        print("\n")
        ls.delete(1)
        print("now the 1st node (B) (counting from 0) will be deleted.")
        ls.show()
        print("\n")
        ls.get_reversed()
        print("now the linked list will be reversed.")
        ls.show()
        print("\n")
        ls.add_to_head("L")
        print("now L will be added to the head of the list")
        ls.show()
        print("\n")
        ls.append("M")
        print("now M will be added to the tail of the list")
        ls.show()
        print("\n")
        ls2 = ls.clone()
        print("now the original linked list ls is deepcopied to ls2")
        ls2.show()
        print("\n")
        ls.insert(7, "N")
        print("now if the original linked list ls is changed (adding a node N), the deepcopied ls2 won't change")
        ls.show()
        ls2.show()
        print("\n")
        ls.clear_all()
        print("now the original linked list is cleared")
        ls.show()