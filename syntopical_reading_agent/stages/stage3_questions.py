"""
Stage 3: Get the Questions Clear

Frames the key questions that the sources are addressing. The questions should
be neutral and comprehensive enough to encompass all perspectives.
"""

from typing import Dict
from ..llm_providers import LLMProvider


class QuestionsStage:
    """
    Stage 3: Clarify the questions being addressed.

    This stage:
    1. Identifies the fundamental questions all authors are addressing
    2. Frames questions neutrally (not biased toward any author)
    3. Orders questions logically
    4. Ensures questions are comprehensive enough to cover all perspectives
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def execute(self, survey_results: Dict, terminology: Dict, topic: str) -> Dict:
        """
        Clarify the key questions being addressed.

        Args:
            survey_results: Results from Stage 1
            terminology: Results from Stage 2
            topic: The research topic

        Returns:
            Dict with structured questions
        """
        questions = self._formulate_questions(survey_results, terminology, topic)

        return {
            "topic": topic,
            "key_questions": questions
        }

    def _formulate_questions(self, survey_results: Dict, terminology: Dict, topic: str) -> str:
        """Formulate the key questions being addressed across all sources."""

        system_prompt = """You are an expert at syntopical reading, skilled at identifying and framing the fundamental questions that multiple authors are addressing.

Your questions must be:
- Neutral (not biased toward any particular author's view)
- Comprehensive (broad enough to encompass all perspectives)
- Fundamental (getting at the core issues, not superficial)
- Clear and specific"""

        # Extract relevant context
        doc_summaries = "\n".join([
            f"- {doc['title']} by {doc['author']}"
            for doc in survey_results["document_analyses"]
        ])

        prompt = f"""Topic: {topic}

SOURCES ANALYZED:
{doc_summaries}

COMMON TERMINOLOGY:
{terminology['common_vocabulary'][:3000]}

Based on the survey of these sources and the established terminology, formulate the KEY QUESTIONS that these authors are addressing.

Structure your response as:

1. PRIMARY QUESTION: The main overarching question that all sources address

2. SUB-QUESTIONS: 4-8 more specific questions that break down the primary question
   - Each sub-question should be addressed by multiple sources
   - Questions should be ordered logically (build on each other)
   - Questions should be neutral and comprehensive

3. QUESTION RELATIONSHIPS: Briefly explain how the sub-questions relate to each other and to the primary question

Remember: Frame questions that ALL authors answer, not questions that only some address. The questions should organize the discussion, not favor any particular viewpoint."""

        response = self.llm.generate(prompt, system=system_prompt, max_tokens=2500)

        return response
