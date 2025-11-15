"""
Paper Analyzer Agent
Downloads PDFs and generates structured summaries using Gemini

Concepts from 5-Day AI Agents Course:
- Day 2: Custom Tools (PDF extraction)
- Day 1: Sequential agent workflow
- Day 3: Context management
"""

import requests
import os
from dotenv import load_dotenv
import PyPDF2
import io


class PaperAnalyzerAgent:
    """Agent that downloads and analyzes research papers"""

    def __init__(self, api_key):
        """Initialize the agent with Gemini API key"""
        self.api_key = api_key
        self.model = 'gemini-2.0-flash'

    def download_pdf(self, pdf_url):
        """
        Download PDF from URL

        Custom Tool (Day 2 concept)

        Args:
            pdf_url (str): URL to PDF file

        Returns:
            bytes: PDF content or None if failed
        """
        print(f"\n📥 Downloading PDF from: {pdf_url}")

        try:
            response = requests.get(pdf_url, timeout=30)
            if response.status_code == 200:
                print("✅ PDF downloaded successfully")
                return response.content
            else:
                print(f"❌ Download failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None

    def extract_text_from_pdf(self, pdf_content, max_pages=5):
        """
        Extract text from PDF bytes

        Custom Tool (Day 2 concept)

        Args:
            pdf_content (bytes): PDF file content
            max_pages (int): Maximum pages to extract (to avoid token limits)

        Returns:
            str: Extracted text
        """
        print(f"📄 Extracting text from PDF (first {max_pages} pages)...")

        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            total_pages = len(pdf_reader.pages)
            pages_to_read = min(max_pages, total_pages)

            text = ""
            for page_num in range(pages_to_read):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            print(f"✅ Extracted {len(text)} characters from {pages_to_read} pages")
            return text

        except Exception as e:
            print(f"❌ Text extraction error: {e}")
            return ""

    def generate_summary(self, paper_text, paper_title):
        """
        Use Gemini to generate structured summary

        Combines: Tool + LLM Reasoning (Day 2 concept)

        Args:
            paper_text (str): Full text from paper
            paper_title (str): Paper title for context

        Returns:
            dict: Structured summary
        """
        print("\n🤖 Generating structured summary with Gemini...")

        # Truncate text if too long (Gemini has token limits)
        max_chars = 15000
        if len(paper_text) > max_chars:
            paper_text = paper_text[:max_chars] + "..."
            print(f"⚠️  Text truncated to {max_chars} characters")

        # Create analysis prompt
        prompt = f"""You are analyzing an academic research paper.

Paper Title: {paper_title}

Paper Content:
{paper_text}

Generate a structured summary with these sections:

1. **Main Research Question**: What problem does this paper address?
2. **Methodology**: What approach/methods did they use?
3. **Key Findings**: What are the main results/discoveries?
4. **Limitations**: What are the limitations mentioned?
5. **Future Work**: What future research directions are suggested?

Format your response as:
RESEARCH QUESTION: [answer]
METHODOLOGY: [answer]
KEY FINDINGS: [answer]
LIMITATIONS: [answer]
FUTURE WORK: [answer]

Keep each section concise (2-3 sentences max).
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
                summary_text = result['candidates'][0]['content']['parts'][0]['text']

                # Parse structured output
                summary = self._parse_summary(summary_text)
                print("✅ Summary generated successfully\n")
                return summary

            else:
                print(f"❌ Gemini API error: {response.status_code}")
                return {}

        except Exception as e:
            print(f"❌ Summary generation error: {e}")
            return {}

    def _parse_summary(self, summary_text):
        """Parse Gemini's response into structured format"""
        summary = {
            'research_question': '',
            'methodology': '',
            'key_findings': '',
            'limitations': '',
            'future_work': ''
        }

        lines = summary_text.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith('RESEARCH QUESTION:'):
                current_section = 'research_question'
                summary[current_section] = line.replace('RESEARCH QUESTION:', '').strip()
            elif line.startswith('METHODOLOGY:'):
                current_section = 'methodology'
                summary[current_section] = line.replace('METHODOLOGY:', '').strip()
            elif line.startswith('KEY FINDINGS:'):
                current_section = 'key_findings'
                summary[current_section] = line.replace('KEY FINDINGS:', '').strip()
            elif line.startswith('LIMITATIONS:'):
                current_section = 'limitations'
                summary[current_section] = line.replace('LIMITATIONS:', '').strip()
            elif line.startswith('FUTURE WORK:'):
                current_section = 'future_work'
                summary[current_section] = line.replace('FUTURE WORK:', '').strip()
            elif current_section and line:
                summary[current_section] += ' ' + line

        return summary

    def analyze_paper(self, paper_url, paper_title):
        """
        Complete paper analysis pipeline

        Sequential workflow (Day 1 concept)

        Args:
            paper_url (str): URL to paper PDF
            paper_title (str): Paper title

        Returns:
            dict: Complete analysis
        """
        print("=" * 70)
        print(f"📊 ANALYZING PAPER: {paper_title}")
        print("=" * 70)

        # Step 1: Download PDF
        pdf_content = self.download_pdf(paper_url)
        if not pdf_content:
            return None

        # Step 2: Extract text
        paper_text = self.extract_text_from_pdf(pdf_content)
        if not paper_text:
            return None

        # Step 3: Generate summary
        summary = self.generate_summary(paper_text, paper_title)

        return {
            'title': paper_title,
            'url': paper_url,
            'summary': summary,
            'text_length': len(paper_text)
        }


def main():
    """Test the Paper Analyzer Agent"""

    # Load API key
    load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')

    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return

    # Create agent
    print("🚀 Initializing Paper Analyzer Agent...\n")
    agent = PaperAnalyzerAgent(API_KEY)

    # Test with a sample paper
    test_paper = {
        'title': 'Attention Is All You Need',
        'url': 'https://arxiv.org/pdf/1706.03762.pdf'
    }

    # Analyze paper
    analysis = agent.analyze_paper(test_paper['url'], test_paper['title'])

    if analysis:
        # Display structured results
        print("\n" + "=" * 70)
        print("📋 STRUCTURED PAPER ANALYSIS")
        print("=" * 70)
        print(f"\nTitle: {analysis['title']}")
        print(f"URL: {analysis['url']}")
        print(f"Text Extracted: {analysis['text_length']:,} characters")
        print("\n" + "-" * 70)

        summary = analysis['summary']

        print("\n🔍 RESEARCH QUESTION:")
        print(summary.get('research_question', 'N/A'))

        print("\n⚙️  METHODOLOGY:")
        print(summary.get('methodology', 'N/A'))

        print("\n💡 KEY FINDINGS:")
        print(summary.get('key_findings', 'N/A'))

        print("\n⚠️  LIMITATIONS:")
        print(summary.get('limitations', 'N/A'))

        print("\n🚀 FUTURE WORK:")
        print(summary.get('future_work', 'N/A'))

        print("\n" + "=" * 70)
        print("✅ Paper Analyzer Agent test complete!")


if __name__ == "__main__":
    main()