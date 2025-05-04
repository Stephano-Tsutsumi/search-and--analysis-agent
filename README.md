# Search Agent

This repository contains tools for web search and financial data retrieval.

## Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/search-agent.git
cd search-agent
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

```bash
cp .env.example .env
```

Then edit the `.env` file and add your API keys.

## Available Tools

- Google Search Tools
- Yahoo Finance Tools
- Playwright Tools (for web automation)

## Usage

Example usage of the investment research workflow:

```bash
python investment_research_workflow.py
```

## Requirements

- Python 3.8+
- OpenAI API key
- Other dependencies listed in requirements.txt
