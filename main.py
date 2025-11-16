"""
ScholarSync AI - Main Integration Script
Combines multiple agents to automate research workflow

Concepts from 5-Day AI Agents Course:
- Day 1: Multi-agent orchestration
- Day 2: Tool integration
- Day 3: Session management
"""

import os
from dotenv import load_dotenv
from agents.literature_scout import LiteratureScoutAgent
from agents.paper_analyzer import PaperAnalyzerAgent
from agents.research_gap_analyzer import ResearchGapAnalyzerAgent


class ScholarSyncOrchestrator:
    """
    Main orchestrator that coordinates multiple agents

    Sequential Multi-Agent System (Day 1 concept)
    """

    def __init__(self, api_key):
        """Initialize all agents"""
        self.api_key = api_key

        # Initialize agents
        print("🔧 Initializing agents...")
        self.scout = LiteratureScoutAgent(api_key)
        self.analyzer = PaperAnalyzerAgent(api_key)
        self.gap_analyzer = ResearchGapAnalyzerAgent(api_key)
        print("✅ All 3 agents initialized\n")

    def research_workflow(self, query, max_papers=3, analyze_top=1):
        """
        Complete research workflow

        Args:
            query (str): Research query
            max_papers (int): Number of papers to find
            analyze_top (int): Number of top papers to analyze in detail

        Returns:
            dict: Complete research results
        """
        print("=" * 70)
        print(f"🔬 STARTING RESEARCH WORKFLOW")
        print(f"Query: {query}")
        print("=" * 70)

        # STEP 1: Find papers (Agent 1)
        print("\n📍 STEP 1: Finding relevant papers...")
        papers = self.scout.search_papers(query, max_results=max_papers)

        if not papers:
            print("❌ No papers found. Exiting.")
            return None

        # STEP 2: Rank papers (Agent 1)
        print("\n📍 STEP 2: Ranking papers by relevance...")
        ranked_papers = self.scout.rank_papers_with_gemini(papers, query)

        # STEP 3: Analyze top papers (Agent 2)
        print(f"\n📍 STEP 3: Analyzing top {analyze_top} paper(s) in detail...")

        analyzed_papers = []
        for i, paper in enumerate(ranked_papers[:analyze_top], 1):
            print(f"\n--- Analyzing Paper {i}/{analyze_top} ---")
            analysis = self.analyzer.analyze_paper(paper['url'], paper['title'])
            if analysis:
                analyzed_papers.append(analysis)

        # STEP 4: Analyze research gaps (Agent 3)
        if len(analyzed_papers) >= 2:
            print(f"\n📍 STEP 4: Identifying research gaps across papers...")
            gap_analysis = self.gap_analyzer.analyze_gaps(analyzed_papers, query)
        else:
            print(f"\n⚠️  STEP 4 SKIPPED: Need at least 2 analyzed papers for gap analysis")
            gap_analysis = None

        # Compile results
        results = {
            'query': query,
            'total_papers_found': len(papers),
            'ranked_papers': ranked_papers,
            'detailed_analyses': analyzed_papers,
            'gap_analysis': gap_analysis
        }

        return results

    def display_results(self, results):
        """Display results in structured format"""
        if not results:
            return

        print("\n" + "=" * 70)
        print("📊 RESEARCH WORKFLOW COMPLETE")
        print("=" * 70)

        print(f"\n🔍 Query: {results['query']}")
        print(f"📚 Papers Found: {results['total_papers_found']}")
        print(f"📄 Papers Analyzed: {len(results['detailed_analyses'])}")

        # Show all ranked papers
        print("\n" + "-" * 70)
        print("📑 ALL RANKED PAPERS:")
        print("-" * 70)
        for i, paper in enumerate(results['ranked_papers'], 1):
            print(f"\nRank #{i}")
            print(f"  Title: {paper['title']}")
            print(f"  Authors: {', '.join(paper['authors'])}")
            print(f"  URL: {paper['url']}")

        # Show detailed analyses
        if results['detailed_analyses']:
            print("\n" + "=" * 70)
            print("🔬 DETAILED ANALYSIS OF TOP PAPER(S):")
            print("=" * 70)

            for i, analysis in enumerate(results['detailed_analyses'], 1):
                print(f"\n{'=' * 70}")
                print(f"PAPER #{i}: {analysis['title']}")
                print('=' * 70)

                summary = analysis['summary']

                print("\n🔍 Research Question:")
                print(f"  {summary.get('research_question', 'N/A')}")

                print("\n⚙️  Methodology:")
                print(f"  {summary.get('methodology', 'N/A')}")

                print("\n💡 Key Findings:")
                print(f"  {summary.get('key_findings', 'N/A')}")

                print("\n⚠️  Limitations:")
                print(f"  {summary.get('limitations', 'N/A')}")

                print("\n🚀 Future Work:")
                print(f"  {summary.get('future_work', 'N/A')}")

        # Show gap analysis
        if results.get('gap_analysis'):
            print("\n" + "=" * 70)
            print("🔬 RESEARCH GAP ANALYSIS")
            print("=" * 70)

            gap = results['gap_analysis']

            print("\n🔗 Common Themes Across Papers:")
            print(f"  {gap.get('common_themes', 'N/A')}")

            print("\n🔀 Divergent Approaches:")
            print(f"  {gap.get('divergent_approaches', 'N/A')}")

            print("\n❓ Research Gaps Identified:")
            print(f"  {gap.get('research_gaps', 'N/A')}")

            print("\n💡 Proposed Research Directions:")
            for direction in gap.get('proposed_directions', []):
                print(f"  {direction}")

            print("\n🌟 Novel Contribution Opportunity:")
            print(f"  {gap.get('novel_contribution', 'N/A')}")

        print("\n" + "=" * 70)
        print("✅ END OF REPORT")
        print("=" * 70)


