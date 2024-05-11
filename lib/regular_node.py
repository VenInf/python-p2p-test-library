from p2pnetwork.node import Node
import pickle

class RegularNode (Node):
    def __init__(self, host, port, id=None, main_id=None, main_node_host=None, main_node_port=None, callback=None, max_connections=0):
        super(RegularNode, self).__init__(host, port, id, callback, max_connections)
        self.is_main_node = False
    
        self.main_id = main_id
        self.main_node_host = main_node_host
        self.main_node_port = main_node_port

        self.known_nodes = set()
        print(f"Init node {host}:{port}, {id}")

        self.data_id_table = {}
        self.known_data = {}

    def start(self):
        super(RegularNode, self).start()
        print(f"connect with main node {(self.main_node_host, self.main_node_port)}")
        self.connect_with_node(host=self.main_node_host, port=self.main_node_port)

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)
        
    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)
        
    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")
        
    def connection_by_id(self, node_id):
        for n in self.all_nodes:
            if str(n.id) == str(node_id):
                return n
    
    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))

        if data.startswith("[nodeinfo]"):
            data = data.removeprefix("[nodeinfo]").removesuffix("\n")
            host, port = data.split(":")
            port = int(port)
            print(f"({self.id}) received info about a node {host}:{port}\n")
            self.known_nodes.add((host, port))

        if data.startswith("[knowndatareq]"):
            for data_id in self.known_data:
                print(f"sending known data id: {data_id} to {node}")
                self.send_to_node(node, f"[knowndataans]{self.id}:{data_id}\n")

        if data.startswith("[knowndataans]"):
            data = data.removeprefix("[knowndataans]").removesuffix("\n")
            node_id, data_id = data.split(":")
            print(f"({self.id}) received that {node_id} has data {data_id}\n")
            print({data_id: node_id})
            self.data_id_table.update({node_id: data_id})

        if data.startswith("[datareq]"):
            req_data_id = data.removeprefix("[datareq]").removesuffix("\n")
            for data_id, known_data_by_id in self.known_data.items():
                if (str(data_id) == str(req_data_id)):
                    print(f"{self.id} found requested data id {data_id}")
                    self.send_to_node(node, f"[dataans]{data_id}:{known_data_by_id}")
                    return
            else:
                print(f"requested data id {req_data_id} is not found")
        
        if data.startswith("[dataans]"):
            data = data.removeprefix("[dataans]").removesuffix("\n")
            data_id, known_data_by_id = data.split(":")
            print(f"{self.id} received requested data {data_id} : {known_data_by_id}")
            self.known_data.update({data_id: known_data_by_id})

    def connect_to_known_nodes(self):
        if(not self.is_main_node):
            for host, port in self.known_nodes:         
                print(f"connect with known node {host}:{port}\n")
                self.connect_with_node(host=host, port=port)
    
    def request_known_data(self, node_id):
        print(f"requesting data ids from {node_id}")
        self.send_to_node(self.connection_by_id(node_id), "[knowndatareq]")

    def request_data_by_id(self, req_data_id):
        for node_id, data_id in self.data_id_table.items():
            if (str(req_data_id) == str(data_id)):
                print(f"{node_id} has the {req_data_id}")
                self.send_to_node(self.connection_by_id(node_id), f"[datareq]{req_data_id}")
                return
        print(f"no info who has the data id = {req_data_id}")

    def add_data(self, data_id, data):
        self.known_data.update({data_id: data})

        