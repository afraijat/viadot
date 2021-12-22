from typing import Any, Dict

import sharepy

from ..config import local_config
from ..exceptions import CredentialError
from .base import Source


class Sharepoint(Source):
    """
    A Sharepoint class to connect and download specific Excel file from Sharepoint.

    Args:
        credentials (dict): In credentials should be included:
            "site" - Path to sharepoint website (e.g : {tenant_name}.sharepoint.com)
            "username" - Sharepoint username (e.g username@{tenant_name}.com)
            "password"
        download_from_path (str, optional): Full url to file
                        (e.g : https://{tenant_name}.sharepoint.com/sites/{directory}/Shared%20Documents/Dashboard/file). Defaults to None.
    """

    def __init__(
        self,
        credentials: Dict[str, Any] = None,
        download_from_path: str = None,
        *args,
        **kwargs,
    ):

        DEFAULT_CREDENTIALS = local_config.get("SHAREPOINT")
        credentials = credentials or DEFAULT_CREDENTIALS
        if credentials is None:
            raise CredentialError("Credentials not found.")
        self.url = download_from_path
        self.required_credentials = ["site", "username", "password"]
        super().__init__(*args, credentials=credentials, **kwargs)

    def get_connection(self) -> sharepy.session.SharePointSession:
        if any([rq not in self.credentials for rq in self.required_credentials]):
            raise CredentialError("Missing credentials.")

        return sharepy.connect(
            site=self.credentials["site"],
            username=self.credentials["username"],
            password=self.credentials["password"],
        )

    def download_file(
        self,
        url: str = None,
        download_to_path: str = "Sharepoint_file.xlsm",
    ) -> None:

        url = url or self.url
        if not url:
            raise CredentialError("Missing required parameter 'url'.")

        conn = self.get_connection()
        conn.getfile(
            url=url,
            filename=download_to_path,
        )
