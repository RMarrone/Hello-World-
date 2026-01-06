# Syntopical Reading Agent

An AI-powered agent that implements the **syntopical reading** method from Mortimer Adler's classic book *"How to Read a Book"*. This tool helps you analyze multiple sources on a topic and synthesize them into a coherent, insightful post that maps the intellectual landscape.

## 📚 What is Syntopical Reading?

Syntopical reading (also called comparative reading) is the highest level of reading according to Adler. Unlike reading a single book for comprehension, syntopical reading involves:

1. Reading multiple sources on the same topic
2. Finding common ground across authors
3. Identifying where they agree and disagree
4. Synthesizing a new understanding that transcends any single source

This agent automates and enhances this process using AI to help you create thoughtful, well-researched posts.

## 🎯 The Five Stages

The agent implements Adler's five-stage syntopical reading process:

### Stage 1: Survey and Find Relevant Passages
- Inspects each document for relevance
- Identifies key passages that address your topic
- Extracts each author's main themes and stance

### Stage 2: Bring Authors to Terms
- Establishes common vocabulary across all sources
- Maps equivalent terms (different words, same concept)
- Distinguishes homonyms (same word, different meanings)
- Creates unified definitions

### Stage 3: Get the Questions Clear
- Identifies the fundamental questions all authors address
- Frames questions neutrally (unbiased)
- Orders questions logically
- Ensures comprehensive coverage of all perspectives

### Stage 4: Define the Issues
- Maps where authors agree and disagree
- Shows how each author answers each question
- Identifies the nature of disagreements (factual, value-based, definitional)
- Charts the spectrum of positions

### Stage 5: Analyze and Synthesize
- Creates a coherent analysis transcending individual sources
- Identifies patterns and deeper insights
- Generates original understanding from the conversation
- Produces a well-structured post

## 🚀 Quick Start

### Installation

```bash
# Clone or download this repository
cd syntopical-reading-agent

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Set up API Key

```bash
# For Claude (recommended)
export ANTHROPIC_API_KEY="your-api-key-here"

# Or for OpenAI
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

#### Option 1: Command Line

```bash
# Using a config file
python -m syntopical_reading_agent.cli \
  --config examples/config_example.json \
  --topic "What is the nature of consciousness?"

# Using individual files
python -m syntopical_reading_agent.cli \
  --topic "What makes a good leader?" \
  --file article1.txt --author "Simon Sinek" \
  --file article2.txt --author "Brené Brown" \
  --url https://example.com/leadership-article
```

#### Option 2: Python API

```python
from syntopical_reading_agent import create_syntopical_post

sources = [
    {"type": "file", "path": "article1.txt", "author": "Author One"},
    {"type": "file", "path": "article2.txt", "author": "Author Two"},
    {"type": "url", "url": "https://example.com/article"}
]

post = create_syntopical_post(
    sources=sources,
    topic="What is creativity?",
    provider="claude",
    output_format="blog"
)

print(post)
```

## 📖 Detailed Usage

### Using Configuration Files

Create a JSON config file:

```json
{
  "topic": "What is the nature of creativity?",
  "sources": [
    {
      "type": "file",
      "path": "creativity1.txt",
      "author": "Mihaly Csikszentmihalyi",
      "title": "Flow and Creativity"
    },
    {
      "type": "url",
      "url": "https://example.com/creativity-research",
      "author": "Teresa Amabile"
    }
  ],
  "output_format": "blog",
  "provider": "claude"
}
```

Then run:

```bash
python -m syntopical_reading_agent.cli --config your_config.json --topic "Your question"
```

### Python API - Advanced Usage

```python
from syntopical_reading_agent import SyntopicalReadingAgent, DocumentLoader

# Load documents
documents = [
    DocumentLoader.load_from_file("article1.txt", author="Author One"),
    DocumentLoader.load_from_url("https://example.com/article", author="Author Two"),
    DocumentLoader.load_from_text("Some text content...", title="My Notes", author="Me")
]

# Create agent
agent = SyntopicalReadingAgent(provider_name="claude")

# Run analysis
results = agent.read(
    documents=documents,
    topic="What is the future of AI?",
    output_format="blog",  # or "academic" or "essay"
    save_intermediates=True
)

# Access intermediate results
survey = agent.get_stage_result("stage1_survey")
terminology = agent.get_stage_result("stage2_terminology")
questions = agent.get_stage_result("stage3_questions")
issues = agent.get_stage_result("stage4_issues")

# Get final post
final_post = results['final_post']
print(final_post)
```

