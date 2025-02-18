from cyberviz.formats.csv_ds import CsvDataset
from unittest.mock import patch, mock_open
import unittest
import os


class TestCsvDataset(unittest.TestCase):
    def setUp(self):
        self.csv_path = 'data/hiraki2021.csv'
        self.dataset = CsvDataset(self.csv_path)

    @patch('os.path.isfile')
    def test_init_invalid_path(self, mock_isfile):
        mock_isfile.return_value = False
        with self.assertRaises(ValueError):
            CsvDataset('/invalid/path.csv')

    @patch('os.path.isfile')
    def test_init_valid_path(self, mock_isfile):
        mock_isfile.return_value = True
        dataset = CsvDataset(self.csv_path)
        self.assertEqual(dataset.format_dataset, 'csv')
        self.assertEqual(dataset.extension_dataset, '.csv')

    @patch('dask.dataframe.read_csv')
    def test_open_dataset(self, mock_read_csv):
        #TODO
        pass

    @patch('cyberviz.formats.csv_ds.get_lexicon')
    def test_activate_lexicon(self, mock_get_lexicon):
        mock_get_lexicon.return_value = {'key': 'value'}
        self.dataset.activate_lexicon()
        self.assertEqual(self.dataset.lexicon, {'key': 'value'})

    @patch('cyberviz.formats.csv_ds.match_headers')
    @patch('cyberviz.formats.csv_ds.CsvDataset.get_headers')
    def test_merge_dataset(self, mock_get_headers, mock_match_headers):
        mock_get_headers.return_value = ['header1', 'header2']
        mock_match_headers.return_value = ['header1', 'header2', 'header3']
        dataset2 = CsvDataset(self.csv_path)
        dataset2.status = True
        self.dataset.status = True
        self.dataset.lexicon = {'key': 'value'}
        self.dataset.merge_dataset(dataset2)
        mock_match_headers.assert_called_once_with(['header1', 'header2'], ['header1', 'header2'], {'key': 'value'})