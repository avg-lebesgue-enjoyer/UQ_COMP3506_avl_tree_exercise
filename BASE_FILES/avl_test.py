"""
@file avl_test.py
@author Gabriel Field (uqgfiel1)
Tests for avl.py
"""

## SECTION: Imports

import random as random

from avl import *



## SECTION: main()

TESTING_AVL_STRUCTURE = False # NOTE: Change this to `True` once you're ready to test your rebalancing!

def main():
  tree : AVLTree = AVLTree()
  """ Tree we're testing with. """
  history : list[str] = []               # Values: "i k v" (insert k v), "f k" (find k), "r k" (remove k)
  """ This will store the history of operations done to `tree`. """
  association_list : list[int, Any] = [] # Entries: (k, v) pairs where `tree.find(k)` should give something `== v`
  """ This will store a reference map to compare against. """
  
  print("<?> TEST: Empty tree...")
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: One node...")
  do(tree, "i", 0, "a", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: One node, new value...")
  do(tree, "i", 0, "aa", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: Two nodes...")
  do(tree, "i", 1, "b", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: Three nodes...")
  do(tree, "i", 2, "c", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> TEST: Three nodes, new value...")
  do(tree, "i", 2, "c'", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> TEST: Four nodes...")
  do(tree, "i", 3, "d", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> TEST: Five nodes...")
  do(tree, "i", 4, "e", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> TEST: Six nodes...")
  do(tree, "i", -1, "z", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> TEST: Seven nodes...")
  do(tree, "i", -2, "y", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: Eight nodes...")
  do(tree, "i", -3, "x", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)

  print("<?> TEST: Eight nodes, changing up key 0...")
  do(tree, "i", 0, "amon gus", history, association_list)
  print_tree(tree)
  test(tree, association_list, history)
  
  print("<?> ALL TESTS PASSED :)")


def do(
    tree : AVLTree, 
    operation : str, key : int, value : Any, 
    history : list[str], 
    association_list : list[int, Any]
) -> None:
  """
  Do the `operation` on the `tree`, update the `history` of operations, and update the 
  reference `association_list`. 
  
  `operation` can be "i" (insert) or "r" (remove).
  """
  if operation == "i":
    # Update history
    history.append(f"i {key} {value}")
    # Update association list
    maybeEntry = association_list_find_entry(association_list, key)
    if maybeEntry is not None:
      association_list.remove(maybeEntry)
    association_list.append((key, value))
    # Perform action on tree
    tree.insert(key, value)
  elif operation == "r":
    # Update history
    history.append(f"r {key}")
    # Update association list
    maybeEntry = association_list_find_entry(association_list, key)
    if maybeEntry is not None:
      association_list.remove(maybeEntry)
    # Perform action on tree
    tree.remove(key)
  else:
    # BAD TEST HARNESS; THIS CASE SHOULD NOT OCCUR!
    print("<!> FATAL: Test harness tried to do an invalid operation.")
    assert False

def association_list_find_entry(association_list : list[int, Any], key : int) -> tuple[int, Any] | None:
  """
  Return None if there is no entry in the given `association_list` matching the given `key`.
  If there is such an entry, return it.
  If there is more than one match, halt execution of the program.
  """
  matches = [(k, v) for (k, v) in association_list if k == key]
  if len(matches) > 1:
    print("<!> FATAL: Test harness has multiple matching pairs in the association list with the same key.")
    assert False
  if len(matches) == 1:
    return matches[0]
  return None

def test(tree : AVLTree, association_list : list[int, Any], history : list[str]) -> None:
  """
  Test the given `tree`. Ensure that:
    It is a binary search tree
    Every node is balanced
    It has `len(association_list)` nodes
    All pairs (k, v) in `association_list` have `tree.find(k) == v`
  Raise an AssertionError otherwise.
  """
  print("\t<?> Is binary search tree...")
  good = tree.is_binary_search_tree()
  if not good:
    fail_out(association_list, history)
  
  if TESTING_AVL_STRUCTURE:
    print("\t<?> Is balanced at every node...")
    good = tree.is_everywhere_balanced()
    if not good:
      fail_out(association_list, history)
  
  print("\t<?> Has " + str(len(association_list)) + " nodes...")
  good = tree.compute_number_of_nodes() == len(association_list)
  if not good:
    fail_out(association_list, history)

  print("\t<?> Matches the reference association list...")
  for (key, value) in association_list:
    print("\t\t<?> Key " + str(key) + ":")

    found_value = tree.find(key)
    print("\t\t\t<?> finds a value")
    good = found_value is not None
    if not good:
      fail_out(association_list, history)

    print("\t\t\t<?> and this value is " + str(value))
    good = found_value == value
    if not good:
      fail_out(association_list, history)

def fail_out(association_list : list[int, Any], history : list[str]) -> None:
  """
  Print debug info and immediately halt execution.
  """
  print("<!> FAILED.")
  print("<!> Operation history: " + str(history))
  print("<!> Association list: " + str(association_list))
  assert False

def print_tree(tree : AVLTree) -> None:
  """
  Print the tree and a debug message
  """
  print("<!> Tree looks like:")
  print(tree)




## LAUNCH

if __name__ == "__main__":
  main()
