import unittest
import sys
import time
import random

sys.path.insert(0, '..')  # Adjust path for importing from the parent directory

from lib.main_node import MainNode
from lib.regular_node import RegularNode


class TestRegularNode(unittest.TestCase):
    def setUp(self):
        """Setup a MainNode and RegularNode with unique ports for testing."""
        self.base_port = random.randint(49152, 65535)
        self.main_node = MainNode("127.0.0.1", self.base_port, id=1)
        self.regular_node = RegularNode("127.0.0.1", self.base_port + 1, id=2, main_id=1, main_node_host="127.0.0.1",
                                        main_node_port=self.base_port)

        self.main_node.start()
        self.regular_node.start()

        time.sleep(1)

    def test_initialization(self):
        """Test the initialization of RegularNode."""
        self.assertEqual(self.regular_node.host, "127.0.0.1")
        self.assertEqual(self.regular_node.port, self.base_port + 1)
        self.assertFalse(self.regular_node.is_main_node)

    def test_connection_to_main_node(self):
        """Test that RegularNode attempts to connect to MainNode on start."""
        self.assertTrue(self.regular_node.connection_by_id(self.main_node.id))

    def test_message_handling(self):
        """Test that RegularNode handles incoming messages correctly."""
        test_message = "[nodeinfo]127.0.0.1:8001"
        self.regular_node.node_message(self.regular_node, test_message)

        self.assertIn(("127.0.0.1", 8001), self.regular_node.known_nodes)

    def test_data_management(self):
        """Test data management capabilities of RegularNode."""
        self.regular_node.add_data(200, "Test Data")
        self.assertIn(200, self.regular_node.known_data)
        self.assertEqual(self.regular_node.known_data[200], "Test Data")

    def tearDown(self):
        """Ensure all nodes are stopped after tests."""
        self.main_node.stop()
        self.regular_node.stop()
        time.sleep(1)


if __name__ == '__main__':
    unittest.main()
