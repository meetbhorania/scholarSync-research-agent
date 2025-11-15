# ScholarSync AI - Research Assistant Agent

Multi-agent system for automating academic literature review.

## 🎯 Problem
Researchers spend 40+ hours per week manually searching, reading, and organizing academic papers.

## 💡 Solution
ScholarSync AI automates paper discovery, ranking, and analysis using AI agents.

## 🏗️ Architecture

### Agent 1: Literature Scout ✅
- Searches arxiv for relevant papers
- Uses Gemini to rank papers by relevance
- Status: **Complete**

### Agent 2: Paper Analyzer (Coming soon)
- Downloads and extracts text from PDFs
- Generates structured summaries
- Identifies key citations

### Agent 3: Hypothesis Generator (Coming soon)
- Analyzes research gaps
- Suggests new research directions
- Generates testable hypotheses

### Agent 4: Citation Manager (Coming soon)
- Organizes papers into collections
- Generates bibliographies
- Tracks reading progress

## 🛠️ Tech Stack
- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.0 Flash
- **Tools**: arxiv API, PyMuPDF (planned)
- **Language**: Python 3.10+

## 📦 Setup
```bash
# Clone repository
git clone https://github.com/meetbhorania/scholarSync-research-agent.git
cd scholarSync-research-agent

# Install dependencies
pip install google-genai arxiv python-dotenv requests

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Test Agent 1
python agents/literature_scout.py
```

## 🎓 Course Concepts Applied
Built using concepts from Google's 5-Day AI Agents Intensive Course:
- **Day 1**: Multi-agent architecture
- **Day 2**: Custom tools (arxiv search)
- **Day 4**: Logging and observability

## 📊 Current Status
- [x] Agent 1: Literature Scout
- [ ] Agent 2: Paper Analyzer
- [ ] Agent 3: Hypothesis Generator
- [ ] Agent 4: Citation Manager
- [ ] Integration & Memory
- [ ] Deployment

## 🏆 Competition
This project is submitted for the **Agents for Good** track of the Kaggle AI Agents Intensive Capstone Project.

---

*Last updated: 15th November 2025*