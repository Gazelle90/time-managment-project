import logging
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


KEY_VAULT_URL = os.getenv(
    "AZURE_KEY_VAULT_URL", "https://time-management-kv.vault.azure.net/"
)


def get_database_credentials():
    """Get database credentials from Azure Key Vault or environment variables."""

    try:
        if KEY_VAULT_URL:
            logger.info("Attempting to get credentials from Azure Key Vault...")

            credential = DefaultAzureCredential()

            secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

            # Hämta secrets från ditt Key Vault
            host = secret_client.get_secret("postgres-host").value
            database = secret_client.get_secret("postgres-database").value
            user = secret_client.get_secret("postgres-user").value
            password = secret_client.get_secret("postgres-password").value
            port = int(secret_client.get_secret("postgres-port").value)

            logger.info("Successfully retrieved credentials from Azure Key Vault")
            logger.info(
                f"Connecting to: host={host}, "
                f"database={database}, "
                f"user={user}, "
                f"port={port}"
            )

            return host, database, user, password, port

    except Exception as e:
        logger.warning(f"Could not get credentials from Key Vault: {e}")
        logger.info("Falling back to environment variables...")

    host = os.getenv("POSTGRES_HOST", "nazret-team-pg01.postgres.database.azure.com")
    database = os.getenv("POSTGRES_DB", "team_time_management")
    user = os.getenv("POSTGRES_USER", "pgadmin")
    password = os.getenv("POSTGRES_PASSWORD", "")

    port = int(os.getenv("POSTGRES_PORT", "5432"))

    logger.info("Using credentials from environment variables")
    logger.info(
        f"Connecting to: host={host}, database={database}, user={user}, port={port}"
    )

    return host, database, user, password, port


def get_blob_connection_string():
    """Get Blob Storage connection string from Azure Key Vault."""

    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

    return secret_client.get_secret("blob-storage-connection-string").value
