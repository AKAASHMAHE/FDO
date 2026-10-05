from pathlib import Path

import requests


class FusekiService:
    def __init__(
        self,
        base_url: str = "http://localhost:3030",
        dataset: str = "fdo",
    ):
        self.base_url = base_url.rstrip("/")
        self.dataset = dataset

    @property
    def query_url(self) -> str:
        return f"{self.base_url}/{self.dataset}/query"

    @property
    def update_url(self) -> str:
        return f"{self.base_url}/{self.dataset}/update"

    @property
    def data_url(self) -> str:
        return f"{self.base_url}/{self.dataset}/data"

    def query(self, sparql: str) -> dict:
        response = requests.post(
            self.query_url,
            data={"query": sparql},
            headers={
                "Accept": "application/sparql-results+json"
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def upload_rdf(
        self,
        rdf_path: str | Path,
        content_type: str = "text/turtle",
    ) -> None:
        path = Path(rdf_path)

        with path.open("rb") as file:
            response = requests.post(
                self.data_url,
                data=file,
                headers={
                    "Content-Type": content_type
                },
                timeout=60,
            )

        response.raise_for_status()

    def clear_default_graph(self) -> None:
        response = requests.post(
            self.update_url,
            data={"update": "CLEAR DEFAULT"},
            headers={
                "Content-Type": (
                    "application/x-www-form-urlencoded"
                )
            },
            timeout=30,
        )

        response.raise_for_status()