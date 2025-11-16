"""
Research Gap Analyzer Agent
Compares multiple analyzed papers to identify research gaps

Concepts from 5-Day AI Agents Course:
- Day 1: Multi-agent collaboration
- Day 2: Advanced LLM reasoning
- Day 3: Context management across multiple papers
"""

import requests
import json
import os
from dotenv import load_dotenv


class ResearchGapAnalyzerAgent:
    """Agent that identifies research gaps across multiple papers"""

    def __init__(self, api_key):
        """Initialize the agent with Gemini API key"""
        self.api_key = api_key
        self.model = 'gemini-2.0-flash'

    def analyze_gaps(self, analyzed_papers, research_query):
        """
        Compare multiple papers and identify research gaps

        Sequential reasoning (Day 1 concept)

        Args:
            analyzed_papers (list): List of paper analysis results from Agent 2
            research_query (str): Original research query

        Returns:
            dict: Gap analysis with research directions
        """
        if not analyzed_papers or len(analyzed_papers) < 2:
            print("⚠️  Need at least 2 analyzed papers to find gaps")
            return None

        print("\n" + "=" * 70)
        print(f"🔬 ANALYZING RESEARCH GAPS")
        print(f"Comparing {len(analyzed_papers)} papers...")
        print("=" * 70)

        # Format papers for comparison
        papers_comparison = self._format_papers_for_comparison(analyzed_papers)

        # Generate gap analysis
        gap_analysis = self._generate_gap_analysis(papers_comparison, research_query)

        return gap_analysis

    def _format_papers_for_comparison(self, analyzed_papers):
        """Format analyzed papers into comparison structure"""
        comparison_text = ""

        for i, paper in enumerate(analyzed_papers, 1):
            summary = paper.get('summary', {})
            comparison_text += f"\n{'=' * 60}\n"
            comparison_text += f"PAPER {i}: {paper['title']}\n"
            comparison_text += f"{'=' * 60}\n"
            comparison_text += f"\nResearch Question:\n{summary.get('research_question', 'N/A')}\n"
            comparison_text += f"\nMethodology:\n{summary.get('methodology', 'N/A')}\n"
            comparison_text += f"\nKey Findings:\n{summary.get('key_findings', 'N/A')}\n"
            comparison_text += f"\nLimitations:\n{summary.get('limitations', 'N/A')}\n"
            comparison_text += f"\nFuture Work:\n{summary.get('future_work', 'N/A')}\n"

        return comparison_text

    def _generate_gap_analysis(self, papers_comparison, research_query):
        """Use Gemini to identify research gaps"""

        print("\n🤖 Using Gemini to identify research gaps...\n")

        # Create comprehensive analysis prompt
        prompt = f"""You are a research expert analyzing academic papers to identify research gaps.

Original Research Query: {research_query}

Papers Being Compared:
{papers_comparison}

Your Task: Perform a comprehensive gap analysis across these papers.

Provide a structured analysis with these sections:

1. COMMON THEMES: What do all these papers agree on or explore together?

2. DIVERGENT APPROACHES: Where do the papers differ in methodology or focus?

3. RESEARCH GAPS: What has NOT been explored yet? What's missing?
   - Unexplored methodologies
   - Untested domains/applications
   - Missing comparisons
   - Unaddressed limitations

4. PROPOSED RESEARCH DIRECTIONS: Based on the gaps, what are 3-5 specific research questions that could be pursued?

5. NOVEL CONTRIBUTION OPPORTUNITIES: What would be a novel contribution to this field?

Format your response as:
COMMON THEMES: [answer]

DIVERGENT APPROACHES: [answer]

RESEARCH GAPS: [answer]

PROPOSED RESEARCH DIRECTIONS:
1. [question 1]
2. [question 2]
3. [question 3]

NOVEL CONTRIBUTION: [answer]

Keep each section clear and specific.
"""

        # Call Gemini API
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}'

        data = {
            'contents': [{
                'parts': [{'text': prompt}]
            }]
        }

        try:
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                analysis_text = result['candidates'][0]['content']['parts'][0]['text']

                # Parse structured response
                gap_analysis = self._parse_gap_analysis(analysis_text)
                print("✅ Gap analysis complete!\n")
                return gap_analysis

            else:
                print(f"❌ Gemini API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Gap analysis failed: {e}")
            return None

    def _parse_gap_analysis(self, analysis_text):
        """Parse Gemini's gap analysis into structured format"""

        analysis = {
            'common_themes': '',
            'divergent_approaches': '',
            'research_gaps': '',
            'proposed_directions': [],
            'novel_contribution': ''
        }

        lines = analysis_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith('COMMON THEMES:'):
                current_section = 'common_themes'
                analysis[current_section] = line.replace('COMMON THEMES:', '').strip()
            elif line.startswith('DIVERGENT APPROACHES:'):
                current_section = 'divergent_approaches'
                analysis[current_section] = line.replace('DIVERGENT APPROACHES:', '').strip()
            elif line.startswith('RESEARCH GAPS:'):
                current_section = 'research_gaps'
                analysis[current_section] = line.replace('RESEARCH GAPS:', '').strip()
            elif line.startswith('PROPOSED RESEARCH DIRECTIONS:'):
                current_section = 'proposed_directions'
            elif line.startswith('NOVEL CONTRIBUTION:'):
                current_section = 'novel_contribution'
                analysis[current_section] = line.replace('NOVEL CONTRIBUTION:', '').strip()
            elif current_section == 'proposed_directions' and (
                    line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith(
                    '4.') or line.startswith('5.')):
                analysis[current_section].append(line)
            elif current_section and line and current_section != 'proposed_directions':
                analysis[current_section] += ' ' + line

        return analysis


