#!/usr/bin/env python3
"""
Simple Python test for Syntopical Reading Agent
Tests the agent without requiring API keys by using mock/demo mode
"""

import sys
from pathlib import Path

# Add the package to path
sys.path.insert(0, str(Path(__file__).parent))

from syntopical_reading_agent.document_loader import DocumentLoader

def test_document_loading():
    """Test 1: Verify document loading works"""
    print("\n" + "="*60)
    print("TEST 1: Document Loading")
    print("="*60)

    try:
        # Load the sample documents
        doc1 = DocumentLoader.load_from_file(
            "syntopical_reading_agent/examples/sample_sources/ai_future_article1.txt",
            author="Dr. Sarah Chen"
        )
        doc2 = DocumentLoader.load_from_file(
            "syntopical_reading_agent/examples/sample_sources/ai_future_article2.txt",
            author="Professor Marcus Thompson"
        )
        doc3 = DocumentLoader.load_from_file(
            "syntopical_reading_agent/examples/sample_sources/ai_future_article3.txt",
            author="Dr. Amara Okafor"
        )

        print(f"✓ Loaded document 1: {doc1.title} by {doc1.author}")
        print(f"  Content length: {len(doc1.content)} characters")
        print(f"✓ Loaded document 2: {doc2.title} by {doc2.author}")
        print(f"  Content length: {len(doc2.content)} characters")
        print(f"✓ Loaded document 3: {doc3.title} by {doc3.author}")
        print(f"  Content length: {len(doc3.content)} characters")

        print("\n✓ Document loading test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Document loading test FAILED: {e}")
        return False

def test_document_loader_multiple():
    """Test 2: Verify batch document loading"""
    print("\n" + "="*60)
    print("TEST 2: Batch Document Loading")
    print("="*60)

    try:
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
            },
            {
                "type": "file",
                "path": "syntopical_reading_agent/examples/sample_sources/ai_future_article3.txt",
                "author": "Dr. Amara Okafor"
            }
        ]

        documents = DocumentLoader.load_multiple(sources)

        print(f"✓ Loaded {len(documents)} documents using batch loader")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc.title} by {doc.author}")

        print("\n✓ Batch loading test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Batch loading test FAILED: {e}")
        return False

def test_imports():
    """Test 3: Verify all imports work"""
    print("\n" + "="*60)
    print("TEST 3: Package Imports")
    print("="*60)

    try:
        from syntopical_reading_agent import SyntopicalReadingAgent, DocumentLoader
        print("✓ Main imports work")

        from syntopical_reading_agent.llm_providers import LLMProvider, get_provider
        print("✓ LLM provider imports work")

        from syntopical_reading_agent.stages import (
            SurveyStage, TerminologyStage, QuestionsStage,
            IssuesStage, SynthesisStage
        )
        print("✓ Stage imports work")

        print("\n✓ Import test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Import test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_loading():
    """Test 4: Verify text loading works"""
    print("\n" + "="*60)
    print("TEST 4: Direct Text Loading")
    print("="*60)

    try:
        text = "This is a test document about AI and its future implications."
        doc = DocumentLoader.load_from_text(
            text,
            title="Test Document",
            author="Test Author"
        )

        print(f"✓ Created document from text: {doc.title} by {doc.author}")
        print(f"  Content: {doc.content[:50]}...")

        print("\n✓ Text loading test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Text loading test FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SYNTOPICAL READING AGENT - TEST SUITE")
    print("="*60)
    print("\nRunning basic tests (no API key required)...")

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Document Loading", test_document_loading()))
    results.append(("Batch Loading", test_document_loader_multiple()))
    results.append(("Text Loading", test_text_loading()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)

    if passed == total:
        print("\n🎉 All basic tests passed!")
        print("\nTo test with actual LLM processing:")
        print("  1. Set your API key: export ANTHROPIC_API_KEY='your-key'")
        print("  2. Run: ./test_agent.sh")
        print("  or: python3 -m syntopical_reading_agent.cli \\")
        print("        --config syntopical_reading_agent/examples/sample_sources/test_config.json \\")
        print("        --topic 'What does the future hold for artificial intelligence?'")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