def main():
    """Main entry point with interactive mode and error handling"""

    try:
        # Load API key
        load_dotenv()
        API_KEY = os.getenv('GEMINI_API_KEY')

        if not API_KEY:
            print("❌ Error: GEMINI_API_KEY not found in .env file")
            return

        print("=" * 70)
        print("🚀 ScholarSync AI - Research Assistant")
        print("=" * 70)
        print("\nAutomates literature review for researchers")
        print("Searches, ranks, and analyzes academic papers in minutes.")
        print("\n💡 Tip: Press Ctrl+C at any time to exit safely\n")

        # Create orchestrator
        orchestrator = ScholarSyncOrchestrator(API_KEY)

        # Interactive mode
        print("-" * 70)
        research_query = input("🔍 Enter your research topic: ").strip()

        if not research_query:
            print("❌ No query entered. Exiting gracefully.")
            return

        try:
            num_papers = int(input("📚 How many papers to find? (3-10, default=5): ") or "5")
            num_analyze = int(input("📄 How many to analyze in detail? (1-3, default=2): ") or "2")
        except ValueError:
            print("⚠️  Invalid input. Using defaults: 5 papers, analyze 2")
            num_papers = 5
            num_analyze = 2

        print("\n⏳ Starting research workflow...")
        print("(This may take 2-4 minutes depending on number of papers)\n")

        # Run complete workflow
        results = orchestrator.research_workflow(
            query=research_query,
            max_papers=num_papers,
            analyze_top=num_analyze
        )

        if not results:
            print("\n❌ Workflow failed. Please try again.")
            return

        # Display structured results
        orchestrator.display_results(results)

        # Save option
        print("\n" + "-" * 70)
        save = input("💾 Save results to file? (y/n, default=n): ").strip().lower()
        if save == 'y':
            save_results_to_file(results)
            print("\n✅ Session complete! Exiting.")
        else:
            print("\n✅ Session complete! Results not saved. Exiting.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user (Ctrl+C)")
        print("✅ Exiting gracefully. Goodbye!")
        return

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your .env file and internet connection.")
        return


def save_results_to_file(results):
    """Save results to a markdown file"""
    import datetime

    if not results:
        return

    try:
        # Create filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_report_{timestamp}.md"

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Research Report: {results['query']}\n\n")
            f.write(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Papers Found:** {results['total_papers_found']}\n")
            f.write(f"**Papers Analyzed:** {len(results['detailed_analyses'])}\n\n")

            f.write("---\n\n")
            f.write("## Ranked Papers\n\n")
            for i, paper in enumerate(results['ranked_papers'], 1):
                f.write(f"### {i}. {paper['title']}\n")
                f.write(f"- **Authors:** {', '.join(paper['authors'])}\n")
                f.write(f"- **Published:** {paper['published']}\n")
                f.write(f"- **URL:** {paper['url']}\n\n")

            f.write("---\n\n")
            f.write("## Detailed Analysis\n\n")
            for i, analysis in enumerate(results['detailed_analyses'], 1):
                f.write(f"### Paper {i}: {analysis['title']}\n\n")
                summary = analysis['summary']
                f.write(f"**Research Question:**\n{summary.get('research_question', 'N/A')}\n\n")
                f.write(f"**Methodology:**\n{summary.get('methodology', 'N/A')}\n\n")
                f.write(f"**Key Findings:**\n{summary.get('key_findings', 'N/A')}\n\n")
                f.write(f"**Limitations:**\n{summary.get('limitations', 'N/A')}\n\n")
                f.write(f"**Future Work:**\n{summary.get('future_work', 'N/A')}\n\n")
                f.write("---\n\n")

            # Add gap analysis to file
            if results.get('gap_analysis'):
                f.write("## Research Gap Analysis\n\n")
                gap = results['gap_analysis']
                f.write(f"**Common Themes:**\n{gap.get('common_themes', 'N/A')}\n\n")
                f.write(f"**Divergent Approaches:**\n{gap.get('divergent_approaches', 'N/A')}\n\n")
                f.write(f"**Research Gaps:**\n{gap.get('research_gaps', 'N/A')}\n\n")
                f.write(f"**Proposed Research Directions:**\n")
                for direction in gap.get('proposed_directions', []):
                    f.write(f"- {direction}\n")
                f.write(f"\n**Novel Contribution:**\n{gap.get('novel_contribution', 'N/A')}\n\n")

        print(f"✅ Results saved to: {filename}")

    except Exception as e:
        print(f"❌ Error saving file: {e}")


if __name__ == "__main__":
    main()