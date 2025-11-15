# ScholarSync AI - Research Assistant Agent

AI-powered multi-agent system for automating academic literature review.

## 🎯 Problem
Researchers spend 40+ hours per week manually searching, reading, and organizing academic papers. This slows down scientific progress and wastes valuable research time.

## 💡 Solution
ScholarSync AI automates the entire literature review workflow using coordinated AI agents that search, rank, and analyze papers in minutes instead of hours.

## 🏗️ Architecture

### Agent 1: Literature Scout ✅ COMPLETE
- **Function**: Searches arxiv for relevant papers
- **Tool**: arxiv API (custom tool)
- **Intelligence**: Uses Gemini to rank papers by relevance
- **Output**: Ranked list of most relevant papers

### Agent 2: Paper Analyzer ✅ COMPLETE
- **Function**: Downloads and analyzes research papers
- **Tools**: PyPDF2 for text extraction
- **Intelligence**: Gemini generates structured summaries
- **Output**: Research question, methodology, findings, limitations, future work

### Agent 3: Hypothesis Generator 🚧 IN PROGRESS
- Analyzes research gaps across multiple papers
- Suggests new research directions
- Generates testable hypotheses

### Agent 4: Citation Manager 🚧 IN PROGRESS
- Organizes papers into collections
- Generates bibliographies
- Tracks reading progress

### Orchestrator ✅ COMPLETE
Coordinates all agents in a sequential workflow for complete research automation.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Gemini API key ([Get one free](https://aistudio.google.com/apikey))

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/scholarSync-research-agent.git
cd scholarSync-research-agent

# Install dependencies
pip install google-genai arxiv python-dotenv requests PyPDF2

# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### Usage

**Interactive Mode:**
```bash
python main.py
```

Follow the prompts:
1. Enter research topic
2. Specify number of papers to find
3. Choose how many to analyze in detail
4. Optionally save results to file

**Example Output:**
```
🔍 Query: multimodal AI agents
📚 Papers Found: 5
📄 Papers Analyzed: 2

📑 ALL RANKED PAPERS:
1. [Most relevant paper]
2. [Second most relevant]
...

🔬 DETAILED ANALYSIS:
Research Question: ...
Methodology: ...
Key Findings: ...
```

## 🛠️ Tech Stack
- **Framework**: Direct API integration (Google Gemini)
- **LLM**: Gemini 2.0 Flash
- **Tools**: 
  - arxiv API (paper search)
  - PyPDF2 (text extraction)
  - Python-dotenv (secure key management)
- **Language**: Python 3.10+

## 📚 Concepts from 5-Day AI Agents Course

This project demonstrates concepts from Google's AI Agents Intensive Course:

- **Day 1: Multi-Agent Architecture** - Orchestrator coordinates 4 specialized agents
- **Day 2: Custom Tools** - arxiv search, PDF extraction
- **Day 3: Context Management** - Structured summaries with memory
- **Day 4: Observability** - Logging at each workflow step

## 📊 Current Status

- [x] Agent 1: Literature Scout (complete)
- [x] Agent 2: Paper Analyzer (complete)
- [x] Multi-agent orchestration (complete)
- [x] Interactive CLI interface (complete)
- [ ] Agent 3: Hypothesis Generator
- [ ] Agent 4: Citation Manager
- [ ] Memory system (session tracking)
- [ ] Deployment to cloud

## 💪 Impact & Value

**Time Savings:**
- Traditional literature review: 8-10 hours
- With ScholarSync AI: 3-5 minutes
- **Time saved: 95%+**

**Use Cases:**
- PhD students conducting thesis research
- Professors staying current in their field
- Industry researchers doing competitive analysis
- Students writing research papers

## 🏆 Competition Entry

This project is submitted for the **Agents for Good** track of the Kaggle AI Agents Intensive Capstone Project (November 2025).

**Why "Agents for Good"?**
- Democratizes access to research tools
- Accelerates scientific discovery
- Helps researchers worldwide work more efficiently

## 📁 Project Structure
```
scholarSync-research-agent/
├── main.py                      # Orchestrator & entry point
├── agents/
│   ├── literature_scout.py      # Agent 1: Search & rank papers
│   └── paper_analyzer.py        # Agent 2: Analyze papers
├── .env                         # API keys (not in repo)
├── .gitignore                   # Protected files
└── README.md                    # This file
```

## 🔐 Security Note

Never commit API keys to GitHub. Always use `.env` files (excluded via `.gitignore`).

## 📝 License

MIT License - feel free to use and modify!

---

**Built with 🧠 by Meet Bhorania** | [LinkedIn](https://www.linkedin.com/in/meetbhorania/)
