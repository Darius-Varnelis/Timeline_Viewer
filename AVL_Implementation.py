
from datetime import datetime
import re
class Node:
    def __init__(self, startTime,values):
        self.key = startTime
        self.values = values
        self.left = None
        self.right = None
        self.height = 1

    # A utility function to get the
    # height of the tree
def height(node):
    if not node:
        return 0
    return node.height

# A utility function to right rotate
# subtree rooted with y
def right_rotate(y):
    x = y.left
    T2 = x.right

    # Perform rotation
    x.right = y
    y.left = T2

    # Update heights
    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))

    # Return new root
    return x

# A utility function to left rotate
# subtree rooted with x
def left_rotate(x):
    y = x.right
    T2 = y.left

    # Perform rotation
    y.left = x
    x.right = T2

    # Update heights
    x.height = 1 + max(height(x.left), height(x.right))
    y.height = 1 + max(height(y.left), height(y.right))

    # Return new root
    return y

# Get balance factor of node N
def get_balance(node):
    if not node:
        return 0
    return height(node.right) - height(node.left)

# Recursive function to insert a key in
# the subtree rooted with node
def insert(node, startTime, values, endTime = None):

    # Perform the normal BST insertion
    if not node:
        return Node(startTime, values)

    if startTime < node.key:
        node.left = insert(node.left, startTime, values, endTime)
    elif startTime > node.key:
        node.right = insert(node.right, startTime, values, endTime)
    else:
        # Equal keys are not allowed in BST
        return node

    # Update height of this ancestor node
    node.height = 1 + max(height(node.left), height(node.right))

    # Get the balance factor of this ancestor node
    balance = get_balance(node)

    # If this node becomes unbalanced,
    # then there are 4 cases

    # Left Left Case
    if balance < -1 and startTime < node.left.key:
        return right_rotate(node)

    # Right Right Case
    if balance > 1 and startTime > node.right.key:
        return left_rotate(node)

    # Left Right Case
    if balance < -1 and startTime > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)

    # Right Left Case
    if balance > 1 and startTime < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    # Return the (unchanged) node pointer
    return node


def delete_node(root, key):
    # STEP 1: PERFORM STANDARD BST DELETE
    if root is None:
        return root

    # If the key to be deleted is smaller
    # than the root's key, then it lies in
    # left subtree
    if key < root.key:
        root.left = delete_node(root.left, key)

    # If the key to be deleted is greater
    # than the root's key, then it lies in
    # right subtree
    elif key > root.key:
        root.right = delete_node(root.right, key)

    # if key is same as root's key, then
    # this is the node to be deleted
    else:
        # node with only one child or no child
        if root.left is None or root.right is None:
            temp = root.left if root.left else root.right

            # No child case
            if temp is None:
                root = None
            else:  # One child case
                root = temp

        else:
            # node with two children: Get the
            # inorder successor (smallest in
            # the right subtree)
            temp = min_value_node(root.right)

            # Copy the inorder successor's
            # data to this node
            root.key = temp.key
            root.values = temp.values

            # Delete the inorder successor
            root.right = delete_node(root.right, temp.key)

    # If the tree had only one node then return
    if root is None:
        return root

    # STEP 2: UPDATE HEIGHT OF THE CURRENT NODE
    root.height = max(height(root.left),
                      height(root.right)) + 1

    # STEP 3: GET THE BALANCE FACTOR OF THIS
    # NODE (to check whether this node
    # became unbalanced)
    balance = get_balance(root)

    # If this node becomes unbalanced, then
    # there are 4 cases

    # Left Left Case
    if balance < -1 and get_balance(root.left) <= 0:
        return right_rotate(root)

    # Left Right Case
    if balance < -1 and get_balance(root.left) > 0:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    # Right Right Case
    if balance > 1 and get_balance(root.right) >= 0:
        return left_rotate(root)

    # Right Left Case
    if balance > 1 and get_balance(root.right) < 0:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root
def min_value_node(node):
    current = node

    # loop down to find the leftmost leaf
    while current.left is not None:
        current = current.left

    return current

def interval(root, min_value, max_value, values=None):
    '''Funkcija, kuri suranda koordinačių reikšmes, kurios priklauso tam tikram laiko intervalui.'''
    if values is None:
        values = []
    if root is None:
        return values

    if root.key > min_value:
        interval(root.left, min_value, max_value, values)

    if min_value <= root.key <= max_value:
        values.append(root.values)

    if root.key < max_value:
        interval(root.right, min_value, max_value, values)

    return values
def interval_keys(root, min_value, max_value, keys=None):
    '''Funkcija, kuri suranda visas laiko reikšmes duomenyse, kuriose priklauso tam tikram intervalui. Skirta delete_interval funkcijai'''
    if keys is None:
        keys = []
    if root is None:
        return keys

    if root.key > min_value:
        interval_keys(root.left, min_value, max_value, keys)

    if min_value <= root.key <= max_value:
        keys.append(root.key)

    if root.key < max_value:
        interval_keys(root.right, min_value, max_value, keys)

    return keys

def delete_interval(root, min_value, max_value):
    '''Ištrinamas pasirinktas intervalas iš medžio'''
    for key in interval_keys(root, min_value, max_value):
        root = delete_node(root, key)
    return root

def importing_data(file, node=None):
    for entry in file['semanticSegments']:
        if entry.get('timelinePath'):
            for point in entry['timelinePath']:
                node = insert(node, datetime.fromisoformat(point['time']), [float(x) for x in re.findall(r"-?\d+\.?\d*",(point['point']))])
        elif entry.get('activity'):
            node = insert(node, datetime.fromisoformat(entry['startTime']), [float(x) for x in re.findall(r"-?\d+\.?\d*", entry['activity']['start']['latLng'])])
            node = insert(node, datetime.fromisoformat(entry['endTime']), [float(x) for x in re.findall(r"-?\d+\.?\d*", entry['activity']['end']['latLng'])])
        elif entry.get('position'):
            node = insert(node, datetime.fromisoformat(entry['position']['timestamp']), entry['position']['latLng'])
    return node