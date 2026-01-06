"""
Stage 2: Bring the Authors to Terms

Establishes a common vocabulary across all sources. Different authors may use
different terms for the same concept, or the same term for different concepts.
"""

from typing import List, Dict
from ..llm_providers import LLMProvider


class TerminologyStage:
    """
    Stage 2: Establish common terminology across sources.

    This stage:
    1. Identifies key terms used by different authors
    2. Maps equivalent terms (different words, same concept)
    3. Distinguishes homonyms (same word, different meanings)
    4. Creates a unified vocabulary for discussion
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def execute(self, survey_results: Dict, topic: str) -> Dict:
        """
        Analyze terminology across all sources.

        Args:
            survey_results: Results from Stage 1 (survey)
            topic: The research topic

        Returns:
            Dict with terminology mapping and definitions
        """
        # Collect all analyses
        analyses = [doc["analysis"] for doc in survey_results["document_analyses"]]
        doc_info = [(doc["title"], doc["author"]) for doc in survey_results["document_analyses"]]

        terminology = self._establish_common_terms(analyses, doc_info, topic)

        return {
            "topic": topic,
            "common_vocabulary": terminology
        }

    def _establish_common_terms(self, analyses: List[str], doc_info: List[tuple], topic: str) -> str:
        """Create a common vocabulary across all sources."""

        system_prompt = """You are an expert at syntopical reading, specifically skilled at establishing common terminology across multiple authors.

Your task is to identify how different authors use terms, find synonyms and homonyms, and create a unified vocabulary."""

        # Combine analyses for context
        combined_analyses = "\n\n---\n\n".join([
            f"Source: {title} by {author}\n{analysis}"
            for (title, author), analysis in zip(doc_info, analyses)
        ])

        prompt = f"""Topic: {topic}

Below are analyses from multiple sources on this topic:

{combined_analyses[:12000]}

Please establish a COMMON TERMINOLOGY by:

1. KEY CONCEPTS: List the 5-10 most important concepts discussed across these sources

2. SYNONYMS: Identify cases where different authors use different terms for the same concept
   Format: "Concept X" - Author A calls it "term1", Author B calls it "term2"

3. HOMONYMS: Identify cases where the same term is used differently by different authors
   Format: "term" - For Author A means X, but for Author B means Y

4. UNIFIED DEFINITIONS: Provide clear, neutral definitions for each key concept that encompasses how all authors use it

5. IMPORTANT DISTINCTIONS: Note any crucial distinctions or nuances that must be preserved

Create a terminology guide that allows us to discuss all authors' ideas using consistent language."""

        response = self.llm.generate(prompt, system=system_prompt, max_tokens=3000)

        return response
