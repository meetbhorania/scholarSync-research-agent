"""
Literature Scout Agent
Searches for academic papers using arxiv and ranks them with Gemini

Concepts from 5-Day AI Agents Course:
- Day 2: Custom Tools (arxiv search)
- Day 1: Agent architecture
- Day 4: Logging and observability
"""

import requests
import json
import os
from dotenv import load_dotenv


class LiteratureScoutAgent:
    """Agent that searches and ranks research papers"""

    def __init__(self, api_key):
        """Initialize the agent with Gemini API key"""
        self.api_key = api_key
        self.model = 'gemini-2.0-flash'

    def search_papers(self, query, max_results=5):
        """
        Search arxiv for papers

        This is a CUSTOM TOOL (Day 2: Tools & MCP)

        Args:
            query (str): Search query for papers
            max_results (int): Maximum number of papers to retrieve

        Returns:
            list: List of paper dictionaries
        """
        print(f"\n🔍 Searching arxiv for: '{query}'")

        try:
            import arxiv

            # Create arxiv client and search
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            papers = []
            for result in client.results(search):
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors][:3],
                    'summary': result.summary[:300] + "...",
                    'published': str(result.published.date()),
                    'url': result.pdf_url
                })

            print(f"✅ Found {len(papers)} papers\n")
            return papers

        except Exception as e:
            print(f"❌ Error searching papers: {e}")
            return []

    def rank_papers_with_gemini(self, papers, user_query):
        """
        Use Gemini LLM to rank papers by relevance

        Combines: Custom Tool + LLM Reasoning (Day 2 concept)

        Args:
            papers (list): List of paper dictionaries
            user_query (str): Original search query

        Returns:
            list: Ranked list of papers
        """
        if not papers:
            return []

        print("🤖 Asking Gemini to rank papers by relevance...\n")

        # Format papers for Gemini
        papers_text = ""
        for i, paper in enumerate(papers, 1):
            papers_text += f"\nPaper {i}:\n"
            papers_text += f"Title: {paper['title']}\n"
            papers_text += f"Summary: {paper['summary']}\n"

        # Create ranking prompt
        prompt = f"""You are a research assistant helping to rank academic papers.

User's Research Query: {user_query}

Papers to rank:
{papers_text}

Task: Rank these papers from most relevant to least relevant for the user's query.

Return ONLY a comma-separated list of paper numbers (most relevant first).
Example format: 3,1,4,2,5

Your ranking:"""

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
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                ranking_text = result['candidates'][0]['content']['parts'][0]['text'].strip()

                # Parse ranking from Gemini's response
                ranking = [int(x.strip()) - 1 for x in ranking_text.split(',')]
                ranked_papers = [papers[i] for i in ranking if 0 <= i < len(papers)]

                print(f"✅ Gemini ranked {len(ranked_papers)} papers\n")
                return ranked_papers

            else:
                print(f"⚠️ Gemini API error: {response.status_code}")
                return papers

        except Exception as e:
            print(f"⚠️ Ranking failed: {e}")
            return papers


def main():
    """Test the Literature Scout Agent"""

    # Load API key from .env file (SECURE!)
    load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')

    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        print("Please create a .env file with: GEMINI_API_KEY=your_key_here")
        return

    # Create agent instance
    print("🚀 Initializing Literature Scout Agent...\n")
    agent = LiteratureScoutAgent(API_KEY)

    # Test search
    query = "AI agents for scientific research"
    max_papers = 5
    papers = agent.search_papers(query, max_results=max_papers)

    if not papers:
        print("No papers found. Exiting.")
        return

    # Test ranking with Gemini
    ranked_papers = agent.rank_papers_with_gemini(papers, query)

    # Display ALL ranked results (structured output)
    print("=" * 70)
    print(f"📚 ALL {len(ranked_papers)} RANKED PAPERS (Most Relevant First):")
    print("=" * 70)

    for i, paper in enumerate(ranked_papers, 1):
        print(f"\nRank #{i}")
        print(f"Title:     {paper['title']}")
        print(f"Authors:   {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"URL:       {paper['url']}")
        print("-" * 70)

    print("\n✅ Literature Scout Agent test complete!")
    print(f"📊 Summary: Retrieved and ranked {len(ranked_papers)} papers")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()