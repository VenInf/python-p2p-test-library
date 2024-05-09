#######################################################################################################################
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# This example show how to derive a own Node class (MyOwnPeer2PeerNode) from p2pnet.Node to implement your own Node   #
# implementation. See the MyOwnPeer2PeerNode.py for all the details. In that class all your own application specific  #
# details are coded.                                                                                                  #
#######################################################################################################################

import sys
import time
sys.path.insert(0, '..') # Import the files where the modules are located

from lib.main_node import MainNode
from lib.regular_node import RegularNode


node_main = MainNode("127.0.0.1", 8001, id=1)
node_2 = RegularNode("127.0.0.1", 8002, id=2, main_id=1, main_node_host="127.0.0.1", main_node_port=8001)
node_3 = RegularNode("127.0.0.1", 8003, id=3, main_id=1, main_node_host="127.0.0.1", main_node_port=8001)

time.sleep(1)

node_main.start()
node_2.start()
node_3.start()

time.sleep(1)

debug = True
node_main.debug = debug
node_2.debug = debug
node_3.debug = debug

time.sleep(2)

# node_main.send_known_nodes()

# time.sleep(2)

# node_2.connect_to_known_nodes()
# node_3.connect_to_known_nodes()
# time.sleep(2)

print("-------- Finish initialisation -------------")


node_2.add_data(100, "Hello")
node_3.add_data(101, " World!")

print(f"node_2.known_data {node_2.known_data}")
print(f"node_3.known_data {node_3.known_data}")

node_main.request_known_data(node_2.id)
time.sleep(2)

node_main.request_known_data(node_3.id)
time.sleep(2)


print(f"node_main.data_id_table -- {node_main.data_id_table}")


print("--------      End network      -------------")

node_main.stop()
node_2.stop()
node_3.stop()
print('end test')
