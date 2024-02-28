'''
Executes queries against a log analytics workspace
'''

import pandas as pd
from datetime import timedelta
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
import json


def execute_query(ws_id: str, query: str, timespan: tuple) -> dict:
    """
    Executes KQL query against LAW and returns results.

    Args:
        ws_id: id of the workspace to query.
        query: query to be executed.
            Should be a string that contains the SQL query
        timespan: ~datetime.timedelta or tuple[~datetime.datetime,
            ~datetime.timedelta] or tuple[~datetime.datetime,
            ~datetime.datetime] or None

    Returns:
        dictionary representation of query results
    """

    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    try:
        response = client.query_workspace(
            workspace_id=ws_id,
            query=query,
            timespan=timespan
            )
        if response.status == LogsQueryStatus.PARTIAL:
            error = response.partial_error
            data = response.partial_data
            print(error)
        elif response.status == LogsQueryStatus.SUCCESS:
            data = response.tables
        for table in data:
            df = pd.DataFrame(data=table.rows, columns=table.columns)
            return json.loads(df.to_json(orient="records"))
    except HttpResponseError as err:
        print("something fatal happened")
        print(err)


def get_active_conns(ws_id):
    """
    Executes KQL query against LAW and returns a list of all dataTypes that
        have been active over the past 7 days.

    Args:
        ws_id: id of the workspace to query.

    Returns:
        dictionary representation of query results
    """
    timespan = timedelta(7)
    query = """let a = (
        CommonSecurityLog
        | summarize by DeviceVendor, DeviceProduct
        | extend d = strcat("CEF - ", DeviceVendor, " - ", DeviceProduct)
        | project CEF = d
        );
    let b = (
        AzureDiagnostics
        | summarize by ResourceType, Type
        | extend d = strcat(Type, " - ", ResourceType)
        | project Diag = d
        );
    union *
    | summarize by Type
    | union a, b
    | extend Source = iff(isnotempty(CEF), CEF, iff(isnotempty(Diag), Diag, Type))
    | project Source
    | sort by Source asc"""

    return execute_query(ws_id, query, timespan)
