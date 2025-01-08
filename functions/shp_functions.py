from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class SHPFCA:
    def __init__(self):        
        """
        Initializes the SHPFCA object, setting up authentication credentials for SharePoint connection.
        """
        # Retrieve Azure Key credentials
        self.client_id = self.get_azure_key('KVK-SPK-SHA-PROD').split('@')[0]
        self.client_secret = self.get_azure_key('KVS-SPK-SHA-PROD')
        
        # Establish SharePoint context
        self.ctx = self.connect_to_sharepoint()

    def get_azure_key(self, key_name, vault_name='KV-DENA'):
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

    def print_id(self):
        """
        Prints the client ID for verification purposes.
        
        Returns:
        - str: The client ID.
        """
        return self.client_id

    def connect_to_sharepoint(self):
        """
        Establishes a SharePoint client context using client_id and client_secret.

        Returns:
        - ClientContext: A SharePoint client context established with the credentials.
        - None: If an error occurs during connection establishment.
        """
        site_url = "https://hogeschoolutrecht.sharepoint.com/sites/MDW-FCA-DA-P"
        try:
            # Initialize authentication context
            context_auth = AuthenticationContext(site_url)

            # Attempt to acquire token for the application
            if context_auth.acquire_token_for_app(
                client_id=self.client_id, client_secret=self.client_secret
            ):
                # Return client context if successful
                ctx = ClientContext(site_url, context_auth)
                return ctx
        except Exception as e:
            # Print error message if exception occurs
            print(f"Error: {type(e).__name__} {e}")
            return None

    ## SHAREPOINT FUNCTIONS
    def read_from_sharepoint(self, shp_folder, shp_file_name):
        """
        Reads a file from SharePoint.

        Parameters:
        - shp_folder (str): The SharePoint folder path.
        - shp_file_name (str): The name of the file to be read.

        Returns:
        - response: The response object containing file content if the file is found.
        - None: If the file cannot be opened.
        """
        file_path = shp_folder + shp_file_name
        response = File.open_binary(self.ctx, file_path)

        # Check if the file was successfully retrieved
        if response.status_code == 200:
            return response
        else:
            print(f"Can't open file, status code: {response.status_code}")
            return None

    def upload_to_sharepoint(self, input_df, shp_file_name, shp_folder):
        """
        Uploads a DataFrame to SharePoint as an Excel file.

        Parameters:
        - input_df (DataFrame): The DataFrame to be uploaded.
        - shp_file_name (str): The target file name on SharePoint.
        - shp_folder (str): The target SharePoint folder.

        Returns:
        - None
        """
        # Copy DataFrame and convert it to a binary stream
        df = input_df.copy()
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        file_content = buffer.read()

        # Get target folder on SharePoint
        target_folder = self.ctx.web.get_folder_by_server_relative_url(shp_folder)

        # Upload file using ThreadPoolExecutor for concurrent execution
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = executor.submit(
                target_folder.upload_file, shp_file_name, file_content
            )
            if as_completed([future]):
                future.result().execute_query()
