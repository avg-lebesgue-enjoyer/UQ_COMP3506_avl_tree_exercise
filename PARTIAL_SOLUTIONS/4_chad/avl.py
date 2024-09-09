"""
@file avl.py
@author YOUR CODE HERE!  # Your name!
@author Gabriel Field (uqgfiel1)
Exercise for building an AVL tree in code.
"""
## SECTION: Imports

from __future__ import annotations
from typing import Any



## SECTION: Instructions
"""
[1.] Carefully read all the code you have been provided.
Ensure that you understand what the provided code *does*.
You may skip reading the things that say "IGNORE ME:".



[2.] Implement a BINARY SEARCH TREE by implementing following methods. Do them in whatever order you would like.
Node:
  insert(self, key : int, value : Any) -> tuple[bool, Node]:
    Insert into the subtree starting at this node.
    Returns:
      (bool): True just when a NEW node was inserted
      (Node): The changed/inserted node
    WARNING: This method does not fix the heights of the parents!
    WARNING: This method does not rebalance the tree!

  find(self, key : int) -> Any | None:
    Find the value in the subtree rooted at this Node matching the given `key`.
    Return None if there is no node in this subtree matching the given `key`.

AVLTree:
  __init__(self) -> AVLTree
    Create a new empty AVL tree.
  
  insert(self, key : int, value : Any) -> None
    Insert a value into this AVL tree, associated to a node with the given key.
    If a node with that key already exists, override the value in that node.
    If a node with that key does not exist, create a new node.
    Ensure that your tree remains balanced (eventually, when you implement the *AVL* tree)
  
  find(key : int) -> Any | None
    If there is a node with the given key, then return its value.
    Otherwise, return None.

Your tree does not need to support a remove(self, key : int) -> None, because
I couldn't be bothered to write a solution for that myself lol. As an extension
exercise, add such a method!



[3.] Get some helper methods working, towards an implementation of an AVL tree.
Do them in whatever order you would like.
Once step [3.] is done, you WILL NOT have a functional AVL tree; we will be missing
tri-node restructuring.

Node:
  get_highest_child(self) -> Node | None
    Get the highest child of this node.
    If this node has no children, return None instead.
  
  fix_heights_after_insertion(self) -> None:
    Assumes that this Node's height was just updated
    (e.g. if this Node was just freshly inserted into the AVL tree).
    This method will fix the heights of the ancestors of this Node,
    to account for the fact that these ancestors might be higher.

  rebalance(self) -> None
    Rebalance the tree, seeking up from this Node.

AVLTree:
  insert() needs to be fixed so that it calls `Node.rebalance()` when necessary.

  

[4.] Implement tri_node_restructuring, collaboratively as a class.
This method is kinda disgusting...
Once step [4.] is done, you SHOULD have a functional AVL tree, and can test it out.
Ensure that you set `TESTING_AVL_STRUCTURE = True` when you test your AVL tree.

AVLTree:
  tri_node_restructuring(self) -> None
    Assumes that this Node is not balanced.
    Rebalance the tree by tri-node restructuring:
      this Node,
      this Node's highest child,
      this Node's highest child's highest child.



[5.] Notes:
I have provided two "class invariant" methods in AVLTree so that you can check whether
your AVL tree is indeed a valid AVL tree at any point in time. These methods are used
extensively in `avl_test.py`.

**To find code that you need to implement, search for "YOUR CODE HERE!" in this file.**

To test your code, run `python avl_test.py`.
  When testing your [2.] BINARY SEARCH TREE, keep `TESTING_AVL_STRUCTURE = False` (line 17).
  When testing your [4.] AVL TREE, set `TESTING_AVL_STRUCTURE = True` (line 17).
"""



## SECTION: Node

# NOTE: Helpful function for returning the height of a POSSIBLY UNINITIALISED node.
def real_height(maybe_node : Node | None) -> int:
  """
  Return the height of a Node. 
  If the provided node is a None-pointer, then it'll have height 0.
  """
  if maybe_node is None:
    return 0
  return maybe_node.height

