from knack.help_files import helps

helps['kql'] = """
    type: group
    short-summary: Run KQL queries against an Azure Data Explorer (Kusto) cluster.
"""

helps['kql query'] = """
    type: command
    short-summary: Execute a KQL query and return results.
    examples:
      - name: Query a table with an explicit cluster URL
        text: |
            az kql query --cluster https://mycluster.westus2.kusto.windows.net \\
              --database Samples \\
              --kql "StormEvents | where StartTime > ago(7d) | take 20"
      - name: Same, with a configured default cluster and a query file
        text: |
            az configure --defaults kql-cluster=https://mycluster.westus2.kusto.windows.net
            az kql query --database Samples --query-file ./my-query.kql
      - name: Raise the server timeout for a broad historical sweep
        text: |
            az kql query --database Samples --timeout 600 \\
              --kql "StormEvents | where StartTime > ago(30d) | summarize count() by State"
"""
