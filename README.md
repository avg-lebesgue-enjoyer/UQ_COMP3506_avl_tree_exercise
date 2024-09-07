# Instructions

## To students
1. Download the `BASE_FILES/` folder. You can `git clone` if you want, but it might be a nightmare later on when merge conflicts happen...
2. Have a look at `avl.py`'s `## SECTION: Instructions` section, and follow what it says.
3. With ~10 minutes, implement `[2.] Binary Search Tree`.
4. With ~5 minutes, test your `[2.] Binary Search Tree` using `avl_test.py`. Do you fail any tests? If so, how could you fix them up?
5. Grab a model `[2.]` solution (will be posted once step (4.) is done). Work off this one from now on.
6. With ~20 minutes, implement the `[3.] helper methods`. Try to test methods individually as you go (don't use `avl_test.py`) so that you really learn something!
7. Grab a model `[3.]` solution (will be posted once step (6.) is done).
8. With ~20 minutes, collaborate as a class to implement `Node.tri_node_restructuring()`. Have a good look at the `HINT:`s provided! This method can get really messy, and can have lots of little bugs if you don't do it very carefully...!
9. Grab a model `[4.]` solution (will be posted once step (8.) is done).
10. Test it out! Try to break my code :)

## To tutor
1. Have students come to this repo and download the `BASE_FILES/` folder.
2. Walk students through the instructions in `avl.py`'s `## SECTION: Instructions` section.
3. Allocate ~10 minutes to implement `[2.] Binary Search Tree`. This includes:
  - `AVLTree.__init__()`
  - `Node.insert()`
  - `AVLTree.insert()`
  - `Node.find()`
  - `AVLTree.find()`
4. Have students TEST their tree (~5 mins).
5. Release `[2.]` solution to students. Have them TEST their
6. Allocate ~20 minutes to implement the `[3.] helper methods`:
  - `Node.get_highest_child()`
  - `Node.fix_heights_after_insertion()`
  - `Node.rebalance()`
  - `AVLTree.insert()` (fix this method so that it attempts to re-balance whenever necessary.)
7. Release `[3.]` solution to students.
8. Spend ~20 mins collaboratively working through `Node.tri_node_restructuring()` so that we get a `[4.] AVLTree` working. Points to think about:
  - What shapes could the pointers between `self`, `highest_child` and `highest_childs_highest_child` look like? What are the four different cases here? Draw them out!
  - What needs to happen with all the child-pointers among `self`, `highest_child` and `highest_childs_highest_child` in each case?
  - What needs to happen with all the `.parent` pointers?
  - Where do we re-connect the subtrees in each case?
  - Which nodes might need their `.height` updated in each case?
  - If `self.parent is None`, then we're tri-node-restructuring with the root. How can we account for this to make sure that the `AVLTree.root` points to the correct node after restructuring?
9. Release `[4.]` solution to students.
10. Test it! Make sure it all works :)
