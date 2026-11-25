def load_arguments(self, _):
    with self.argument_context('kql query') as c:
        c.argument(
            'cluster',
            options_list=['--cluster', '-c'],
            configured_default='kql-cluster',
            help=(
                'Kusto cluster URL, e.g. https://mycluster.westus2.kusto.windows.net. '
                'Can be set as a default with: az configure --defaults kql-cluster=<url>'
            ),
        )
        c.argument(
            'database',
            options_list=['--database', '-d'],
            required=True,
            help='Database name within the cluster, e.g. Samples, telemetry, logs.',
        )
        c.argument(
            'query',
            options_list=['--kql', '-kq'],
            help='Inline KQL query text. Mutually exclusive with --query-file.',
        )
        c.argument(
            'query_file',
            options_list=['--query-file'],
            help='Path to a file containing KQL query text. Mutually exclusive with --kql.',
        )
        c.argument(
            'timeout',
            type=int,
            default=240,
            help='Server-side query timeout in seconds (1-3600; Kusto default 240, max 3600).',
        )
        c.argument(
            'client_request_id',
            help='Optional custom client-request-id for correlating this run server-side.',
        )
