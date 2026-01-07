# Sample Output

This directory contains an example of what the Syntopical Reading Agent produces.

## Example Files

**example_final_post.md** - A sample final post showing what the agent generates when analyzing the three AI articles in `sample_sources/`.

This demonstrates:
- How the agent structures a syntopical reading post
- How it presents different perspectives fairly
- How it identifies agreements and disagreements
- How it synthesizes insights that emerge from comparing sources
- The quality and depth of analysis you can expect

## Note

This is a **manually created example** to show you what the output looks like. When you run the agent yourself with an API key, it will:

1. Create a `syntopical_output/` directory in the repository root
2. Generate two files:
   - `{topic}_{timestamp}_full.json` - Complete results from all 5 stages
   - `{topic}_{timestamp}_post.md` - The final synthesized post

The actual output will vary based on:
- The documents you analyze
- The topic/question you ask
- The LLM provider and model you use
- The output format you choose (blog, academic, essay)

## Try It Yourself

To generate real output:

```bash
export ANTHROPIC_API_KEY='your-key'

python3 -m syntopical_reading_agent.cli \
  --config syntopical_reading_agent/examples/sample_sources/test_config.json \
  --topic "What does the future hold for artificial intelligence?"
```

Then check `syntopical_output/` for your results!