### Supported Source Types

1. **Local Files**: Text files, markdown, etc.
   ```python
   {"type": "file", "path": "document.txt", "author": "Jane Doe", "title": "My Article"}
   ```

2. **URLs**: Web pages (text will be extracted)
   ```python
   {"type": "url", "url": "https://example.com/article", "author": "John Smith"}
   ```

3. **Direct Text**: Inline text content
   ```python
   {"type": "text", "text": "Your content here...", "title": "My Notes", "author": "Me"}
   ```

### LLM Providers

#### Claude (Default)
```python
agent = SyntopicalReadingAgent(
    provider_name="claude",
    model="claude-sonnet-4-20250514",  # or claude-opus-4-20250514
    api_key="your-key"  # optional, uses env var by default
)
```

#### OpenAI
```python
agent = SyntopicalReadingAgent(
    provider_name="openai",
    model="gpt-4-turbo-preview",
    api_key="your-key"
)
```

### Output Formats

- **blog**: Engaging blog post for general audience
- **academic**: Formal academic style with structured sections
- **essay**: Thoughtful essay exploring the topic in depth

## 📁 Project Structure

```
syntopical_reading_agent/
├── __init__.py              # Package initialization
├── __main__.py              # Entry point for CLI
├── syntopical_agent.py      # Main agent orchestrator
├── llm_providers.py         # LLM abstraction layer
├── document_loader.py       # Document loading utilities
├── cli.py                   # Command-line interface
├── stages/                  # Individual reading stages
│   ├── __init__.py
│   ├── stage1_survey.py
│   ├── stage2_terminology.py
│   ├── stage3_questions.py
│   ├── stage4_issues.py
│   └── stage5_synthesis.py
└── examples/                # Usage examples
    ├── config_example.json
    └── python_usage_example.py
```

## 🔧 Advanced Features

### Accessing Intermediate Results

All intermediate stage results are saved automatically:

```python
results = agent.read(documents, topic)

# Full results include:
# - results['stage1_survey']
# - results['stage2_terminology']
# - results['stage3_questions']
# - results['stage4_issues']
# - results['stage5_synthesis']
# - results['final_post']
```

Results are also saved to `syntopical_output/` directory:
- Full JSON with all stages: `{topic}_{timestamp}_full.json`
- Final markdown post: `{topic}_{timestamp}_post.md`

### Custom Output Path

```bash
python -m syntopical_reading_agent.cli \
  --config sources.json \
  --topic "Your topic" \
  --output my_custom_post.md
```

### Disable Saving Intermediates

```python
results = agent.read(documents, topic, save_intermediates=False)
```

Or via CLI:
```bash
python -m syntopical_reading_agent.cli --config sources.json --topic "Topic" --no-save
```

## 💡 Tips for Best Results

1. **Choose Diverse Sources**: Include authors with different perspectives
2. **Quality Over Quantity**: 3-5 good sources often better than 10 mediocre ones
3. **Provide Context**: Include author names and titles when possible
4. **Frame Good Questions**: Your topic should be a clear, focused question
5. **Review Intermediates**: Check the JSON output to see how the agent analyzed each stage

## 📝 Example Topics

Good syntopical reading topics:
- "What is the nature of consciousness?"
- "How should AI be regulated?"
- "What makes a good leader?"
- "Is free will real?"
- "What is the future of work?"
- "How do we solve climate change?"

## 🤝 Contributing

This is an open-source project. Contributions welcome!

Areas for improvement:
- Additional LLM providers
- Support for PDF documents
- Better citation management
- Interactive mode
- Web interface

## 📚 Further Reading

- *How to Read a Book* by Mortimer Adler and Charles Van Doren
- The concept of syntopical reading is explained in Part IV of the book
- [Farnam Street summary of syntopical reading](https://fs.blog/syntopical-reading/)

## ⚖️ License

MIT License - feel free to use and modify as needed.

## 🙏 Acknowledgments

Inspired by Mortimer Adler's timeless work on reading and critical thinking. This tool aims to make the powerful technique of syntopical reading more accessible through AI assistance.

---

**Note**: This agent is a tool to assist your thinking, not replace it. Always critically evaluate the synthesis and bring your own judgment to the conversation.
