# DWH FUNCTIONS


def getAzureKey(vault, key):
    """Retrieve keys from the Azure keyvault with the vault name and key name"""
    from azure.keyvault.secrets import SecretClient
    from azure.identity import AzurePowerShellCredential

    # get credentials
    credential = AzurePowerShellCredential()
    client = SecretClient(
        vault_url=f"https://{vault}.vault.azure.net", credential=credential
    )
    retrieved_secret = client.get_secret(name=key)

    return retrieved_secret.value


def readFromDB(USERNAME, PASSWORD, SERVER, DATABASE, SQLQUERY):
    from sqlalchemy.engine import URL
    from sqlalchemy import create_engine
    import pandas as pd
    import sqlalchemy as sa

    # get connection URL
    connection_url = URL.create(
        "mssql+pyodbc",
        query={
            "odbc_connect": "Driver={ODBC Driver 18 for SQL Server};"
            f"Server={SERVER};"
            f"Database={DATABASE};"
            "TrustServerCertificate=yes;"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        },
    )

    engine = create_engine(connection_url)

    with engine.begin() as conn:
        df = pd.read_sql_query(sa.text(SQLQUERY), conn)

    return df


def readFromDBPyODBC(SERVER, DATABASE, SQLQUERY, USERNAME, PASSWORD):
    import pypyodbc

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        f"uid={USERNAME};"
        f"pwd={PASSWORD};"
        "TrustServerCertificate=yes"
    )

    # setup connection
    cnxn = pypyodbc.connect(connection_string)
    cursor = cnxn.cursor()

    # load data from query
    cursor.execute(SQLQUERY)
    rows = cursor.fetchall()

    # transform to df
    import pandas as pd

    df = pd.DataFrame.from_records(rows, columns=[x[0] for x in cursor.description])

    return df


## HELP FUNCTIONS
def addDfTotals(table, groupCol, sumCols):
    import pandas as pd

    """Adds a row of totals with corret name"""
    # --- 'Beïnvloedbaar vs Niet beïnvloedbaar'
    cols = [groupCol] + sumCols
    df = table[cols].groupby(groupCol).sum().reset_index()
    df = pd.concat([df, df.sum().to_frame().T], ignore_index=False)
    df.reset_index(drop=True, inplace=True)

    import numpy as np

    df[groupCol] = np.where(
        df[groupCol] == df[groupCol][df.index.max()], "Totaal", df[groupCol]
    )

    return df


def connectToSharepoint(client_id, client_secret):
    # Azure AD Application Details
    from office365.runtime.auth.client_credential import ClientCredential
    from office365.sharepoint.client_context import ClientContext

    site_url = "https://hogeschoolutrecht.sharepoint.com/sites/MDW-FCA-DA-P"
    client_credentials = ClientCredential(client_id, client_secret)
    ctx = ClientContext(site_url).with_credentials(client_credentials)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Authenticated into SharePoint as:", web.properties["Title"])

    return ctx


## SHAREPOINT FUNCTIONS
def readFromSharepoint(shp_folder, shp_file_name, ctx):
    # Import Libraries
    from office365.sharepoint.files.file import File

    file_path = shp_folder + shp_file_name
    response = File.open_binary(ctx, file_path)
    if response.status_code == 200:
        return response
    else:
        print(f"Can't open file, status code: {response.status_code}")


def uploadToSharePoint(input_df, shp_file_name, shp_folder, client_id, client_secret):
    from io import BytesIO
    import pandas as pd

    df = input_df.copy()
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    file_content = buffer.read()
    ctx = connectToSharepoint(client_id, client_secret)

    from concurrent.futures import ThreadPoolExecutor, as_completed

    target_folder = ctx.web.get_folder_by_server_relative_url(shp_folder)

    with ThreadPoolExecutor(max_workers=5) as executor:
        # file_content = content_file.read()
        futures = executor.submit(
            target_folder.upload_file, shp_file_name, file_content
        )
        if as_completed(futures):
            futures.result().execute_query()


def sqlPathToString(sql_file, jmstart="", jmend="", suppliers=""):
    ## Load totals from UBW
    sql_path = f"SQLS\\{sql_file}.sql"

    # Open file
    with open(sql_path, "r") as fp:
        sql = fp.read()

    from string import Template

    sql_str = Template(sql).substitute(
        jmstart=jmstart, jmend=jmend, suppliers=suppliers
    )
    return sql_str
