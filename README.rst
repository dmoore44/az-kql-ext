Azure CLI 'kql' Extension
==========================

Standalone Azure CLI extension that adds data-plane KQL query execution to ``az`` via ``az kql query``, reusing your active ``az login`` session.

Installation
------------

Every GitHub Release carries a built wheel. Install it straight from the release:

.. code-block:: bash

    az extension add --source https://github.com/dmoore44/az-kql-ext/releases/download/v0.1.0/kql-0.1.0-py3-none-any.whl

Replace ``v0.1.0`` / ``0.1.0`` with the release you want; each release page lists the exact file name. A locally built wheel installs the same way:

.. code-block:: bash

    az extension add --source ./dist/kql-0.1.0-py3-none-any.whl

Usage
-----

.. code-block:: bash

    # Set a default cluster (optional)
    az configure --defaults kql-cluster=https://mycluster.westus2.kusto.windows.net

    # Run an inline KQL query
    az kql query --database Samples --kql "StormEvents | take 10" -o table

    # Run a query from a file
    az kql query --database Samples --query-file ./query.kql -o json

    # Raise timeout (1-3600s; Kusto default is 240s)
    az kql query --database Samples --timeout 600 --kql "StormEvents | summarize count() by State"

Note: ``--kql`` / ``-kq`` is used instead of ``--query`` so it does not collide with Azure CLI's global ``--query`` JMESPath output filter.

Building from Source
--------------------

.. code-block:: bash

    python3 -m venv .venv
    .venv/bin/pip install build setuptools wheel
    .venv/bin/python -m build --wheel --no-isolation --outdir dist .
