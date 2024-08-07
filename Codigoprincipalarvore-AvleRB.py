import os
import time
from collections import defaultdict

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.comparisons = 0

    def insert(self, root, key):
        if not root:
            return AVLNode(key)

        self.comparisons += 1
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        if root is None or root.key == key:
            return root

        self.comparisons += 1
        if key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def left_rotate(self, z):
        if not z or not z.right:
            return z

        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        if not z or not z.left:
            return z

        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

def avl_insert(tree, key):
    start_time = time.time()
    tree.root = tree.insert(tree.root, key)
    end_time = time.time()
    return end_time - start_time

def avl_search(tree, key):
    start_time = time.time()
    found = tree.search(tree.root, key)
    end_time = time.time()
    return found, end_time - start_time

class RBNode:
    def __init__(self, key, color='R'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = 'B'
        self.root = self.TNULL
        self.comparisons = 0

    def insert(self, key):
        new_node = RBNode(key)
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        if self.root == self.TNULL:
            self.root = new_node
            self.root.color = 'B'
            return 0

        parent = None
        current = self.root
        while current != self.TNULL:
            parent = current
            self.comparisons += 1
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.fix_insert(new_node)
        return new_node

    def search(self, key):
        current = self.root
        while current != self.TNULL and key != current.key:
            self.comparisons += 1
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def fix_insert(self, k):
        while k != self.root and k.parent.color == 'R':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'R':
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'R':
                    u.color = 'B'
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'B'
                    k.parent.parent.color = 'R'
                    self.right_rotate(k.parent.parent)
        self.root.color = 'B'

    def left_rotate(self, x):
        if not x or not x.right:
            return

        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        if not x or not x.left:
            return

        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

def rb_insert(tree, key):
    start_time = time.time()
    tree.insert(key)
    end_time = time.time()
    return end_time - start_time

def rb_search(tree, key):
    start_time = time.time()
    found = tree.search(key)
    end_time = time.time()
    return found, end_time - start_time

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        keys = [int(num) for num in content.split()]
        print(f"Arquivo {file_path} tem {len(keys)} elementos.")  # Imprime o tamanho do conjunto de dados
        return keys

def process_files_in_directory(directory, construct=True):
    insert_times = {'AVL': defaultdict(float), 'RB': defaultdict(float)}
    search_times = {'AVL': defaultdict(float), 'RB': defaultdict(float)}
    comparisons = {'AVL': defaultdict(int), 'RB': defaultdict(int)}
    counts = {'AVL': defaultdict(int), 'RB': defaultdict(int)}
    all_keys = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            keys = read_input_file(file_path)
            if not keys:
                continue
            size = len(keys)
            all_keys.extend(keys)
            if construct:
                # Run 20 times for averaging
                for _ in range(20):
                    # AVL Tree
                    avl_tree = AVLTree()
                    avl_insert_time = sum(avl_insert(avl_tree, key) for key in keys)
                    avl_search_time = sum(avl_search(avl_tree, key)[1] for key in keys)

                    insert_times['AVL'][size] += avl_insert_time
                    search_times['AVL'][size] += avl_search_time
                    comparisons['AVL'][size] += avl_tree.comparisons
                    counts['AVL'][size] += 1

                    # Red-Black Tree
                    rb_tree = RBTree()
                    rb_insert_time = sum(rb_insert(rb_tree, key) for key in keys)
                    rb_search_time = sum(rb_search(rb_tree, key)[1] for key in keys)

                    insert_times['RB'][size] += rb_insert_time
                    search_times['RB'][size] += rb_search_time
                    comparisons['RB'][size] += rb_tree.comparisons
                    counts['RB'][size] += 1
            else:
                all_keys.extend(keys)

    # Average the times and comparisons over the 20 runs
    for size in counts['AVL']:
        if counts['AVL'][size] > 0:
            insert_times['AVL'][size] /= 20
            search_times['AVL'][size] /= 20
            comparisons['AVL'][size] /= 20

    for size in counts['RB']:
        if counts['RB'][size] > 0:
            insert_times['RB'][size] /= 20
            search_times['RB'][size] /= 20
            comparisons['RB'][size] /= 20

    return insert_times, search_times, comparisons, counts, all_keys

def main():
    from google.colab import drive  # Google Drive Access
    drive.mount('/content/drive')

    dir1 = '/content/drive/MyDrive/UNIOESTE/EstruturadeDados/2024/TRABALHO02/4/Construir'
    dir2 = '/content/drive/MyDrive/UNIOESTE/EstruturadeDados/2024/TRABALHO02/4/Consultar'

    print("Construindo árvores usando arquivos na pasta 1:")
    insert_times1, search_times1, comparisons1, counts1, all_keys1 = process_files_in_directory(dir1, construct=True)

    print("AVL Tree - Pasta 1 (Construção):")
    for size in insert_times1['AVL']:
        total_insert_time = insert_times1['AVL'][size]
        avg_insert_time = total_insert_time / counts1['AVL'][size]
        avg_comparisons = comparisons1['AVL'][size] / counts1['AVL'][size]
        print(f"Tamanho do arranjo: {size}")
        print(f"Total insert time: {total_insert_time:.6f} seconds")
        print(f"Total comparisons: {comparisons1['AVL'][size]}")
        print(f"Média do tempo de inserção: {avg_insert_time:.6f} seconds")
        print(f"Média das comparações: {avg_comparisons:.2f}")

    print("\nRed-Black Tree - Pasta 1 (Construção):")
    for size in insert_times1['RB']:
        total_insert_time = insert_times1['RB'][size]
        avg_insert_time = total_insert_time / counts1['RB'][size]
        avg_comparisons = comparisons1['RB'][size] / counts1['RB'][size]
        print(f"Tamanho do arranjo: {size}")
        print(f"Total insert time: {total_insert_time:.6f} seconds")
        print(f"Total comparisons: {comparisons1['RB'][size]}")
        print(f"Média do tempo de inserção: {avg_insert_time:.6f} seconds")
        print(f"Média das comparações: {avg_comparisons:.2f}")

    print("\nConsultando árvores usando arquivos na pasta 2:")
    insert_times2, search_times2, comparisons2, counts2, all_keys2 = process_files_in_directory(dir2, construct=False)

    # AVL Tree
    avl_tree = AVLTree()
    for key in all_keys1:
        avl_insert(avl_tree, key)
    avl_search_times = [avl_search(avl_tree, key)[1] for key in all_keys2]
    total_avl_search_time = sum(avl_search_times)
    print("AVL Tree - Pasta 2 (Consulta):")
    print(f"Total search time: {total_avl_search_time:.6f} seconds")
    print(f"Total comparisons: {avl_tree.comparisons}")
    for size, time in zip(counts2['AVL'].keys(), avl_search_times):
      print(f"Tamanho do vetor: {size}, Tempo de consulta: {time:.6f} seconds")
    
    print("AVL Tree:")
    for size in search_times1['AVL']: 
        total_search_time = search_times1['AVL'][size] 
        avg_search_time = total_search_time / counts1['AVL'][size] 
        avg_comparisons = comparisons1['AVL'][size] / counts1['AVL'][size]
        print(f"Tamanho do arranjo: {size}")
        print(f"Tempo total de busca: {total_search_time:.6f} segundos")
        print(f"Tempo médio de busca: {avg_search_time:.6f} segundos")
        print(f"Número médio de comparações: {avg_comparisons}")
        print("----")


    # Red-Black Tree
    rb_tree = RBTree()
    for key in all_keys1:
        rb_insert(rb_tree, key)
    rb_search_times = [rb_search(rb_tree, key)[1] for key in all_keys2]
    total_rb_search_time = sum(rb_search_times)
    print("\nRed-Black Tree - Pasta 2 (Consulta):")
    print(f"Total search time: {total_rb_search_time:.6f} seconds")
    print(f"Total comparisons: {rb_tree.comparisons}")
    for size, time in zip(counts2['RB'].keys(), rb_search_times):
      print(f"Tamanho do vetor: {size}, Tempo de consulta: {time:.6f} seconds")

    print("Red-Black Tree - Pasta 1 (Busca):")
    for size in search_times1['RB']: # Changed rb_search_times to search_times1
        total_search_time = search_times1['RB'][size] # Changed rb_search_times to search_times1
        avg_search_time = total_search_time / counts1['RB'][size] 
        avg_comparisons = comparisons1['RB'][size] / counts1['RB'][size]
        print(f"Tamanho do arranjo: {size}")
        print(f"Tempo total de busca: {total_search_time:.6f} segundos")
        print(f"Tempo médio de busca: {avg_search_time:.6f} segundos")
        print(f"Número médio de comparações: {avg_comparisons}")
        print("----")

    # Print average times
    #print("\nMédia dos tempos de inserção por tamanho de arranjo - AVL Tree:")
    #for size in insert_times1['AVL']:
        #avg_time = insert_times1['AVL'][size]
        #print(f"Tamanho do arranjo: {size}, Média do tempo: {avg_time:.6f} seconds")

   #print("\nMédia dos tempos de inserção por tamanho de arranjo - Red-Black Tree:")
    #for size in insert_times1['RB']:
        #avg_time = insert_times1['RB'][size]
        #print(f"Tamanho do arranjo: {size}, Média do tempo: {avg_time:.6f} seconds")

if __name__ == "__main__":
    main()
