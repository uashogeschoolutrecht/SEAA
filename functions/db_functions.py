import struct
import pyodbc
import pandas as pd
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
import adal 
from typing import Any
from string import Template

class DB:
    def __init__(self):
        """
        Initialize the DB class by setting up Azure credentials and generating an access token.
        """
        self.client_secret = self.get_azure_key(key_name='KVS-SPK-PBI-SQL')
        self.client_id = self.get_azure_key(key_name='KVK-SPK-PBI-SQL')
        self.tenant_id = self.get_azure_key(key_name='KVT-HU-TENANT-ID')
        self.token_structure = self.generate_token_structure()

    def get_azure_key(self, key_name: str, vault_name: str = 'KV-DENA') -> str:
        """
        Retrieve a secret key from Azure Key Vault.

        Parameters:
        - key_name (str): The name of the key to retrieve.
        - vault_name (str): The name of the Azure Key Vault.

        Returns:
        - str: The value of the retrieved secret key.
        """
        # Setup credentials and initialize SecretClient
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=f"https://{vault_name}.vault.azure.net", credential=credential)
        
        # Retrieve the secret value
        retrieved_secret = client.get_secret(name=key_name)
        return retrieved_secret.value

    def generate_token_structure(self) -> bytes:
        """
        Generate a token structure required for SQL Server connection.

        Returns:
        - bytes: The packed token structure for SQL Server connection.
        """
        authority_host_url = "https://login.microsoftonline.com"
        authority_url = f"{authority_host_url}/{self.tenant_id}"
        resource = "https://database.windows.net/"
        
        # Obtain authentication token from Azure AD
        context = adal.AuthenticationContext(authority_url, api_version=None)
        token = context.acquire_token_with_client_credentials(resource, self.client_id, self.client_secret)
        
        # Process the token into the required binary structure
        token_bytes = bytes(token["accessToken"], "UTF-8")
        expanded_token = b''

        for byte in token_bytes:
            expanded_token += bytes({byte})
            expanded_token += bytes(1)
        
        return struct.pack("=i", len(expanded_token)) + expanded_token

    from azure.identity import InteractiveBrowserCredential


    # def generate_token_structure(self) -> bytes:
    #     """
    #     Generate a token structure required for SQL Server connection using Azure Entra account.

    #     Returns:
    #     - bytes: The packed token structure for SQL Server connection.
    #     """
    #     authority_host_url = "https://login.microsoftonline.com"
    #     authority_url = f"{authority_host_url}/{self.tenant_id}"
    #     scope = "https://database.windows.net/.default"
        
    #     # Obtain authentication token using InteractiveBrowserCredential
    #     credential = InteractiveBrowserCredential()
    #     token = credential.get_token(scope)
        
    #     # Process the token into the required binary structure
    #     token_bytes = bytes(token.token, "UTF-8")
    #     expanded_token = b''

    #     for byte in token_bytes:
    #         expanded_token += bytes({byte})
    #         expanded_token += bytes(1)
        
    #     return struct.pack("=i", len(expanded_token)) + expanded_token

    def read_from_db(self, otap: str, sql_query: str) -> pd.DataFrame:
        """
        Executes a SQL query against a specified database and returns the results as a DataFrame.

        Parameters:
        - otap (str): Environment specifier (e.g., 'dev', 'test', 'acc', 'prod').
        - sql_query (str): The SQL query to execute.

        Returns:
        - DataFrame: Query results as a DataFrame.
        """
        # Define server and database information
        server = f"ssdena{otap}.database.windows.net"
        database = "DB_DENA_DWH"
        
        # Build connection string with the SQL access token
        connection_string = (
            f"Driver={{ODBC Driver 18 for SQL Server}};SERVER={server};"
            f"DATABASE={database};TrustServerCertificate=yes"
        )
        sql_copt_ss_access_token = 1256  # Constant for SQL Server access token attribute
        
        # Connect to the database
        conn = pyodbc.connect(
            connection_string,
            attrs_before={sql_copt_ss_access_token: self.token_structure}
        )
        
        # Execute SQL query and fetch all rows
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convert fetched rows to DataFrame
        return pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    
    

