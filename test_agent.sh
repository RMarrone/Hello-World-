#!/bin/bash
# Quick Test Script for Syntopical Reading Agent

echo "=============================================="
echo "Syntopical Reading Agent - Quick Test"
echo "=============================================="
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY not set!"
    echo ""
    echo "Please set your API key first:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "Get your API key from: https://console.anthropic.com/"
    echo ""
    exit 1
fi

echo "✓ API key found"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import anthropic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencies not installed. Installing now..."
    pip install -r requirements.txt
    echo ""
fi

echo "✓ Dependencies ready"
echo ""

# Run the test
echo "Running syntopical reading on sample AI articles..."
echo "This will take 2-3 minutes as it processes through all 5 stages."
echo ""
echo "================================================"
echo ""

python3 -m syntopical_reading_agent.cli \
  --config syntopical_reading_agent/examples/sample_sources/test_config.json \
  --topic "What does the future hold for artificial intelligence?"

echo ""
echo "================================================"
echo "✓ Test complete!"
echo ""
echo "Check the syntopical_output/ directory for saved results:"
echo "  - Full JSON with all stages"
echo "  - Final markdown post"
echo "================================================"