class Node:
  # NOTE: Member variables
  parent : Node | None
  """ Parent of this Node """
  left   : Node | None
  """ Left child of this Node """
  right  : Node | None
  """ Right child of this Node """
  key    : int
  """ Key at this Node """
  value  : Any
  """ Value stored at this Node """
  height : int
  """
  Height of this Node in its tree.
  A leaf is at height ONE.
  (fwiw, a None-pointer "Node" is at height zero.)
  WARNING: Make sure that this stays up-to-date as you re-balance your tree!
  """

  # NOTE: Constructor
  def __init__(self, parent : Node | None, key : int, value : Any) -> Node:
    """
    Create a new LEAF node with a given parent, key and value.
    """
    self.parent = parent
    self.left   = None
    self.right  = None
    self.height = 1       # NOTE: Leaf nodes have height 1
    self.key    = key
    self.value  = value

  # IGNORE ME: Helper for AVLTree class invariant methods.
  def is_binary_serach_tree(
      self, 
      key_strict_lower_bound : int | None,   # None acts as -\infty
      key_strict_upper_bound : int | None    # None acts as +\infty
  ) -> bool:
    # Validate bounds on this node
    def real_less_check(x : int | None, y : int | None) -> bool:
      if x is None and y is None:
        return True
      if y is None:
        return True
      if x is None:
        return True
      return x < y
    if (not (
      real_less_check(key_strict_lower_bound, self.key) 
      and real_less_check(self.key, key_strict_upper_bound)
    )):
      return False
    # Check bounds for left subtree
    if self.left is not None:
      if not self.left.is_binary_serach_tree(key_strict_lower_bound, self.key):
        return False
    # Check bounds for right subtree
    if self.right is not None:
      if not self.right.is_binary_serach_tree(self.key, key_strict_upper_bound):
        return False
    # All checks pass
    return True
  
  # IGNORE ME: Helper for AVLTree class invariant methods.
  def compute_height(self) -> int:
    def compute_real_height(maybeNode : Node | None) -> int:
      """
      Returns the height of a Node, or a None-pointer.
      A "missing node" (None) has height 0.
      NOTE: This nested function is not very befitting of a C-like algos course...
      """
      if maybeNode is None:
        return 0
      return maybeNode.compute_height()
    return max(compute_real_height(self.left), compute_real_height(self.right)) + 1

  # IGNORE ME: Helper for AVLTree class invariant methods.
  def compute_subtree_balanced(self) -> bool:
    # Check that this node is balanced
    def compute_real_height(maybeNode : Node | None) -> int:
      """
      Returns the height of a Node, or a None-pointer.
      A "missing node" (None) has height 0.
      NOTE: This nested function is not very befitting of a C-like algos course...
      """
      if maybeNode is None:
        return 0
      return maybeNode.compute_height()
    if not (abs(compute_real_height(self.left) - compute_real_height(self.right)) <= 1):
      return False
    # Check that the left subtree is always balanced
    if self.left is not None:
      if not self.left.compute_subtree_balanced():
        return False
    # Check that the right subtree is always balanced
    if self.right is not None:
      if not self.right.compute_subtree_balanced():
        return False
    # All checks pass
    return True

  # IGNORE ME: Print this node and its children
  def print_me(self, padding : str) -> str:
    return_me = ""
    if self.left is not None:
      return_me += self.left.print_me("\t" + padding) + "\n"
    return_me += padding + f"(k: {self.key}, v: {self.value}; h: {self.height})" + "\n"
    if self.right is not None:
      return_me += self.right.print_me("\t" + padding) + ""
    return return_me

  # IGNORE ME: Helper for finding the number of nodes in a tree.
  def compute_number_of_nodes_downstream(self) -> int:
    left_total  = (0 if self.left  is None else self.left.compute_number_of_nodes_downstream())
    right_total = (0 if self.right is None else self.right.compute_number_of_nodes_downstream())
    return left_total + 1 + right_total

  # NOTE: Helper method
  def is_balanced(self) -> bool:
    """
    Return True just when this node is balanced; i.e. when its children's heights
    differ by at most 1.
    """
    return abs(real_height(self.left) - real_height(self.right)) <= 1
  
  # [3.] NOTE: Helper method
  def get_highest_child(self) -> Node | None:
    """
    Get the highest child of this node.
    If this node has no children, return None instead.
    """
    if self.left is None and self.right is None:
      return None
    if self.left is None: # and self.right is not None
      return self.right
    if self.right is None: # and self.left is not None
      return self.left
    # Both children exist; grab the higher one (break ties arbitrarily by right child)
    if self.left.height > self.right.height:
      return self.left
    return self.right

  # [2.] NOTE: Helper method for inserting to a tree
  def insert(self, key : int, value : Any) -> tuple[bool, Node]:
    """
    Insert into the subtree starting at this node.
    Returns:
      (bool): True just when a NEW node was inserted
      (Node): The changed/inserted node
    WARNING: This method does not fix the heights of the parents!
    WARNING: This method does not rebalance the tree!
    """
    if self.key == key:
      self.value = value
      return (False, self)
    if key < self.key:
      # Insert into left subtree
      if self.left is None:
        self.left = Node(self, key, value)
        return (True, self.left)
      return self.left.insert(key, value)
    if self.key < key:
      # Insert into right subtree
      if self.right is None:
        self.right = Node(self, key, value)
        return (True, self.right)
      return self.right.insert(key, value)
    # NOTE: The three "if" statements above cover all possible cases.
  
  # [3.] NOTE: Helper method for inserting to a tree
  def fix_heights_after_insertion(self) -> None:
    """
    Assumes that this Node's height was just updated
    (e.g. if this Node was just freshly inserted into the AVL tree).
    This method will fix the heights of the ancestors of this Node,
    to account for the fact that these ancestors might be higher.
    """
    if self.parent is None:
      return    
    self.parent.height = max(real_height(self.parent.left), real_height(self.parent.right)) + 1
    self.parent.fix_heights_after_insertion()
  
  # [2.] NOTE: Helper method for looking up in a tree
  def find(self, key : int) -> Any | None:
    """
    Find the value in the subtree rooted at this Node matching the given `key`.
    Return None if there is no node in this subtree matching the given `key`.
    """
    if self.key == key:
      return self.value
    if self.left is not None:
      lookup = self.left.find(key)
      if lookup is not None:
        return lookup
    if self.right is not None:
      lookup = self.right.find(key)
      if lookup is not None:
        return lookup
    return None

  # [3.] NOTE: Helper method for rebalancing a tree
  def rebalance(self, tree : AVLTree) -> None:
    """
    Rebalance the tree this node is part of, by restructuring this node or one of its ancestors,
    if any of them are unbalanced.

    Args:
      (tree : AVLTree)
        The tree this node is a part of
    """
    # HINT:
    #   Find the closest ancestor of this node which is not balanced (potentially this node itself)
    #   Call tri_node_restructuring on this ancestor
    if not self.is_balanced():
      print("<!> Rebalancing key " + str(self.key))
      self.tri_node_restructuring(tree)
    elif self.parent is not None:
      self.parent.rebalance(tree)
  
  # [4.] NOTE: Helper method for rebalancing a tree
  def tri_node_restructuring(self, tree : AVLTree) -> None:
    """
    WARNING: Assumes that this Node is not balanced.
    Rebalance the tree by tri-node restructuring:
      this Node,
      this Node's highest child,
      thisNode's highest child's highest child.
    
    Args:
      (tree : AVLTree)
        The tree this node is a part of
    """
    # HINT:
    #   When finding the highest children, keep track of whether they are:
    #                self                            self
    #            child          or       child                 etc.
    #     grandchild                        grandchild
    #   so that your re-structuring is easy to determine.
    #   Draw out the different cases on paper!
    #     Ensure that you know exactly what needs to happen with `self`, `child` and `grandchild`
    #     Ensure that you know exactly what needs to happen with reconnecting the subtrees!
    parent = self.parent
    highest_child = self.get_highest_child()
    highest_childs_highest_child = highest_child.get_highest_child()
    if highest_child.key < self.key:
      # highest_child on the left
      #   self
      # hc
      if highest_childs_highest_child.key < highest_child.key:
        #               parent                      
        #                self                        parent
        #         hc          d       -->              hc   
        #   hchc      c                         hchc        self
        # a      b                            a      b    c      d
        a = highest_childs_highest_child.left
        b = highest_childs_highest_child.right
        c = highest_child.right
        d = self.right
        # Fix up the parent --> self pointer to become a parent --> highest_child pointer
        if parent is not None:
          if self.key < parent.key: # self is parent.left
            parent.left  = highest_child
          else: # self is parent.right
            parent.right = highest_child
        else:
          # This node is the ROOT of `tree`. Make sure to update `tree.root`...
          tree.root = highest_child
        # Restructure the three nodes and the subtrees a, b, c, d.
        highest_child.left   = highest_childs_highest_child
        highest_child.right  = self
        highest_child.parent = parent
        highest_childs_highest_child.left   = a
        highest_childs_highest_child.right  = b
        highest_childs_highest_child.parent = highest_child
        self.left   = c
        self.right  = d
        self.parent = highest_child
        # Fix the heights (again)
        self.height = max(real_height(self.left), real_height(self.right)) + 1
        self.fix_heights_after_insertion()
      elif highest_child.key < highest_childs_highest_child.key:
        #              parent                         
        #               self                          parent
        #   hc               d       -->               hchc 
        # a     hchc                               hc        self
        #     b      c                            a  b      c    d
        a = highest_child.left
        b = highest_childs_highest_child.left
        c = highest_childs_highest_child.right
        d = self.right
        # Fix up the parent --> self pointer to become a parent --> hchc pointer
        if parent is not None:
          if self.key < parent.key: # self is parent.left
            parent.left  = highest_childs_highest_child
          else: # self is parent.right
            parent.right = highest_childs_highest_child
        else:
          # This node is the ROOT of `tree`. Make sure to update `tree.root`...
          tree.root = highest_childs_highest_child
        # Restructure the three nodes and the subtrees a, b, c, d
        highest_childs_highest_child.left   = highest_child
        highest_childs_highest_child.right  = self
        highest_childs_highest_child.parent = parent
        highest_child.left  = a
        highest_child.right = b
        highest_child.parent = highest_childs_highest_child
        self.left  = c
        self.right = d
        self.parent = highest_child
        # Fix the heights (again)
        highest_child.height = max(real_height(highest_child.left), real_height(highest_child.right)) + 1
        self.height          = max(real_height(self.left),          real_height(self.right))          + 1
        self.fix_heights_after_insertion()
      else:
        # THIS CASE SHOULD NOT OCCUR.
        assert("<!> FATAL ERROR. DUPLICATE KEY IN THE TREE.")
    elif self.key < highest_child.key:
      # highest_child on the right
      # self
      #      hc
      if highest_childs_highest_child.key < highest_child.key:
        #  parent                             
        #   self                              parent
        # a             hc         -->         hchc
        #        hchc       d             self       hc
        #      b      c                  a    b     c  d
        a = self.left
        b = highest_childs_highest_child.left
        c = highest_childs_highest_child.right
        d = highest_child.right
        # Fix up the parent --> self pointer to be a parent --> hchc pointer
        if parent is not None:
          if self.key < parent.key: # self is parent.left
            parent.left  = highest_childs_highest_child
          else: # self is parent.right
            parent.right = highest_childs_highest_child
        else:
          # This node is the ROOT of `tree`. Make sure to update `tree.root`...
          tree.root = highest_childs_highest_child
        # Restructure the three nodes and the subtrees a, b, c, d
        highest_childs_highest_child.left   = self
        highest_childs_highest_child.right  = highest_child
        highest_childs_highest_child.parent = parent
        self.left   = a
        self.right  = b
        self.parent = highest_childs_highest_child
        highest_child.left   = c
        highest_child.right  = d
        highest_child.parent = highest_childs_highest_child
        # Fix the heights (again)
        highest_child.height = max(real_height(highest_child.left), real_height(highest_child.right)) + 1
        self.height          = max(real_height(self.left),          real_height(self.right))          + 1
        self.fix_heights_after_insertion()
      elif highest_child.key < highest_childs_highest_child.key:
        #   parent                                  
        #    self                                    parent
        #  a        hc               -->               hc
        #         b      hchc                  self          hchc
        #              c      d              a      b      c      d
        a = self.left
        b = highest_child.left
        c = highest_childs_highest_child.left
        d = highest_childs_highest_child.right
        # Fix up the parent --> self pointer to be a parent --> highest_child pointer
        if parent is not None:
          if self.key < parent.key: # self is parent.left
            parent.left  = highest_child
          else: # self is parent.right
            parent.right = highest_child
        else:
          # This node is the ROOT of `tree`. Make sure to update `tree.root`...
          tree.root = highest_child
        # Restructure the three nodes and the subtrees a, b, c, d
        highest_child.left   = self
        highest_child.right  = highest_childs_highest_child
        highest_child.parent = parent
        self.left   = a
        self.right  = b
        self.parent = highest_child
        highest_childs_highest_child.left   = c
        highest_childs_highest_child.right  = d
        highest_childs_highest_child.parent = highest_child
        # Fix the heights (again)
        self.height = max(real_height(self.left), real_height(self.right)) + 1
        self.fix_heights_after_insertion()
      else:
        # THIS CASE SHOULD NOT OCCUR.
        print("<!> FATAL ERROR. DUPLICATE KEY IN THE TREE.")
        assert False
    else:
      # THIS CASE SHOULD NOT OCCUR.
      print("<!> FATAL ERROR. DUPLICATE KEY IN TREE.")
      assert False