def main():
    """Test the Research Gap Analyzer Agent"""

    # Load API key
    load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')

    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return

    print("🚀 Testing Research Gap Analyzer Agent...\n")

    # Create agent
    agent = ResearchGapAnalyzerAgent(API_KEY)

    # Mock data (simulating Agent 2 output for 2 papers)
    mock_analyzed_papers = [
        {
            'title': 'Attention Is All You Need',
            'summary': {
                'research_question': 'Can we build sequence models without recurrence or convolution?',
                'methodology': 'Transformer architecture using self-attention mechanisms',
                'key_findings': 'Achieved state-of-the-art on translation tasks, faster training',
                'limitations': 'Requires large amounts of training data',
                'future_work': 'Apply to other tasks beyond translation'
            }
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'summary': {
                'research_question': 'Can we pre-train transformers bidirectionally for better understanding?',
                'methodology': 'Masked language modeling and next sentence prediction',
                'key_findings': 'BERT outperforms previous models on 11 NLP tasks',
                'limitations': 'Computational cost is very high for pre-training',
                'future_work': 'Explore multilingual and smaller models'
            }
        }
    ]

    # Test gap analysis
    query = "transformer architectures for NLP"
    gap_analysis = agent.analyze_gaps(mock_analyzed_papers, query)

    if gap_analysis:
        # Display results
        print("\n" + "=" * 70)
        print("📊 RESEARCH GAP ANALYSIS RESULTS")
        print("=" * 70)

        print("\n🔗 COMMON THEMES:")
        print(gap_analysis.get('common_themes', 'N/A'))

        print("\n🔀 DIVERGENT APPROACHES:")
        print(gap_analysis.get('divergent_approaches', 'N/A'))

        print("\n❓ RESEARCH GAPS:")
        print(gap_analysis.get('research_gaps', 'N/A'))

        print("\n💡 PROPOSED RESEARCH DIRECTIONS:")
        for direction in gap_analysis.get('proposed_directions', []):
            print(f"  {direction}")

        print("\n🌟 NOVEL CONTRIBUTION OPPORTUNITY:")
        print(gap_analysis.get('novel_contribution', 'N/A'))

        print("\n" + "=" * 70)
        print("✅ Research Gap Analyzer test complete!")


if __name__ == "__main__":
    main()