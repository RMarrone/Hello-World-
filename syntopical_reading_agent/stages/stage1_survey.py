"""
Stage 1: Survey and Find Relevant Passages

Inspects multiple sources to find passages relevant to the research topic.
This is a preparatory stage that identifies what content is actually useful.
"""

from typing import List, Dict
from ..document_loader import Document
from ..llm_providers import LLMProvider


class SurveyStage:
    """
    Stage 1: Survey the field and identify relevant passages.

    This stage examines each document to:
    1. Determine if it's relevant to the topic
    2. Extract key passages that address the topic
    3. Provide a brief summary of each document's perspective
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def execute(self, documents: List[Document], topic: str) -> Dict:
        """
        Survey documents and extract relevant passages.

        Args:
            documents: List of documents to survey
            topic: The research topic/question

        Returns:
            Dict with survey results including relevant passages per document
        """
        results = {
            "topic": topic,
            "documents_surveyed": len(documents),
            "document_analyses": []
        }

        for doc in documents:
            analysis = self._analyze_document(doc, topic)
            results["document_analyses"].append(analysis)

        return results

    def _analyze_document(self, document: Document, topic: str) -> Dict:
        """Analyze a single document for relevance and extract key passages."""

        system_prompt = """You are an expert at syntopical reading, as described in "How to Read a Book" by Mortimer Adler.

Your task is to survey a document and identify passages relevant to a specific research topic."""

        prompt = f"""Topic: {topic}

Document Title: {document.title}
Author: {document.author}
Source: {document.source}

Document Content:
{document.content[:15000]}

Please analyze this document and provide:

1. RELEVANCE SCORE (0-10): How relevant is this document to the topic?
2. KEY THEMES: What are the 2-3 main themes this document addresses related to the topic?
3. RELEVANT PASSAGES: Extract 3-5 specific passages (quotes with context) that directly address the topic
4. AUTHOR'S STANCE: What is the author's overall position or perspective on this topic?
5. UNIQUE CONTRIBUTION: What unique insight or angle does this source provide?

Format your response as structured sections with clear headings."""

        response = self.llm.generate(prompt, system=system_prompt, max_tokens=2000)

        return {
            "title": document.title,
            "author": document.author,
            "source": document.source,
            "analysis": response
        }
