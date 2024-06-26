import os
import time
import csv

# Definição da classe para a árvore AVL
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def search(self, root, key):
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.search(root.right, key)
        return self.search(root.left, key)

# Definição da classe para a árvore Rubro-Negra
class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1

class RBTree:
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = 0
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def insert(self, key):
        node = RBNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fixInsert(node)

    def fixInsert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rightRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.leftRotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.leftRotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rightRotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x.parent.right == y:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def searchTree(self, k):
        return self.searchTreeHelper(self.root, k)

    def searchTreeHelper(self, node, key):
        if node == self.TNULL or key == node.key:
            return node
        if key < node.key:
            return self.searchTreeHelper(node.left, key)
        return self.searchTreeHelper(node.right, key)

# Função para medir tempo e comparações
def measure_performance(tree, elements):
    comparisons = 0
    start_time = time.time()

    root = None
    for element in elements:
        if isinstance(tree, AVLTree):
            root = tree.insert(root, element)
        elif isinstance(tree, RBTree):
            tree.insert(element)
        comparisons += 1

    end_time = time.time()
    construction_time = end_time - start_time

    search_comparisons = 0
    start_time = time.time()

    for element in elements:
        if isinstance(tree, AVLTree):
            tree.search(root, element)
        elif isinstance(tree, RBTree):
            tree.searchTree(element)
        search_comparisons += 1

    end_time = time.time()
    search_time = end_time - start_time

    return {
        'construction_comparisons': comparisons,
        'construction_time': construction_time,
        'search_comparisons': search_comparisons,
        'search_time': search_time
    }

# Função para ler arquivos de texto e extrair elementos
def read_elements_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            elements = file.readlines()
        elements = [int(element.strip()) for element in elements if element.strip().isdigit()]
        return elements
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return []

# Função para processar arquivos em um diretório
def process_files_in_directory(directory, tree_class):
    results = []

    try:
        input_files = os.listdir(directory)
    except Exception as e:
        print(f"Erro ao acessar o diretório {directory}: {e}")
        return

    for input_file in input_files:
        file_path = os.path.join(directory, input_file)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            elements = read_elements_from_file(file_path)
            if elements:
                tree = tree_class()
                performance = measure_performance(tree, elements)
                results.append({
                    'file_name': input_file,
                    'construction_comparisons': performance['construction_comparisons'],
                    'construction_time': performance['construction_time'],
                    'search_comparisons': performance['search_comparisons'],
                    'search_time': performance['search_time']
                })

    if results:
        output_file = f"results_{tree_class.__name__}.csv"
        with open(output_file, mode='w', newline='') as file:
            fieldnames = ['file_name', 'construction_comparisons', 'construction_time',
                          'search_comparisons', 'search_time']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        print(f"Resultados salvos em {output_file}")

# Caminhos para os diretórios de entrada
construction_folder = r"C:\Users\pante\OneDrive\Área de Trabalho\Trabalho Estrutura de Dados 02\4\Construir"
query_folder = r"C:\Users\pante\OneDrive\Área de Trabalho\Trabalho Estrutura de Dados 02\4\Consultar"

# Processar arquivos no diretório de construção
print("Processando arquivos no diretório de construção (AVL Tree):")
process_files_in_directory(construction_folder, AVLTree)

print("Processando arquivos no diretório de construção (Red-Black Tree):")
process_files_in_directory(construction_folder, RBTree)

# Processar arquivos no diretório de consulta
print("Processando arquivos no diretório de consulta (AVL Tree):")
process_files_in_directory(query_folder, AVLTree)

print("Processando arquivos no diretório de consulta (Red-Black Tree):")
process_files_in_directory(query_folder, RBTree)
