import unittest
import sys
import time
import random

sys.path.insert(0, '..')  # Adjust path for importing from the parent directory

from lib.main_node import MainNode
from lib.regular_node import RegularNode


class TestMainNode(unittest.TestCase):
    def setUp(self):
        """Setup unique ports for each test to avoid binding errors."""
        self.base_port = random.randint(49152, 65535)
        self.node_main = MainNode("127.0.0.1", self.base_port, id=1)
        self.node_2 = RegularNode("127.0.0.1", self.base_port + 1, id=2, main_id=1, main_node_host="127.0.0.1",
                                  main_node_port=self.base_port)
        self.node_3 = RegularNode("127.0.0.1", self.base_port + 2, id=3, main_id=1, main_node_host="127.0.0.1",
                                  main_node_port=self.base_port)

        self.node_main.start()
        self.node_2.start()
        self.node_3.start()

        time.sleep(1)

    def test_initialization(self):
        """Test initialization of the MainNode."""
        self.assertEqual(self.node_main.host, "127.0.0.1")
        self.assertEqual(self.node_main.port, self.base_port)
        self.assertTrue(self.node_main.is_main_node)

    def test_connection_management(self):
        """Test that MainNode correctly tracks connected nodes."""
        self.assertIn((self.node_2.host, str(self.node_2.port)), self.node_main.known_nodes)
        self.assertIn((self.node_3.host, str(self.node_3.port)), self.node_main.known_nodes)

    def test_data_exchange(self):
        """Test the data exchange process between nodes."""
        self.node_2.add_data(100, "Hello")
        self.node_3.add_data(101, "World")

        self.node_main.request_known_data(self.node_2.id)
        self.node_main.request_known_data(self.node_3.id)

        time.sleep(1)

        self.assertEqual(self.node_main.data_id_table['2'], '100')
        self.assertEqual(self.node_main.data_id_table['3'], '101')

    def tearDown(self):
        """Ensure all nodes are stopped after tests and socket cleanup."""
        self.node_main.stop()
        self.node_2.stop()
        self.node_3.stop()
        time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
