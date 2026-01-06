#!/usr/bin/env python3
"""
Example: Using the Syntopical Reading Agent programmatically
"""

from syntopical_reading_agent import SyntopicalReadingAgent, DocumentLoader, create_syntopical_post

# Example 1: Simple usage with the convenience function
def example_1_simple():
    """Simplest way to create a syntopical post"""

    sources = [
        {
            "type": "file",
            "path": "article1.txt",
            "author": "Author One",
            "title": "First Perspective"
        },
        {
            "type": "file",
            "path": "article2.txt",
            "author": "Author Two",
            "title": "Second Perspective"
        },
        {
            "type": "url",
            "url": "https://example.com/article3",
            "author": "Author Three"
        }
    ]

    post = create_syntopical_post(
        sources=sources,
        topic="What makes a good leader?",
        provider="claude",
        output_format="blog"
    )

    print(post)


# Example 2: Step-by-step with full control
def example_2_detailed():
    """More detailed usage with access to intermediate results"""

    # Load documents manually
    documents = [
        DocumentLoader.load_from_file("article1.txt", author="Author One"),
        DocumentLoader.load_from_file("article2.txt", author="Author Two"),
        DocumentLoader.load_from_url("https://example.com/article3", author="Author Three")
    ]

    # Create agent
    agent = SyntopicalReadingAgent(provider_name="claude")

    # Run the analysis
    results = agent.read(
        documents=documents,
        topic="What makes a good leader?",
        output_format="blog",
        save_intermediates=True
    )

    # Access specific stages
    survey = agent.get_stage_result("stage1_survey")
    terminology = agent.get_stage_result("stage2_terminology")
    questions = agent.get_stage_result("stage3_questions")
    issues = agent.get_stage_result("stage4_issues")
    synthesis = agent.get_stage_result("stage5_synthesis")

    # Print the final post
    agent.print_final_post()

    # Or access it directly
    print(results['final_post'])


# Example 3: Using with OpenAI
def example_3_openai():
    """Using OpenAI instead of Claude"""

    sources = [
        {"type": "file", "path": "article1.txt", "author": "Author One"},
        {"type": "file", "path": "article2.txt", "author": "Author Two"}
    ]

    post = create_syntopical_post(
        sources=sources,
        topic="The future of AI",
        provider="openai",
        model="gpt-4-turbo-preview",
        output_format="academic"
    )

    print(post)


# Example 4: Working with text directly
def example_4_direct_text():
    """Loading documents from text strings"""

    text1 = """
    Leadership is about inspiring others to achieve a common goal.
    Great leaders communicate vision clearly and motivate their teams.
    """

    text2 = """
    Leadership requires emotional intelligence and the ability to understand
    and respond to the needs of team members.
    """

    documents = [
        DocumentLoader.load_from_text(text1, source="inline1",
                                     title="Leadership as Inspiration",
                                     author="Smith"),
        DocumentLoader.load_from_text(text2, source="inline2",
                                     title="Emotional Intelligence in Leadership",
                                     author="Jones")
    ]

    agent = SyntopicalReadingAgent(provider_name="claude")
    results = agent.read(
        documents=documents,
        topic="What are the key qualities of effective leadership?",
        output_format="essay"
    )

    print(results['final_post'])


# Example 5: Custom LLM provider
def example_5_custom_provider():
    """Using a custom LLM provider configuration"""

    from syntopical_reading_agent.llm_providers import ClaudeProvider

    # Create custom provider with specific settings
    llm = ClaudeProvider(
        model="claude-opus-4-20250514",  # Use a specific model
        api_key="your-api-key-here"  # Or use environment variable
    )

    # Load documents
    documents = DocumentLoader.load_multiple([
        {"type": "file", "path": "article1.txt", "author": "Author One"},
        {"type": "file", "path": "article2.txt", "author": "Author Two"}
    ])

    # Create agent with custom provider
    agent = SyntopicalReadingAgent(llm_provider=llm)

    results = agent.read(
        documents=documents,
        topic="How does technology impact society?",
        output_format="blog"
    )

    print(results['final_post'])


if __name__ == "__main__":
    # Run one of the examples
    print("Running Example 1: Simple Usage")
    print("="*60)

    # Uncomment to run:
    # example_1_simple()

    print("\nTo run other examples, uncomment them in the __main__ section")
