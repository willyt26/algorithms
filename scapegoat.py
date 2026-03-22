from abc import ABC, abstractmethod


# ── copied from notebook so this file runs standalone ──────────────────────────
class AbstractSearchInterface(ABC):

    @abstractmethod
    def insertElement(self, element):
        pass

    @abstractmethod
    def searchElement(self, element):
        pass


# ── your node class goes here (auxiliary cell in notebook) ─────────────────────
class ScapeGoatNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# ── your scapegoat tree goes here ─────────────────────────────────────────────
class ScapegoatTree(AbstractSearchInterface):
    def __init__(self):
        self.root = None
        self.size = 0
        self.alpha = 2/3

    def insertElement(self, element):
        inserted = False
        current = self.root
        path = []
        direction = ""
        if self.root is None:
            self.root = ScapeGoatNode(element)
            self.size += 1
            return True
        while not inserted:
            if current is None:
                if direction == "left":
                    path[-1].left = ScapeGoatNode(element)
                elif direction == "right":
                    path[-1].right = ScapeGoatNode(element)
                self.size += 1
                inserted = True
            else:
                path.append(current)
                if current.key == element:
                    return False
                elif current.key > element:
                    direction = "left"
                    current = current.left
                elif current.key < element:
                    direction = "right"
                    current = current.right
        scapegoat = self.findScapeGoat(path)
        if scapegoat is not None:
            nodes = self.getSubtreeNodes(scapegoat)
            balanced_subtree =  self.balanceSubtree(nodes)
            if scapegoat == self.root:
                self.root = balanced_subtree
            else:
                parent = path[path.index(scapegoat) - 1]
                if parent.left == scapegoat:
                    parent.left = balanced_subtree
                elif parent.right == scapegoat:
                    parent.right = balanced_subtree
        return inserted

    def searchElement(self, element):
        found = False
        if self.root is None:
            return False
        current = self.root
        while not found:
            if current is None:
                return False
            elif current.key == element:
                found = True
            elif current.key > element:
                current = current.left
            elif current.key < element:
                current = current.right
        return found

    def findSubtreeSize(self, node):
        if node is None:
            return 0
        return 1 + self.findSubtreeSize(node.left) + self.findSubtreeSize(node.right)

    def findScapeGoat(self, path):
        scapegoat = None
        for node in reversed(path):
            total = self.findSubtreeSize(node)
            if (self.findSubtreeSize(node.left) > self.alpha * total
                    or self.findSubtreeSize(node.right) > self.alpha * total):
                scapegoat = node
                break
        return scapegoat

    def getSubtreeNodes(self, node):
        if node is None:
            return []
        left_list = self.getSubtreeNodes(node.left)
        right_list = self.getSubtreeNodes(node.right)
        return left_list + [node] + right_list

    def balanceSubtree(self, nodes):
        if not nodes:
            return None
        middle = len(nodes) // 2
        left_list = nodes[:middle]
        right_list = nodes[(middle + 1):]
        root = nodes[middle]
        root.left = self.balanceSubtree(left_list)
        root.right = self.balanceSubtree(right_list)
        return root

# ── quick manual tests (delete before moving to notebook) ─────────────────────
