#!/usr/bin/env python3
"""
Command-line interface for the Syntopical Reading Agent
"""

import argparse
import json
import sys
from pathlib import Path

from .syntopical_agent import SyntopicalReadingAgent, create_syntopical_post
from .document_loader import DocumentLoader


def main():
    parser = argparse.ArgumentParser(
        description="Syntopical Reading Agent - Create synthesized posts from multiple sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using a config file
  python -m syntopical_reading_agent.cli --config sources.json --topic "What is AI?"

  # Using command-line arguments
  python -m syntopical_reading_agent.cli \\
    --topic "The nature of consciousness" \\
    --file article1.txt --author "John Doe" \\
    --file article2.txt --author "Jane Smith" \\
    --url https://example.com/article3

  # Specify output format and LLM provider
  python -m syntopical_reading_agent.cli \\
    --config sources.json \\
    --topic "Climate change solutions" \\
    --format academic \\
    --provider openai \\
    --model gpt-4
        """
    )

    # Required arguments
    parser.add_argument(
        "--topic",
        required=True,
        help="The research topic or question to explore"
    )

    # Source specification
    source_group = parser.add_argument_group("Source specification")
    source_group.add_argument(
        "--config",
        help="JSON config file with sources (see examples/config.json)"
    )
    source_group.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Add a file source (can be used multiple times)"
    )
    source_group.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="Add a URL source (can be used multiple times)"
    )
    source_group.add_argument(
        "--author",
        action="append",
        dest="authors",
        help="Author for the previous --file or --url (optional)"
    )
    source_group.add_argument(
        "--title",
        action="append",
        dest="titles",
        help="Title for the previous --file or --url (optional)"
    )

    # LLM configuration
    llm_group = parser.add_argument_group("LLM configuration")
    llm_group.add_argument(
        "--provider",
        default="claude",
        choices=["claude", "openai"],
        help="LLM provider to use (default: claude)"
    )
    llm_group.add_argument(
        "--model",
        help="Specific model to use (e.g., claude-sonnet-4-20250514, gpt-4)"
    )
    llm_group.add_argument(
        "--api-key",
        help="API key for the LLM provider (can also use env vars)"
    )

    # Output configuration
    output_group = parser.add_argument_group("Output configuration")
    output_group.add_argument(
        "--format",
        default="blog",
        choices=["blog", "academic", "essay"],
        help="Output format (default: blog)"
    )
    output_group.add_argument(
        "--output",
        help="Output file path (default: auto-generated in syntopical_output/)"
    )
    output_group.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save intermediate results"
    )

    args = parser.parse_args()

    # Build sources list
    sources = []

    # Load from config file if provided
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)

        with open(config_path, 'r') as f:
            config = json.load(f)
            sources.extend(config.get("sources", []))

    # Add command-line sources
    if args.files:
        for i, file_path in enumerate(args.files):
            source = {"type": "file", "path": file_path}
            if args.authors and i < len(args.authors):
                source["author"] = args.authors[i]
            if args.titles and i < len(args.titles):
                source["title"] = args.titles[i]
            sources.append(source)

    if args.urls:
        offset = len(args.files) if args.files else 0
        for i, url in enumerate(args.urls):
            source = {"type": "url", "url": url}
            idx = offset + i
            if args.authors and idx < len(args.authors):
                source["author"] = args.authors[idx]
            if args.titles and idx < len(args.titles):
                source["title"] = args.titles[idx]
            sources.append(source)

    if not sources:
        print("Error: No sources specified. Use --config, --file, or --url", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Prepare LLM provider kwargs
    provider_kwargs = {}
    if args.model:
        provider_kwargs["model"] = args.model
    if args.api_key:
        provider_kwargs["api_key"] = args.api_key

    try:
        # Load documents
        print(f"Loading {len(sources)} source(s)...")
        documents = DocumentLoader.load_multiple(sources)
        print(f"Loaded {len(documents)} document(s)")

        # Create and run agent
        agent = SyntopicalReadingAgent(
            provider_name=args.provider,
            **provider_kwargs
        )

        results = agent.read(
            documents,
            args.topic,
            output_format=args.format,
            save_intermediates=not args.no_save
        )

        # Print final post
        print("\n" + "="*60)
        print("FINAL POST")
        print("="*60 + "\n")
        print(results['final_post'])

        # Save to custom output if specified
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(results['final_post'])
            print(f"\n✓ Post saved to: {output_path}")

        print("\n" + "="*60)
        print("✓ Syntopical reading complete!")
        print("="*60)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
