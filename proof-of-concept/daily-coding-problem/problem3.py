"""
Daily Coding Problem <founders@dailycodingproblem.com> Unsubscribe
	
4:38 PM (43 minutes ago)
	
to me

Good morning! Here's your coding interview problem for today.

This problem was asked by Google.

Given the root to a binary tree, implement serialize(root), which serializes 
the tree into a string, and deserialize(s), which deserializes the string back 
into the tree.

For example, given the following Node class

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

The following test should pass:

node = Node('root', Node('left', Node('left.left')), Node('right'))
assert deserialize(serialize(node)).left.left.val == 'left.left'

"""
import json

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def serialize(node):
    if node:
        return json.dumps({
            'val': node.val,
            'left': serialize(getattr(node, 'left', None)),
            'right': serialize(getattr(node, 'right', None)),
        })
    
    return json.dumps(None)


def deserialize(node_str):
    node = json.loads(node_str)
    if node:
        return Node(
            node['val'],
            deserialize(node['left']),
            deserialize(node['right']))


node = Node('root', Node('left', Node('left.left')), Node('right'))
assert deserialize(serialize(node)).left.left.val == 'left.left'

node2 = Node('root', Node('l1', Node('l2', Node('l3'))), Node('r2'))
assert deserialize(serialize(node2)).left.left.val == 'l2'
assert deserialize(serialize(node2)).left.left.left.val == 'l3'
assert deserialize(serialize(node2)).right.val =='r2'
