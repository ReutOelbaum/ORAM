import socket, pickle, random, math, string
from types import SimpleNamespace
import json
from moduls import Node

MESSAGE_CONNECTION_SIZE = 1000000000

N = 32
# len_of_file= 5
# len_of_file_name_default=3

height = int(math.ceil(math.log(N, 2)) + 1)  # height of the tree
num_of_leafs = int(math.pow(2, height - 1))
num_of_nodes = int(math.pow(2, height) - 1)
num_of_files_at_bucket = int(math.log(N, 2))


def randStr(chars=string.ascii_uppercase + string.digits, len=10):
    return ''.join(random.choice(chars) for _ in range(len))


class Tree:
    def __init__(self, N):
        self.height = int(math.ceil(math.log(N, 2)) + 1)
        self.num_of_leafs = N
        self.num_of_nodes = int(math.pow(2, height) - 1)
        self.tree = []
        for i in range(num_of_nodes):
            self.tree.append(randStr(len=100))

    def print_tree(self):
        for i in range(num_of_nodes):
            # self.tree[i].print_node()
            print(i)
            print(self.tree[i])

    @staticmethod
    def get_leaf_index(branch):  # get num of leaf - between 1 to num_of_leafs return the coresponding Node
        return int(int(math.pow(2, height - 1)) - 1 + int(branch) - 1);

    @staticmethod
    def get_parent_index(node):
        return int(math.floor((node - 1) / 2.0))

    @staticmethod
    def get_left_child_index(node):
        return node * 2 + 1

    @staticmethod
    def get_right_child_index(node):
        return node * 2 + 2

    @staticmethod
    def get_path_indexes(leaf_id):
        node = Tree.get_leaf_index(leaf_id)
        print(node)
        path_indexes = list()
        for i in range(height):
            path_indexes.append(node)
            node = Tree.get_parent_index(node)
        return list(reversed(path_indexes))

    # def add_file(self, file_content):
    #     self.tree[0].bucket[random.randint(1, num_of_files_at_bucket) - 1]=file_content#maybe bring the client the entire node and return only the
    #     self.flesh()


# class File:
#     def __init__(self, file_name, content):
#         self.file_name = file_name
#         self.content = content
#
#     def print_file(self):
#         print(self.file_name)
#         print(self.content)
#
# class Node:
#     def __init__(self, index, data):
#         self.index = index
#         self.data = []
#         # self.bucket_names= []
#         # for i in range(num_of_files_at_bucket):
#         #     self.bucket.append(randStr(len=len_of_file).encode())
#         #     self.bucket_names.append(randStr(len=len_of_file_name_default).encode())
#
#     def print_node(self):
#         print(self.index)
#         print(self.data)
#         # print(self.bucket)


# class Node:
#     def __init__(self, data=5):
#         self.index = data
#         self.bucket = []
#         self.bucket_names= []
#         for i in range(num_of_files_at_bucket):
#             self.bucket.append(randStr(len=len_of_file).encode())
#             self.bucket_names.append(randStr(len=len_of_file_name_default).encode())
#
#     def print_node(self):
#         print(self.index)
#         print(self.bucket_names)
#         print(self.bucket)

# print("my tree")

MY_TREE = Tree(N)
MY_TREE.print_tree()

HOST = 'localhost'
PORT = 12344

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    data = client_socket.recv(MESSAGE_CONNECTION_SIZE)
    if not data:
        break
    data = data.decode('utf-8')
    print(data)
    if data == "send root":
        # print('gg')
        # root = pickle.dumps(MY_TREE.tree[0])
        root = MY_TREE.tree[0]
        client_socket.sendall(root)
    if data == "get node":
        print("get node")
        client_socket.sendall(b"ok")
        data = client_socket.recv(MESSAGE_CONNECTION_SIZE)
        # index=data.decode()
        index = int.from_bytes(data, "big")

        # node = pickle.dumps(MY_TREE.tree[index])
        node = MY_TREE.tree[index]
        print("nodee")
        print(node)
        client_socket.sendall(node)
    if data == "post node":
        client_socket.sendall(b"ok")
        data = client_socket.recv(MESSAGE_CONNECTION_SIZE)
        print(data)
        node = data
        # print(data)
        # node = pickle.loads(data)
        # print(node)
        # print(node.bucket)
        # print(node.bucket_names)
        client_socket.sendall(b"ok")
        # print(type(node))
        data = client_socket.recv(MESSAGE_CONNECTION_SIZE)
        # index=data.decode()
        index = int.from_bytes(data, "big")
        client_socket.sendall(b"ok")
        # print(index)
        # print(type(index))
        index = int(index)
        print("index")
        print(index)

        # print("node")
        # print(node)
        # MY_TREE.tree[index]=node
        MY_TREE.tree[index] = node
        MY_TREE.print_tree()
    if data == "print tree":
        client_socket.sendall(b"ok")
        MY_TREE.print_tree()

client_socket.close()
