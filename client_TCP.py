# from module import Node
# # import sys
from cryptography.fernet import Fernet
import socket, pickle, math, random, string
import hashlib


class File:
    def __init__(self, file_name, len_content=5):  # , content=None):
        self.file_name = file_name
        # self.content = content  # - need to delete it because there is not much space to save the content???!!
        #
        # if content is None:
        #     self.content = randStr(len=len_of_file)
        self.len_content = len_content
        self.leaf_id = random.randint(1, N)
        # print(self.file_name + "leaf id" + str(self.leaf_id))
        self.path_to_leaf = get_path_indexes(self.leaf_id)
        self.exact_location = 0

    def re_locate(self):
        self.leaf_id = random.randint(1, N)
        self.path_to_leaf = get_path_indexes(self.leaf_id)
        self.exact_location = 0
        # self.hash = data
        # self.key = data


class Node_to_server:
    def __init__(self, index, data):
        self.index = index
        self.data = data
        # self.bucket_names = []
        # for i in range(num_of_files_at_bucket):
        #     self.bucket.append(f.encrypt(randStr(len=len_of_file).encode()))
        #     self.bucket_names.append(f.encrypt(randStr(len=len_of_file_name_default).encode()))

    def print_node(self):
        print(self.index)
        print(self.data)


class Node:
    def __init__(self, data=5):
        self.index = data
        self.bucket = []
        self.bucket_names = []
        for i in range(num_of_files_at_bucket):
            self.bucket.append(f.encrypt(randStr(len=len_of_file).encode()))
            self.bucket_names.append(f.encrypt(randStr(len=len_of_file_name_default).encode()))

    def print_node(self):
        print(self.index)
        print(self.bucket_names)
        print(self.bucket)


# open socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12344
MESSAGE_CONNECTION_SIZE = 1000000000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

key = Fernet.generate_key()
# initialize the Fernet class
f = Fernet(key)

N = 32 # power of 2
len_of_file = 100
len_of_file_name_default = 3

height = int(math.ceil(math.log(N, 2)) + 1)  # height of the tree
num_of_leafs = int(math.pow(2, height - 1))
num_of_nodes = int(math.pow(2, height) - 1)
num_of_files_at_bucket = int(math.log(N, 2))
# client var
counter_of_files = 0


def hash(msg):
    return hashlib.sha224(msg.encode()).hexdigest()


def encrypt(msg):
    #msg is already in bytes
    return f.encrypt(msg)


def decrypt(msg):
    # msg is already in bytes
    return f.decrypt(msg)


def randStr(chars=string.ascii_uppercase + string.digits, len=10):
    return ''.join(random.choice(chars) for _ in range(len))


counter_of_files = 0
# len_of_file = 5
num_of_files_at_bucket = int(math.log(N, 2))
height = int(math.ceil(math.log(N, 2)) + 1)  # height of the tree

map_from_hash_or_content_to_file_name = {}
files = {}
file_name_to_hash = {}


# functions_to_client:


def get_leaf_index(branch):  # get num of leaf - between 1 to num_of_leafs return the coresponding Node
    return int(int(math.pow(2, height - 1)) - 1 + int(branch) - 1);


def get_parent_index(node):
    return int(math.floor((node - 1) / 2.0))


def get_left_child_index(node):
    return node * 2 + 1


def get_right_child_index(node):
    return node * 2 + 2


def get_path_indexes(leaf_id):
    node = get_leaf_index(leaf_id)
    # print(node)
    path_indexes = list()
    for i in range(height):
        path_indexes.append(node)
        node = get_parent_index(node)
    return list(reversed(path_indexes))


# communication
def get_root_node():
    # print("reut")
    s.sendall(b"send root")
    data = s.recv(MESSAGE_CONNECTION_SIZE)
    data = decrypt(data)
    # print(data)
    # print('REUT' + str(type(data)))
    root_node = pickle.loads(data)
    # print("Client sent: " + str(root_node))
    return root_node


def get_node(index):
    # print("debug1")
    s.sendall(b"get node")
    try:
        ans = s.recv(MESSAGE_CONNECTION_SIZE)
    except:
        print("An exception occurred")
    data = ans.decode('utf-8')
    # print(data)
    index_str = str(index)
    # print(index_str)
    # print(type(index_str))
    # s.sendall(index_str.encode())
    index = (index).to_bytes(2, byteorder='big')
    # print(index)
    s.sendall(index)
    data = s.recv(MESSAGE_CONNECTION_SIZE)
    data = decrypt(data)
    # print(data)
    # print('REUT' + str(type(data)))
    node = pickle.loads(data)
    # print("Client sent: " + str(node))
    return node


