import uuid
from datetime import timedelta

from azure.identity import AzureCliCredential
from azure.kusto.data import ClientRequestProperties, KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoAuthenticationError, KustoServiceError
from knack.util import CLIError


def kql_query(
    cmd,  # pylint: disable=unused-argument
    database,
    cluster=None,
    query=None,
    query_file=None,
    timeout=240,
    client_request_id=None,
):
    """Execute a KQL query against an Azure Data Explorer cluster and return rows as dicts."""
    # --- 1. validate mutually-exclusive query source & inputs ---
    if (query is not None) == (query_file is not None):
        raise CLIError('Specify exactly one of --kql or --query-file.')
    if query_file is not None:
        try:
            with open(query_file, 'r', encoding='utf-8') as f:
                query = f.read()
        except OSError as ex:
            raise CLIError(f"Failed to read --query-file '{query_file}': {ex}") from ex
    if not query.strip():
        raise CLIError('KQL query text cannot be empty.')

    if not 1 <= timeout <= 3600:
        raise CLIError('--timeout must be between 1 and 3600 seconds.')

    if not cluster:
        raise CLIError(
            'No --cluster given and no configured default set. '
            'Pass --cluster, or run: az configure --defaults kql-cluster=<cluster-url>'
        )

    # --- 2. build client, reusing the existing `az login` session ---
    try:
        credential = AzureCliCredential()
        kcsb = KustoConnectionStringBuilder.with_azure_token_credential(cluster, credential)
        client = KustoClient(kcsb)
    except Exception as ex:  # pylint: disable=broad-except
        raise CLIError(
            f"Failed to build Kusto client — are you logged in? Run 'az login'. ({ex})"
        ) from ex

    # --- 3. build request properties (timeout, request id) ---
    crp = ClientRequestProperties()
    crp.client_request_id = client_request_id or f'az-kql-{uuid.uuid4()}'
    crp.set_option(crp.request_timeout_option_name, timedelta(seconds=timeout))

    # --- 4. execute ---
    try:
        response = client.execute_query(database, query, crp)
    except KustoAuthenticationError as ex:
        raise CLIError(
            f"Authentication to {cluster} failed. Run 'az login' and retry. ({ex})"
        ) from ex
    except KustoServiceError as ex:
        raise CLIError(f'Kusto query failed: {ex}') from ex
    finally:
        client.close()

    # --- 5. shape result as list[dict] for az's output formatter ---
    if not response.primary_results:
        return []
    table = response.primary_results[0]
    columns = [col.column_name for col in table.columns]
    return [dict(zip(columns, row)) for row in table]
