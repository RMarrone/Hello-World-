# Examples

This directory contains examples for using the Syntopical Reading Agent.

## Files

- **config_example.json**: Template configuration file showing the JSON structure
- **test_config.json**: Working configuration file using the sample sources
- **python_usage_example.py**: Python code examples showing different usage patterns
- **sample_sources/**: Directory containing sample articles for testing

## Quick Test

To test the agent with the sample sources:

```bash
# From the repository root
python -m syntopical_reading_agent.cli \
  --config syntopical_reading_agent/examples/sample_sources/test_config.json \
  --topic "What does the future hold for artificial intelligence?"
```

Note: You'll need to set your API key first:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## Sample Sources

The `sample_sources/` directory contains three articles on AI's future:

1. **ai_future_article1.txt** - An optimistic perspective by Dr. Sarah Chen
2. **ai_future_article2.txt** - A cautious/critical perspective by Professor Marcus Thompson
3. **ai_future_article3.txt** - A balanced middle-path perspective by Dr. Amara Okafor

These demonstrate how the agent synthesizes different viewpoints into a coherent analysis.

## Creating Your Own Config

Use `config_example.json` as a template:

```json
{
  "topic": "Your research question here",
  "sources": [
    {
      "type": "file",
      "path": "path/to/your/document.txt",
      "author": "Author Name",
      "title": "Document Title"
    }
  ],
  "output_format": "blog"
}
```

Supported source types:
- `"type": "file"` - Local text files
- `"type": "url"` - Web pages (text extracted automatically)
- `"type": "text"` - Inline text content
