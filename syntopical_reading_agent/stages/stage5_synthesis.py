"""
Stage 5: Analyze and Synthesize the Discussion

Creates a coherent analysis that transcends individual sources. This is where
the syntopical reading culminates in an original synthesis.
"""

from typing import Dict
from ..llm_providers import LLMProvider


class SynthesisStage:
    """
    Stage 5: Analyze and synthesize the conversation.

    This stage:
    1. Analyzes the overall conversation
    2. Identifies patterns and insights across sources
    3. Evaluates the strength of different positions
    4. Synthesizes into a coherent post
    5. Generates original insights from the conversation
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider

    def execute(self, survey_results: Dict, terminology: Dict, questions: Dict,
                issues: Dict, topic: str, output_format: str = "blog") -> Dict:
        """
        Create final synthesis and post.

        Args:
            survey_results: Results from Stage 1
            terminology: Results from Stage 2
            questions: Results from Stage 3
            issues: Results from Stage 4
            topic: The research topic
            output_format: Output format ("blog", "academic", "essay")

        Returns:
            Dict with the final synthesized post
        """
        synthesis = self._create_synthesis(
            survey_results, terminology, questions, issues, topic, output_format
        )

        return {
            "topic": topic,
            "output_format": output_format,
            "synthesis": synthesis
        }

    def _create_synthesis(self, survey_results: Dict, terminology: Dict,
                         questions: Dict, issues: Dict, topic: str,
                         output_format: str) -> str:
        """Create the final synthesized post."""

        system_prompt = """You are an expert at syntopical reading, skilled at synthesizing multiple perspectives into a coherent analysis.

Your synthesis should:
- Present a balanced view of the conversation
- Identify patterns and deeper insights
- Be original (transcend any single source)
- Be clear and compelling
- Give credit to sources appropriately"""

        format_instructions = {
            "blog": "Write an engaging blog post for an educated general audience.",
            "academic": "Write in academic style with formal structure and citations.",
            "essay": "Write a thoughtful essay exploring the topic in depth."
        }

        doc_list = "\n".join([
            f"- {doc['title']} by {doc['author']}"
            for doc in survey_results["document_analyses"]
        ])

        prompt = f"""Topic: {topic}

SOURCES:
{doc_list}

COMMON TERMINOLOGY:
{terminology['common_vocabulary'][:2000]}

KEY QUESTIONS:
{questions['key_questions'][:2000]}

MAPPED ISSUES:
{issues['issues'][:3000]}

Now create a comprehensive synthesis. {format_instructions.get(output_format, format_instructions['blog'])}

Your post should:

1. INTRODUCTION
   - Introduce the topic and its significance
   - Preview the key questions and why they matter
   - Mention the range of perspectives you'll explore

2. BODY (organized by questions/themes)
   - Address each key question
   - Present different perspectives fairly
   - Highlight agreements and disagreements
   - Analyze the strengths and weaknesses of different positions
   - Identify patterns and connections across sources
   - Offer original insights that emerge from comparing sources

3. SYNTHESIS & INSIGHTS
   - What can we learn from this conversation as a whole?
   - Are there insights that emerge only from reading these sources together?
   - Where is there consensus? Where is there productive disagreement?
   - What questions remain unresolved?

4. CONCLUSION
   - Summarize key takeaways
   - Suggest implications or directions for further thinking

IMPORTANT:
- Attribute ideas to sources appropriately (mention author names)
- Be fair to all perspectives
- Your synthesis should be more than a summary - add value through analysis and connections
- Make it readable and engaging

Write the complete post now:"""

        response = self.llm.generate(prompt, system=system_prompt, max_tokens=4096)

        return response
