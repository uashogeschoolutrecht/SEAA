import requests
import pandas as pd
import os
from typing import Dict, List, Any, Optional
import time
import json

class CBSOpenDataAPI:
    """
    A class to interact with the CBS Open Data API and save results to CSV files.
    """
    
    BASE_URL = "https://opendata.cbs.nl/ODataApi/odata"
    
    def __init__(self, dataset_id: str = "85516NED"):
        """
        Initialize the API client.
        
        Args:
            dataset_id: The ID of the dataset to query (default: 85516NED)
        """
        self.dataset_id = dataset_id
        
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Store available tables
        self.available_tables = []
    
    def get_dataset_info(self) -> Dict:
        """
        Get metadata about the dataset and store available tables.
        
        Returns:
            Dictionary containing dataset metadata
        """
        endpoint = f"/{self.dataset_id}"
        response = self._make_request(endpoint)
        
        if response:
            # Save raw metadata as JSON
            self._save_to_json(response, f"{self.dataset_id}_metadata")
            
            # Store available tables
            if "value" in response:
                self.available_tables = [item["name"] for item in response["value"]]
                print(f"Available tables: {', '.join(self.available_tables)}")
            
            return response
        
        return {}
    
    def get_all_tables(self, top: int = None) -> Dict[str, pd.DataFrame]:
        """
        Get data from all available tables in the dataset.
        
        Args:
            top: Optional limit on the number of records to fetch per table
            
        Returns:
            Dictionary mapping table names to their respective DataFrames
        """
        # First ensure we have the list of available tables
        if not self.available_tables:
            self.get_dataset_info()
        
        results = {}
        
        for table_name in self.available_tables:
            print(f"Fetching table: {table_name}")
            df = self.get_table(table_name, top=top)
            results[table_name] = df
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
        return results
    
    def get_table(self, table_name: str, top: int = None, 
                  skip: int = None, select: str = None, 
                  filter_query: str = None) -> pd.DataFrame:
        """
        Get data from a specific table with optional filtering and selection.
        
        Args:
            table_name: Name of the table to fetch
            top: Maximum number of records to return
            skip: Number of records to skip
            select: Comma-separated list of columns to select
            filter_query: OData filter query
            
        Returns:
            DataFrame containing the table data
        """
        endpoint = f"/{self.dataset_id}/{table_name}"
        params = {}
        
        if top is not None:
            params["$top"] = top
        if skip is not None:
            params["$skip"] = skip
        if select is not None:
            params["$select"] = select
        if filter_query is not None:
            params["$filter"] = filter_query
            
        response = self._make_request(endpoint, params)
        
        if response and "value" in response:
            df = pd.DataFrame(response["value"])
            
            # Create a descriptive filename based on the query parameters
            filename_parts = [self.dataset_id, table_name]
            if top is not None:
                filename_parts.append(f"top{top}")
            if skip is not None:
                filename_parts.append(f"skip{skip}")
            if filter_query is not None:
                # Create a simplified version of the filter for the filename
                simple_filter = filter_query.replace(" ", "").replace("'", "")[:30]
                filename_parts.append(f"filter_{simple_filter}")
                
            filename = "_".join(filename_parts)
            self._save_to_parquet(df, filename)
            return df
        
        return pd.DataFrame()
    
    def get_dimensions(self) -> pd.DataFrame:
        """
        Get the dimensions (variables) available in the dataset.
        
        Returns:
            DataFrame containing the dimensions
        """
        endpoint = f"/{self.dataset_id}/DataProperties"
        response = self._make_request(endpoint)
        
        if response and "value" in response:
            df = pd.DataFrame(response["value"])
            self._save_to_csv(df, f"{self.dataset_id}_dimensions")
            return df
        
        return pd.DataFrame()
    
    def get_dimension_values(self, dimension: str) -> pd.DataFrame:
        """
        Get all possible values for a specific dimension.
        
        Args:
            dimension: The name of the dimension
            
        Returns:
            DataFrame containing the dimension values
        """
        endpoint = f"/{self.dataset_id}/{dimension}"
        response = self._make_request(endpoint)
        
        if response and "value" in response:
            df = pd.DataFrame(response["value"])
            self._save_to_csv(df, f"{self.dataset_id}_{dimension}_values")
            return df
        
        return pd.DataFrame()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a request to the API.
        
        Args:
            endpoint: API endpoint to call
            params: Optional query parameters
            
        Returns:
            JSON response as a dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
    
    def _save_to_csv(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save a DataFrame to a CSV file in the output directory.
        
        Args:
            df: DataFrame to save
            filename: Name for the CSV file (without extension)
        """
        if df.empty:
            print(f"No data to save for {filename}")
            return
            
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    
    def _save_to_json(self, data: Dict, filename: str) -> None:
        """
        Save a dictionary to a JSON file in the output directory.
        
        Args:
            data: Dictionary to save
            filename: Name for the JSON file (without extension)
        """
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filepath}")

    def _save_to_parquet(self, df: pd.DataFrame, filename: str) -> None:
        """
        Save a DataFrame to a Parquet file in the output directory.
        
        Args:
            df: DataFrame to save
            filename: Name for the Parquet file (without extension)
        """
        if df.empty:
            print(f"No data to save for {filename}")
            return
        
        filepath = os.path.join(self.output_dir, f"{filename}.parquet")
        df.to_parquet(filepath, index=False)
        print(f"Data saved to {filepath}")


def main():
    """
    Example usage of the CBSOpenDataAPI class.
    """
    # Initialize the API client with the 85516NED dataset
    api = CBSOpenDataAPI(dataset_id="85516NED")
    
    # Get and save dataset metadata
    api.get_dataset_info()
    
    # Get and save all tables
    # You can limit the number of records per table by setting the top parameter
    # For example: api.get_all_tables(top=1000)
    api.get_all_tables()
    
    # Alternatively, you can fetch specific tables individually
    # api.get_table("TableInfos")
    # api.get_table("TypedDataSet", top=1000)
    # api.get_table("Woonplaatsen")
    
    # Example: Get data with filtering from a specific table
    # api.get_table("TypedDataSet", filter_query="Perioden eq '2020JJ00'")
    
    # Example: Get data with specific columns from a specific table
    # api.get_table("TypedDataSet", select="RegioS,Perioden,BevolkingAantal")


def extract_plaatsnamen():
    """
    Extract the Title column from the 85516NED_Woonplaatsen.parquet file
    and save it to a text file called plaatsnamen.txt
    """
    # Define file paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "output", "85516NED_Woonplaatsen.parquet")
    output_file = os.path.join(base_dir, "dict", "plaatsnamen.txt")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return False
    
    try:
        # Read the parquet file
        df = pd.read_parquet(input_file)
        
        # Check if 'Title' column exists
        if 'Title' not in df.columns:
            print(f"Error: 'Title' column not found in {input_file}.")
            # Try to find a similar column
            print(f"Available columns: {', '.join(df.columns)}")
            return False
        
        # Extract the Title column and save to text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for place_name in df['Title'].sort_values():
                f.write(f"{place_name}\n")
        
        print(f"Successfully extracted {len(df)} place names to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error processing the file: {e}")
        return False

if __name__ == "__main__":
    main()
    extract_plaatsnamen() 
    