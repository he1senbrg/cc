import os
import random
import datetime

def download_dataset(data):
    """
    Get CSV dataset blob path from Azure Blob Storage based on ID
    
    Args:
        data: Dictionary containing 'id' field (e.g., "gwq", "gwr")
        
    Returns:
        str: Azure Blob Storage URL path to the CSV
    """
    print(f"Getting dataset blob path for ID: {data}")
    
    try:
        # Extract ID from data
        dataset_id = data.get('id')
        if dataset_id is None:
            raise ValueError("Missing 'id' field in request data")
        
        # Azure Blob Storage configuration
        # Using specific blob storage account with anonymous read access
        account_url = "https://aigisblob.blob.core.windows.net"
        container_name = "datasets"
        
        # Generate blob name based on ID
        blob_name = f"{dataset_id}.csv"
        
        # Construct the full blob URL
        blob_url = f"{account_url}/{container_name}/{blob_name}"
        
        print(f"Dataset blob URL: {blob_url}")
        return blob_url
    
    except Exception as e:
        print(f"Error getting dataset blob path: {e}")
        raise
