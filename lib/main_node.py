from p2pnetwork.node import Node
import pickle

class MainNode (Node):
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(MainNode, self).__init__(host, port, id, callback, max_connections)
        self.is_main_node = True

        print("Initialized main node")
        
        self.known_nodes = set()
        print(f"Init node {host}:{port}, {id}")

        self.data_id_table = {}
        self.known_data = {}

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)
        print(f"register {node.host}:{node.port}")
        self.known_nodes.add((node.host, node.port))
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)
        print(f"register {node.host}:{node.port}")
        self.known_nodes.add((node.host, node.port))

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)
        print(f"unregister {node.host}:{node.port}")
        self.known_nodes.remove((node.host, node.port))

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)
        print(f"unregister {node.host}:{node.port}")
        self.known_nodes.remove((node.host, node.port))

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

        if data.startswith("[knowndataans]"):
            data = data.removeprefix("[knowndataans]").removesuffix("\n")
            node_id, data_id = data.split(":")
            print(f"({self.id}) received that {node_id} has data {data_id}\n")
            print({data_id: node_id})
            self.data_id_table.update({node_id: data_id})
            
        if data.startswith("[dataans]"):
            data = data.removeprefix("[dataans]").removesuffix("\n")
            data_id, known_data_by_id = data.split(":")
            print(f"{self.id} received requested data {data_id} : {known_data_by_id}")
            self.known_data.update({data_id: known_data_by_id})


    def send_known_nodes(self):
        print("sending nodes information")
        for host, port in self.known_nodes:
            self.send_to_nodes(f"[nodeinfo]{host}:{port}\n")
    
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

