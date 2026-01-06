"""
Syntopical Reading Agent

An implementation of the syntopical reading method from "How to Read a Book"
by Mortimer Adler and Charles Van Doren.

This agent analyzes multiple sources on a topic and synthesizes them into a
coherent post that maps the intellectual landscape of the subject.
"""

from .syntopical_agent import SyntopicalReadingAgent
from .document_loader import DocumentLoader

__version__ = "0.1.0"
__all__ = ["SyntopicalReadingAgent", "DocumentLoader"]