def post_node(node, index):
    # print("post node")
    s.sendall(b"post node")
    try:
        ans = s.recv(MESSAGE_CONNECTION_SIZE)
    except:
        print("An exception occurred")
    data = ans.decode('utf-8')
    # print(data)
    # NEED TO BE OK
    node = pickle.dumps(node)
    # print("node")
    # print(node)
    # print("index")
    # print(index)
    s.sendall(encrypt(node))
    # BETWEEN MESSAGES WE WAIT FOR OK
    try:
        ans = s.recv(MESSAGE_CONNECTION_SIZE)
    except:
        print("An exception occurred")
    data = ans.decode('utf-8')
    # print(data)
    index_str = str(index)
    # print(index_str)
    # print(type(index_str))
    # s.sendall(index_str.encode())
    index = (index).to_bytes(2, byteorder='big')
    # print(index)
    s.sendall(index)
    # BETWEEN MESSAGES WE WAIT FOR OK
    try:
        ans = s.recv(MESSAGE_CONNECTION_SIZE)
        # print(ans)
    except:
        print("An exception occurred")


def get_path(leaf):
    nodes_at_path = []
    for index in get_path_indexes(leaf):
        nodes_at_path.append(get_node(index))
    # print(nodes_at_path)
    # for node in nodes_at_path:
    #     node.print_node()
        # print("Dfg")
    return nodes_at_path


def print_tree():  # maybe add client id
    # print("print tree")
    # just for debuging
    s.sendall(b"print tree")
    try:
        ans = s.recv(MESSAGE_CONNECTION_SIZE)
    except:
        print("An exception occurred")
    data = ans.decode('utf-8')
    # print(data)


def padding(content):
    return content.ljust(len_of_file, 'x')


def unpadding(content, len):
    return content[:len]

# actions
def add_file_to_root(file_name, content):
    root = get_node(0)  # communication
    # print(root.bucket)
    # print(root.bucket_names)

    while True:
        rand_file = random.randint(1, num_of_files_at_bucket)
        # print(type(root.bucket_names[rand_file - 1]))
        file_name_to_replace = f.decrypt(root.bucket_names[rand_file - 1]).decode("utf-8")
        if file_name_to_replace not in files:
            break  # this is dummy file

    encrypted_content = f.encrypt(content.encode())
    encrypted_file_name = f.encrypt(file_name.encode())

    root.bucket[rand_file - 1] = encrypted_content
    root.bucket_names[rand_file - 1] = encrypted_file_name
    # print("the name of the file 1 is ")
    # print(encrypted_file_name)
    # print("the content of the file 1 is ")
    # print(encrypted_content)
    # print(root.bucket)
    post_node(root, 0)


def add_new_file(filename, content):
    global counter_of_files
    if counter_of_files >= N:
        print("The space is over")
        print("There are already " + str(N) + "files in the system")
        return None

    if filename not in files:
        counter_of_files += 1
        print("we add new file")
    else:
        print(
            "we already have file with this name- we will overide it")  # extension- print message and let the user to decide if they want to overide or change the name


    files[filename] = File(filename, len(content))  # aloow overide of files
    content=padding(content)
    # map_from_hash_or_content_to_file_name[content] = filename
    file_name_to_hash[filename] = hash(content)
    add_file_to_root(filename, content)


def flesh_sons(file_name, file_content, current_node_index, left_node, right_node):
    direction = ""
    if file_name in files:
        if (current_node_index * 2 + 1) in files[file_name].path_to_leaf:
            direction = "Left"
            files[file_name].exact_location = current_node_index * 2 + 1
            # print("reut" + str(files[file_name].exact_location))

        else:
            direction = "Right"
            files[file_name].exact_location = current_node_index * 2 + 2
            # print("mypositiom" + str(files[file_name].exact_location))

        while True:
            rand_file = random.randint(1, num_of_files_at_bucket)
            if direction == "Left":

                if f.decrypt(left_node.bucket_names[rand_file - 1]).decode("utf-8") not in files:
                    break  # this is dummy file
            if direction == "Right":
                if f.decrypt(right_node.bucket_names[rand_file - 1]).decode("utf-8") not in files:
                    break  # this is dummy file

        encrypted_content = f.encrypt(file_content.encode())
        encrypted_file_name = f.encrypt(file_name.encode())

        if direction == "Left":
            left_node.bucket[rand_file - 1] = encrypted_content
            left_node.bucket_names[rand_file - 1] = encrypted_file_name
        if direction == "Right":
            right_node.bucket[rand_file - 1] = encrypted_content
            right_node.bucket_names[rand_file - 1] = encrypted_file_name

    return left_node, right_node


def flesh():
    for i in range(2):  # do it twice
        for level in range(height - 1):  # for each level not include the last one
            rand_bucket = random.randint(1, math.pow(2, level))
            node_index = int(int(math.pow(2, level)) - 1 + int(rand_bucket) - 1)
            father_node = get_node(node_index)

            rand_file = random.randint(1, num_of_files_at_bucket)
            # print(rand_file)
            file_content = f.decrypt(father_node.bucket[rand_file - 1]).decode("utf-8")
            file_name = f.decrypt(father_node.bucket_names[rand_file - 1]).decode("utf-8")
            # לוודא שדורסים קובץR
            new_file_content = randStr(len=len_of_file)
            new_file_name = randStr(len=len_of_file_name_default)

            father_node.bucket[rand_file - 1] = f.encrypt(new_file_content.encode())
            father_node.bucket_names[rand_file - 1] = f.encrypt(new_file_name.encode())

            left_node = get_node(get_left_child_index(node_index))
            right_node = get_node(get_right_child_index(node_index))

            new_left_node, new_right_node = flesh_sons(file_name, file_content, node_index, left_node, right_node)

            post_node(father_node, node_index)
            post_node(new_left_node, get_left_child_index(node_index))
            post_node(new_right_node, get_right_child_index(node_index))


