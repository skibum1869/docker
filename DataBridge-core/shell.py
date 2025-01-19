#!/usr/bin/env python3
"""
DataBridge interactive CLI.
Assumes a DataBridge server is running.

Usage:
    Without authentication (connects to localhost):
        python shell.py
    
    With authentication:
        python shell.py <uri>
        Example: python shell.py "databridge://user:token@localhost:8000"

This provides the exact same interface as the Python SDK:
    db.ingest_text("content", metadata={...})
    db.ingest_file("path/to/file")
    db.query("what are the key findings?")
    etc...
"""

import sys
from pathlib import Path
import time
import requests

# Add local SDK to path before other imports
_SDK_PATH = str(Path(__file__).parent / "sdks" / "python")
if _SDK_PATH not in sys.path:
    sys.path.insert(0, _SDK_PATH)

from databridge import DataBridge  # noqa: E402


class DB:
    def __init__(self, uri: str = None):
        """Initialize DataBridge with optional URI"""
        self._client = DataBridge(uri, is_local=True, timeout=1000)
        self.base_url = "http://localhost:8000"  # For health check only

    def check_health(self, max_retries=30, retry_interval=1) -> bool:
        """Check if DataBridge server is healthy with retries"""
        health_url = f"{self.base_url}/health"

        for attempt in range(max_retries):
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass

            if attempt < max_retries - 1:
                print(
                    f"Waiting for DataBridge server to be ready... (attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(retry_interval)

        return False

    def ingest_text(self, content: str, metadata: dict = None) -> dict:
        """Ingest text content into DataBridge"""
        doc = self._client.ingest_text(content, metadata=metadata or {})
        return doc.model_dump()

    def ingest_file(
        self, file: str, filename: str, metadata: dict = None, content_type: str = None
    ) -> dict:
        """Ingest a file into DataBridge"""
        file_path = Path(file)
        doc = self._client.ingest_file(
            file=file_path, filename=filename, content_type=content_type, metadata=metadata or {}
        )
        return doc.model_dump()

    def retrieve_chunks(
        self, query: str, filters: dict = None, k: int = 4, min_score: float = 0.0
    ) -> list:
        """Search for relevant chunks"""
        results = self._client.retrieve_chunks(
            query, filters=filters or {}, k=k, min_score=min_score
        )
        return [r.model_dump() for r in results]

    def retrieve_docs(
        self, query: str, filters: dict = None, k: int = 4, min_score: float = 0.0
    ) -> list:
        """Retrieve relevant documents"""
        results = self._client.retrieve_docs(query, filters=filters or {}, k=k, min_score=min_score)
        return [r.model_dump() for r in results]

    def query(
        self,
        query: str,
        filters: dict = None,
        k: int = 4,
        min_score: float = 0.0,
        max_tokens: int = None,
        temperature: float = None,
    ) -> dict:
        """Generate completion using relevant chunks as context"""
        response = self._client.query(
            query,
            filters=filters or {},
            k=k,
            min_score=min_score,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.model_dump()

    def list_documents(self, skip: int = 0, limit: int = 100, filters: dict = None) -> list:
        """List accessible documents"""
        docs = self._client.list_documents(skip=skip, limit=limit, filters=filters or {})
        return [doc.model_dump() for doc in docs]

    def get_document(self, document_id: str) -> dict:
        """Get document metadata by ID"""
        doc = self._client.get_document(document_id)
        return doc.model_dump()

    def close(self):
        """Close the client connection"""
        self._client.close()


if __name__ == "__main__":
    uri = sys.argv[1] if len(sys.argv) > 1 else None
    db = DB(uri)

    # Check server health
    if not db.check_health():
        print("Error: Could not connect to DataBridge server")
        sys.exit(1)

    print("\nConnected to DataBridge")

    # Start an interactive Python shell with 'db' already imported
    import code
    import readline  # Enable arrow key history
    import rlcompleter  # noqa: F401 # Enable tab completion

    readline.parse_and_bind("tab: complete")

    # Create the interactive shell
    shell = code.InteractiveConsole(locals())

    # Print welcome message
    print("\nDataBridge CLI ready to use. The 'db' object is available with all SDK methods.")
    print("Example: db.ingest_text('hello world')")
    print("Type help(db) for documentation.")

    # Start the shell
    shell.interact(banner="")
