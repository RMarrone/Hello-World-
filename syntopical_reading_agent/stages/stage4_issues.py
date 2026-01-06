"""
Stage 4: Define the Issues

Maps out where authors agree and disagree on the questions. Issues arise when
authors give different answers to the same question.
"""

from typing import Dict
from ..llm_providers import LLMProvider


class IssuesStage:
    """
    Stage 4: Define the issues by mapping agreements and disagreements.

    This stage:
    1. Shows how each author answers each question
    2. Identifies where authors agree
    3. Identifies where authors disagree (the "issues")
    4. Clarifies the nature and significance of disagreements
    5. Maps the intellectual terrain of the conversation
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def execute(self, survey_results: Dict, terminology: Dict, questions: Dict, topic: str) -> Dict:
        """
        Map agreements and disagreements across sources.

        Args:
            survey_results: Results from Stage 1
            terminology: Results from Stage 2
            questions: Results from Stage 3
            topic: The research topic

        Returns:
            Dict with issues mapped
        """
        issues = self._map_issues(survey_results, terminology, questions, topic)

        return {
            "topic": topic,
            "issues": issues
        }

    def _map_issues(self, survey_results: Dict, terminology: Dict, questions: Dict, topic: str) -> str:
        """Map where authors agree and disagree."""

        system_prompt = """You are an expert at syntopical reading, skilled at mapping intellectual conversations and identifying where thinkers agree and disagree.

Your task is to show how different authors answer the same questions, highlighting both consensus and controversy."""

        # Build context from previous stages
        doc_analyses = "\n\n".join([
            f"## {doc['title']} by {doc['author']}\n{doc['analysis'][:2000]}"
            for doc in survey_results["document_analyses"]
        ])

        prompt = f"""Topic: {topic}

COMMON TERMINOLOGY:
{terminology['common_vocabulary'][:2000]}

KEY QUESTIONS:
{questions['key_questions'][:2000]}

DOCUMENT ANALYSES:
{doc_analyses[:8000]}

Now map the ISSUES - where authors agree and disagree. For each key question:

1. Show how EACH author answers it (use the established common terminology)
2. Identify AGREEMENTS: Where do authors converge? What is the consensus?
3. Identify DISAGREEMENTS (Issues): Where do authors diverge? What are they debating?
4. Characterize each issue:
   - What exactly is the disagreement about?
   - Is it a factual disagreement, a value disagreement, or a definitional one?
   - How significant is this disagreement?
5. Map the positions: Show the spectrum of views on each issue

Structure your response by question, showing for each:
- The question
- Each author's answer (brief summary)
- Areas of agreement
- Areas of disagreement (the issues)
- Analysis of the disagreement

Be fair to all perspectives. Don't take sides - your job is to map the conversation objectively."""

        response = self.llm.generate(prompt, system=system_prompt, max_tokens=4000)

        return response