def read_file(file_name):
    return read_or_write_file(file_name, "R")


def write_file(file_name):
    return read_or_write_file(file_name, "W")


def index_of_file_in_bucket(node, file_name):
    for index, item in enumerate(node.bucket_names):
        # print(type(node.bucket_names))
        # print(type(node.bucket_names[index]))
        # print(type(item))
        # print("index")
        # print(index)
        # print(type(index))
        # print(file_name)
        # print(f.decrypt(item))
        if file_name == f.decrypt(item).decode("utf-8"):
            return index
    return "bla"


def read_or_write_file(file_name, read_write_char):  # get R or W
    if file_name in files:
        leaf_id = files[file_name].leaf_id
        path = get_path(leaf_id)
        index = files[file_name].exact_location
        # print(index)
        node_of_file = path[math.floor(math.log(index + 1, 2))]  # THE LEVEL OF THE FILE
        index_of_file = index_of_file_in_bucket(node_of_file, file_name)
        # print(index_of_file)
        # print("inde")
        # print(int(index_of_file))
        encrypted_content = node_of_file.bucket[index_of_file]
        content = f.decrypt(encrypted_content).decode("utf-8")
        # print(content)
        content=unpadding(content, files[file_name].len_content)
        # replace_old_file
        new_content = randStr(len=len_of_file)
        node_of_file.bucket[index_of_file] = f.encrypt(new_content.encode())
        new_file_name = randStr(len=len_of_file_name_default)
        node_of_file.bucket_names[index_of_file] = f.encrypt(new_file_name.encode())
        post_node(node_of_file, index)

        if read_write_char == 'W':
            new_content = input("enter new content of file. len:" + str(len_of_file))


            # print(content)
            if len(new_content) <= len_of_file:
                files[file_name].len_content = len(new_content)
                new_content= padding(new_content)
                # files[file_name].content = new_content
            else:
                files[file_name].len_content = len_of_file
                files[file_name].content = new_content[:len_of_file]
                print("we took only block size")
                # new_str = new_content.ljust(len_of_file, 'x')

        file_name_to_hash[file_name] = hash(new_content)
        # re-write to file
        files[file_name].re_locate()  # aloow overide of files
        # map_from_hash_or_content_to_file_name[content] = file_name
        if file_name_to_hash[file_name] == hash(new_content):
            print("auth SUCCESS!")
        else:
            print("auth FAILED!")
        add_file_to_root(file_name, new_content)
        return content
    else:
        print("There is not such a file")
        return "There is not such a file"


def init_tree_with_dummy_file():
    for i in range(num_of_nodes):
        post_node(Node(i), i)



def choose_action():
    global finish
    text= """
choose num of suppurted action:
1. add file 
2. read file
3. re- write file
4. delete file
5. exit 
    """
    print(text)
    num=input()
    if num=="1":
        if counter_of_files >= N:
            print("The space is over")
            print("There are already " + str(N) + "files in the system")
        else:
            file_name= input("Enter file name")
            file_content = input("Enter file content")
            add_new_file(file_name, file_content)
            flesh()

    elif num=='2':
        print("Choose the file to read")
        print_files()
        file_name=input("file name:")
        if file_name not in files:
            print("There is not such file")
        else:
            print(read_file(file_name))
            flesh()

    elif num=='3':
        print("Choose the file to re-write")
        print_files()
        file_name=input("file name:")
        if file_name not in files:
            print("There is not such file")
        else:
            write_file(file_name)
            flesh()

    elif num=='4':
        print("Choose the file to delete")
        print_files()
        file_name = input("file name:")
        if file_name not in files:
            print("There is not such file")
        else:

            del files[file_name]
            del file_name_to_hash[file_name]

    elif num=="5":
        finish=True
    else:
        "Error. try another action"

def print_files():
    print("The files in the system are:")
    for index ,file in enumerate(files):
        print(str(index+1)+": " +str(file))


def benchmark(num):
    print("the num of leafs")
    print(N)
    add_new_file('my_file1', "1" * 5)
    flesh()
    start = time.time()
    print(start)
    for i in range(num):
        read_file('my_file1')
        flesh()
    end = time.time()
    print(end)
    latency = end - start
    print("time for" +str(num) +"actions")
    print(latency)


if __name__ == "__main__":
    init_tree_with_dummy_file()
    print("print tree")
    # print_tree()
    # add_new_file('my_file1', "1" * 5)
    # flesh()
    # print_tree()
    #
    # print(read_file('my_file1'))
    # print_tree()
    # print("read 1")
    # flesh()
    #
    # write_file('my_file1')
    # print_tree()
    # flesh()
    # print(read_file('my_file1'))
    finish = False
    while not finish:
        choose_action()
        #flesh()
    # benchmark(15)

    s.close()
