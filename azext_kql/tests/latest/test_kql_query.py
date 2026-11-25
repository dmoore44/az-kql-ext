import types
import unittest
from unittest.mock import MagicMock, patch

from knack.util import CLIError

from azext_kql.custom import kql_query


class KqlQueryTests(unittest.TestCase):
    """Unit tests for azext_kql.custom.kql_query."""

    def test_requires_exactly_one_query_source(self):
        with self.assertRaises(CLIError):
            kql_query(None, database='azure', cluster='https://example.kusto.windows.net')
        with self.assertRaises(CLIError):
            kql_query(
                None,
                database='azure',
                cluster='https://example.kusto.windows.net',
                query='print 1',
                query_file='/tmp/nonexistent.kql',
            )

    def test_missing_query_file_raises_cli_error(self):
        with self.assertRaises(CLIError):
            kql_query(
                None,
                database='azure',
                cluster='https://example.kusto.windows.net',
                query_file='/tmp/definitely-does-not-exist-az-kql.kql',
            )

    def test_timeout_bounds(self):
        for bad_timeout in (0, -5, 3601):
            with self.assertRaises(CLIError):
                kql_query(
                    None,
                    database='azure',
                    cluster='https://example.kusto.windows.net',
                    query='print 1',
                    timeout=bad_timeout,
                )

    @patch('azext_kql.custom.KustoClient')
    @patch('azext_kql.custom.KustoConnectionStringBuilder.with_azure_token_credential')
    @patch('azext_kql.custom.AzureCliCredential')
    def test_shapes_primary_results_to_list_of_dicts(self, _cred, _kcsb, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        col1 = types.SimpleNamespace(column_name='Timestamp')
        col2 = types.SimpleNamespace(column_name='http_request.url.hostname')
        table = MagicMock()
        table.columns = [col1, col2]
        table.__iter__.return_value = iter([
            ('2026-11-25T00:00:00Z', 'example.com'),
            ('2026-11-25T00:01:00Z', 'example.org'),
        ])
        mock_client.execute_query.return_value = types.SimpleNamespace(primary_results=[table])

        result = kql_query(
            None,
            database='mydb',
            cluster='https://example.kusto.windows.net',
            query='SampleEvents | take 2',
            timeout=120,
            client_request_id='req-123',
        )

        self.assertEqual(
            result,
            [
                {'Timestamp': '2026-11-25T00:00:00Z', 'http_request.url.hostname': 'example.com'},
                {'Timestamp': '2026-11-25T00:01:00Z', 'http_request.url.hostname': 'example.org'},
            ],
        )
        mock_client.close.assert_called_once()
