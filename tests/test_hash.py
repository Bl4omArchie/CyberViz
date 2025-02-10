import unittest
from hashlib import sha256
from cyberviz.src.hash import compute_hash_file


class TestHashFunctions(unittest.TestCase):

    def test_compute_hash_file(self):
        file_path = 'test_file.txt'
        with open(file_path, 'w') as f:
            f.write('Hello, world!')
            
        expected_hash = sha256(b'Hello, world!').hexdigest()
        result_hash = compute_hash_file(file_path)
        
        self.assertEqual(result_hash, expected_hash)


if __name__ == '__main__':
    unittest.main()