## SECTION: AVLTree

class AVLTree:
  # NOTE: Member variables
  root : Node | None
  """ Root of this AVLTree """

  # [2.] NOTE: Constructor
  def __init__(self) -> AVLTree:
    """
    Create a new, empty AVLTree
    """
    self.root = None

  # NOTE: Class invariant
  def is_binary_search_tree(self) -> bool:
    """
    Return True just when this tree is a BINARY SEARCH tree.
    """
    if self.root is None:
      return True
    return self.root.is_binary_serach_tree(None, None)
  
  # NOTE: Class invariant
  def is_everywhere_balanced(self) -> bool:
    """
    Return True just when this tree is a balanced
    """
    if self.root is None:
      return True
    return self.root.compute_subtree_balanced()
  
  # [2.], [3.] NOTE: Insertion
  def insert(self, key : int, value : Any) -> None:
    """
    Insert a value into this AVL tree, associated to a node with the given key.
    If a node with that key already exists, override the value in that node.
    If a node with that key does not exist, create a new node.
    Ensure that your tree remains balanced.
    """
    # HINT: 
    #   Find either the node with the given key, or where this node should go.
    #   You can use the binary search tree property to help here!
    # HINT:
    #   If you have to create a new node, then you might need to rebalance the tree.
    #   Check out Node.rebalance() for this.
    if self.root is None:
      self.root = Node(None, key, value)
      return
    (inserted_new_node, changed_node) = self.root.insert(key, value)
    if inserted_new_node:
      changed_node.fix_heights_after_insertion()
      changed_node.rebalance(self)
  
  # [2.] NOTE: Find
  def find(self, key : int) -> Any | None:
    """
    If there is a node with the given key, then return its value.
    Otherwise, return None.
    """
    if self.root is None:
      return None
    return self.root.find(key)      
  
  # IGNORE ME: Calculate number of nodes in this tree.
  def compute_number_of_nodes(self) -> int:
    return (0 if self.root is None else self.root.compute_number_of_nodes_downstream())

  # IGNORE ME: Print this tree
  def __str__(self) -> str:
    if self.root is None:
      return "\t(empty AVLTree)"
    return self.root.print_me("\t")
