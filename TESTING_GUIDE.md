# Testing Guide for Syntopical Reading Agent

## Quick Start Testing

### Step 1: Basic Tests (No API Key Needed)

Test that all components load correctly:

```bash
python3 test_basic.py
```

This verifies:
- ✓ All imports work
- ✓ Document loading works
- ✓ Sample files are accessible
- ✓ Core functionality is intact

### Step 2: Full Test with LLM (Requires API Key)

#### Option A: Automated Test Script

```bash
# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the test
./test_agent.sh
```

#### Option B: Manual Test

```bash
# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the agent
python3 -m syntopical_reading_agent.cli \
  --config syntopical_reading_agent/examples/sample_sources/test_config.json \
  --topic "What does the future hold for artificial intelligence?"
```

## What to Expect

When you run the full test, you'll see:

```
============================================================
Starting Syntopical Reading on: What does the future hold for artificial intelligence?
Analyzing 3 documents
============================================================

Stage 1/5: Surveying documents and finding relevant passages...
  ✓ Surveyed 3 documents

Stage 2/5: Establishing common terminology...
  ✓ Common vocabulary established

Stage 3/5: Clarifying key questions...
  ✓ Key questions identified

Stage 4/5: Mapping agreements and disagreements...
  ✓ Issues mapped

Stage 5/5: Creating synthesis...
  ✓ Synthesis complete

============================================================
Syntopical Reading Complete!
============================================================
```

Then you'll see the final post printed to your terminal.

## Understanding the Output

After running, check the `syntopical_output/` directory:

```bash
ls -la syntopical_output/
```

You'll find two files:
1. **`*_full.json`** - Complete results from all 5 stages
2. **`*_post.md`** - The final synthesized post in markdown

### View the Final Post

```bash
cat syntopical_output/*_post.md
```

### Inspect Intermediate Stages

```bash
# Pretty print the full JSON
python3 -m json.tool syntopical_output/*_full.json | less
```

## Test With Your Own Documents

### Test with Local Files

```bash
python3 -m syntopical_reading_agent.cli \
  --topic "Your research question?" \
  --file your_article1.txt --author "Author Name" \
  --file your_article2.txt --author "Another Author"
```

### Test with URLs

```bash
python3 -m syntopical_reading_agent.cli \
  --topic "Your research question?" \
  --url https://example.com/article1 \
  --url https://example.com/article2
```

### Test with Custom Config

Create `my_test.json`:
```json
{
  "topic": "Your question here",
  "sources": [
    {
      "type": "file",
      "path": "path/to/document.txt",
      "author": "Author Name"
    }
  ]
}
```

Then run:
```bash
python3 -m syntopical_reading_agent.cli --config my_test.json --topic "Your question"
```

## Python API Testing

Create `test_api.py`:

```python
from syntopical_reading_agent import create_syntopical_post
import os

# Ensure API key is set
os.environ['ANTHROPIC_API_KEY'] = 'your-key-here'

sources = [
    {
        "type": "file",
        "path": "syntopical_reading_agent/examples/sample_sources/ai_future_article1.txt",
        "author": "Dr. Sarah Chen"
    },
    {
        "type": "file",
        "path": "syntopical_reading_agent/examples/sample_sources/ai_future_article2.txt",
        "author": "Professor Marcus Thompson"
    }
]

post = create_syntopical_post(
    sources=sources,
    topic="What is the future of AI?",
    provider="claude",
    output_format="blog"
)

print(post)
```

Run it:
```bash
python3 test_api.py
```

## Troubleshooting

### "API key required" error

Make sure you've set the environment variable:
```bash
export ANTHROPIC_API_KEY='your-actual-api-key'

# Verify it's set
echo $ANTHROPIC_API_KEY
```

Get your API key from: https://console.anthropic.com/

### "File not found" error

Make sure you're running from the repository root:
```bash
cd /home/user/Hello-World-
python3 -m syntopical_reading_agent.cli ...
```

### Import errors

Install dependencies:
```bash
pip install -r requirements.txt
```

### "anthropic package required" error

```bash
pip install anthropic
```

## Performance Notes

- **Time**: Full test takes 2-4 minutes (5 LLM calls)
- **Cost**: ~$0.10-0.30 per run with Claude Sonnet (depending on document length)
- **Tokens**: Expect ~20k-40k tokens total for the sample documents

## Testing Different Providers

### Test with OpenAI (GPT-4)

```bash
export OPENAI_API_KEY='your-openai-key'

python3 -m syntopical_reading_agent.cli \
  --config syntopical_reading_agent/examples/sample_sources/test_config.json \
  --topic "What does the future hold for artificial intelligence?" \
  --provider openai \
  --model gpt-4-turbo-preview
```

## Next Steps After Testing

1. ✓ Basic tests pass → Core package works
2. ✓ Full test passes → LLM integration works
3. → Try with your own documents
4. → Customize prompts in `syntopical_reading_agent/stages/`
5. → Adjust output format (blog, academic, essay)
6. → Share your results!

## Getting Help

If you encounter issues:
1. Check this guide
2. Review error messages carefully
3. Verify API key is set correctly
4. Ensure you're in the correct directory
5. Check that sample files exist

Happy testing! 🎉
