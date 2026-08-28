import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

from src.data.config import get_blob_connection_string

blob_service_client = BlobServiceClient.from_connection_string(
    get_blob_connection_string()
)


def upload_file_to_blob(container_name: str, file_path: str, blob_name: str):
    container_client = blob_service_client.get_container_client(container_name)

    if not container_client.exists():
        container_client.create_container()

    blob_client = container_client.get_blob_client(blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(
        f"File '{file_path}' uploaded to container '{container_name}' as '{blob_name}'."
    )
