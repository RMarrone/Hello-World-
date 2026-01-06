"""
Document Loader

Handles loading documents from various sources (files, URLs, etc.)
"""

from typing import List, Dict, Optional
from pathlib import Path
import re


class Document:
    """Represents a document with metadata."""

    def __init__(self, content: str, source: str, title: Optional[str] = None, author: Optional[str] = None):
        """
        Initialize a document.

        Args:
            content: The document content
            source: Source identifier (file path, URL, etc.)
            title: Optional document title
            author: Optional author name
        """
        self.content = content
        self.source = source
        self.title = title or self._extract_title_from_source(source)
        self.author = author or "Unknown"

    def _extract_title_from_source(self, source: str) -> str:
        """Extract a reasonable title from the source identifier."""
        if source.startswith("http"):
            return source
        path = Path(source)
        return path.stem.replace("_", " ").replace("-", " ").title()

    def __repr__(self):
        return f"Document(title='{self.title}', source='{self.source}', author='{self.author}')"


class DocumentLoader:
    """Loads documents from various sources."""

    @staticmethod
    def load_from_file(file_path: str, title: Optional[str] = None, author: Optional[str] = None) -> Document:
        """
        Load a document from a file.

        Args:
            file_path: Path to the file
            title: Optional title (defaults to filename)
            author: Optional author

        Returns:
            Document instance
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return Document(content=content, source=str(path), title=title, author=author)

    @staticmethod
    def load_from_url(url: str, title: Optional[str] = None, author: Optional[str] = None) -> Document:
        """
        Load a document from a URL.

        Args:
            url: URL to fetch
            title: Optional title (defaults to URL)
            author: Optional author

        Returns:
            Document instance
        """
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("requests and beautifulsoup4 required for URL loading. "
                            "Install with: pip install requests beautifulsoup4")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Try to extract title from HTML if not provided
        if not title and soup.title:
            title = soup.title.string

        return Document(content=text, source=url, title=title, author=author)

    @staticmethod
    def load_from_text(text: str, source: str = "inline", title: Optional[str] = None,
                      author: Optional[str] = None) -> Document:
        """
        Load a document from a text string.

        Args:
            text: The document text
            source: Source identifier
            title: Optional title
            author: Optional author

        Returns:
            Document instance
        """
        return Document(content=text, source=source, title=title, author=author)

    @staticmethod
    def load_multiple(sources: List[Dict]) -> List[Document]:
        """
        Load multiple documents from a list of source specifications.

        Args:
            sources: List of dicts with keys: type, path/url/text, title (optional), author (optional)
                    Example: [
                        {"type": "file", "path": "doc.txt", "author": "John"},
                        {"type": "url", "url": "https://example.com"},
                        {"type": "text", "text": "Some content", "title": "My Doc"}
                    ]

        Returns:
            List of Document instances
        """
        documents = []

        for spec in sources:
            doc_type = spec.get("type", "").lower()
            title = spec.get("title")
            author = spec.get("author")

            if doc_type == "file":
                doc = DocumentLoader.load_from_file(spec["path"], title=title, author=author)
            elif doc_type == "url":
                doc = DocumentLoader.load_from_url(spec["url"], title=title, author=author)
            elif doc_type == "text":
                doc = DocumentLoader.load_from_text(spec["text"], title=title, author=author)
            else:
                raise ValueError(f"Unknown document type: {doc_type}")

            documents.append(doc)

        return documents
