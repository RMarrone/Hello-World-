"""
Syntopical Reading Agent

Main orchestrator for the syntopical reading process.
Implements the method from "How to Read a Book" by Mortimer Adler.
"""

from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime

from .document_loader import Document, DocumentLoader
from .llm_providers import LLMProvider, get_provider
from .stages import (
    SurveyStage,
    TerminologyStage,
    QuestionsStage,
    IssuesStage,
    SynthesisStage
)


class SyntopicalReadingAgent:
    """
    Main agent that orchestrates the syntopical reading process.

    The agent executes five stages:
    1. Survey and find relevant passages
    2. Bring authors to terms (establish common vocabulary)
    3. Get the questions clear
    4. Define the issues (map agreements/disagreements)
    5. Analyze and synthesize the discussion
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None,
                 provider_name: str = "claude", **provider_kwargs):
        """
        Initialize the Syntopical Reading Agent.

        Args:
            llm_provider: Optional LLMProvider instance. If not provided, one will be created.
            provider_name: Name of LLM provider to use if llm_provider not given (default: "claude")
            **provider_kwargs: Additional kwargs for the provider (e.g., api_key, model)
        """
        if llm_provider is None:
            llm_provider = get_provider(provider_name, **provider_kwargs)

        self.llm = llm_provider

        # Initialize all stages
        self.stage1 = SurveyStage(self.llm)
        self.stage2 = TerminologyStage(self.llm)
        self.stage3 = QuestionsStage(self.llm)
        self.stage4 = IssuesStage(self.llm)
        self.stage5 = SynthesisStage(self.llm)

        # Store intermediate results
        self.results = {}

    def read(self, documents: List[Document], topic: str,
             output_format: str = "blog", save_intermediates: bool = True) -> Dict:
        """
        Execute the complete syntopical reading process.

        Args:
            documents: List of documents to analyze
            topic: The research topic/question
            output_format: Format for final output ("blog", "academic", "essay")
            save_intermediates: Whether to save intermediate results

        Returns:
            Dict containing all results including the final synthesis
        """
        print(f"\n{'='*60}")
        print(f"Starting Syntopical Reading on: {topic}")
        print(f"Analyzing {len(documents)} documents")
        print(f"{'='*60}\n")

        # Stage 1: Survey
        print("Stage 1/5: Surveying documents and finding relevant passages...")
        survey_results = self.stage1.execute(documents, topic)
        self.results['stage1_survey'] = survey_results
        print(f"  ✓ Surveyed {survey_results['documents_surveyed']} documents\n")

        # Stage 2: Terminology
        print("Stage 2/5: Establishing common terminology...")
        terminology_results = self.stage2.execute(survey_results, topic)
        self.results['stage2_terminology'] = terminology_results
        print("  ✓ Common vocabulary established\n")

        # Stage 3: Questions
        print("Stage 3/5: Clarifying key questions...")
        questions_results = self.stage3.execute(survey_results, terminology_results, topic)
        self.results['stage3_questions'] = questions_results
        print("  ✓ Key questions identified\n")

        # Stage 4: Issues
        print("Stage 4/5: Mapping agreements and disagreements...")
        issues_results = self.stage4.execute(
            survey_results, terminology_results, questions_results, topic
        )
        self.results['stage4_issues'] = issues_results
        print("  ✓ Issues mapped\n")

        # Stage 5: Synthesis
        print("Stage 5/5: Creating synthesis...")
        synthesis_results = self.stage5.execute(
            survey_results, terminology_results, questions_results,
            issues_results, topic, output_format
        )
        self.results['stage5_synthesis'] = synthesis_results
        print("  ✓ Synthesis complete\n")

        # Compile final results
        final_results = {
            "topic": topic,
            "output_format": output_format,
            "timestamp": datetime.now().isoformat(),
            "num_documents": len(documents),
            "documents": [
                {"title": doc.title, "author": doc.author, "source": doc.source}
                for doc in documents
            ],
            "stage1_survey": survey_results,
            "stage2_terminology": terminology_results,
            "stage3_questions": questions_results,
            "stage4_issues": issues_results,
            "stage5_synthesis": synthesis_results,
            "final_post": synthesis_results['synthesis']
        }

        if save_intermediates:
            self._save_results(final_results, topic)

        print(f"{'='*60}")
        print("Syntopical Reading Complete!")
        print(f"{'='*60}\n")

        return final_results

    def _save_results(self, results: Dict, topic: str):
        """Save results to files."""
        # Create output directory
        output_dir = Path("syntopical_output")
        output_dir.mkdir(exist_ok=True)

        # Create a safe filename from topic
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic[:50]  # Limit length
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save full results as JSON
        json_path = output_dir / f"{safe_topic}_{timestamp}_full.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"  → Full results saved to: {json_path}")

        # Save final post as markdown
        md_path = output_dir / f"{safe_topic}_{timestamp}_post.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Syntopical Reading: {results['topic']}\n\n")
            f.write(f"*Generated on {results['timestamp']}*\n\n")
            f.write(f"## Sources\n\n")
            for doc in results['documents']:
                f.write(f"- **{doc['title']}** by {doc['author']}\n")
            f.write(f"\n---\n\n")
            f.write(results['final_post'])
        print(f"  → Final post saved to: {md_path}")

    def get_stage_result(self, stage_name: str) -> Optional[Dict]:
        """
        Get results from a specific stage.

        Args:
            stage_name: Name of the stage (e.g., "stage1_survey", "stage5_synthesis")

        Returns:
            Stage results or None if not yet executed
        """
        return self.results.get(stage_name)

    def print_final_post(self):
        """Print the final synthesized post to console."""
        if 'stage5_synthesis' in self.results:
            print("\n" + "="*60)
            print("FINAL SYNTHESIZED POST")
            print("="*60 + "\n")
            print(self.results['stage5_synthesis']['synthesis'])
            print("\n" + "="*60 + "\n")
        else:
            print("No synthesis available yet. Run the agent first.")


# Convenience function
def create_syntopical_post(sources: List[Dict], topic: str,
                          provider: str = "claude",
                          output_format: str = "blog",
                          **provider_kwargs) -> str:
    """
    Convenience function to create a syntopical reading post.

    Args:
        sources: List of source dicts (see DocumentLoader.load_multiple)
        topic: Research topic
        provider: LLM provider name
        output_format: Output format ("blog", "academic", "essay")
        **provider_kwargs: Additional provider arguments (api_key, model, etc.)

    Returns:
        The final synthesized post as a string

    Example:
        post = create_syntopical_post(
            sources=[
                {"type": "file", "path": "article1.txt", "author": "Smith"},
                {"type": "url", "url": "https://example.com/article2"}
            ],
            topic="What is consciousness?",
            provider="claude"
        )
    """
    # Load documents
    documents = DocumentLoader.load_multiple(sources)

    # Create and run agent
    agent = SyntopicalReadingAgent(provider_name=provider, **provider_kwargs)
    results = agent.read(documents, topic, output_format=output_format)

    return results['final_post']
