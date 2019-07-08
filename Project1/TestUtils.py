import unittest
import utils as utils

class TestUtils(unittest.TestCase):
  def test_fasta_to_seq(self):
    actual = utils.fasta_to_seq("sample.fasta.txt")
    expected = list("MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR")
    self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()