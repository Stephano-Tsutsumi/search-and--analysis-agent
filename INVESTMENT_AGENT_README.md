# Investment Agent

An intelligent tool that combines Yahoo Finance data, Google Search trends, and news sentiment analysis to identify stocks likely to increase in value based on current political and economic trends worldwide.

## Features

- **Global Trend Analysis**: Analyzes current political and economic trends using Google Search
- **Stock Fundamental Analysis**: Uses Yahoo Finance to analyze company fundamentals
- **News Sentiment Analysis**: Incorporates news sentiment to gauge market mood
- **Confidence Scoring**: Calculates confidence scores for each stock recommendation
- **Rich Output**: Beautiful formatted tables and detailed analysis reports
- **Data Export**: Saves recommendations to JSON files for further analysis

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root with your API keys:

```bash
# News API Key (required)
# Get your free API key at: https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here
```

### 3. Get News API Key

1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key
4. Add it to your `.env` file

## Usage

### Basic Usage

```bash
python investment_agent.py
```

### What the Agent Does

1. **Analyzes Global Trends**: Searches for current political and economic trends
2. **Evaluates Stock Universe**: Analyzes 80+ stocks across 8 sectors
3. **Calculates Confidence Scores**: Based on fundamentals, trends, and sentiment
4. **Generates Recommendations**: Top 15 stocks with highest confidence scores
5. **Saves Results**: Exports recommendations to JSON file

### Output

The agent provides:

- **Formatted Table**: Shows symbol, company, price, sector, confidence score, P/E ratio, and trend alignment
- **Detailed Analysis**: Reasoning for each top recommendation
- **JSON Export**: Complete data saved to timestamped file

## Stock Universe

The agent analyzes stocks across these sectors:

- **Technology**: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META, NFLX, ADBE, CRM
- **Healthcare**: JNJ, PFE, UNH, ABBV, TMO, DHR, LLY, ABT, BMY, AMGN
- **Energy**: XOM, CVX, COP, EOG, SLB, ENPH, SEDG, FSLR, NEE
- **Finance**: JPM, BAC, WFC, GS, MS, BLK, V, MA, AXP, C
- **Consumer**: PG, KO, PEP, WMT, HD, MCD, DIS, NKE, SBUX, TGT
- **Industrial**: CAT, DE, BA, GE, MMM, HON, UPS, FDX, LMT, RTX
- **Real Estate**: AMT, PLD, CCI, EQIX, DLR, PSA, O, SPG, VICI, WELL
- **Materials**: LIN, APD, FCX, NEM, BHP, RIO, VALE, AA, X, NUE

## Confidence Score Calculation

The agent calculates confidence scores based on:

1. **Fundamental Analysis** (40%):

   - P/E ratio evaluation
   - Market cap consideration
   - Price relative to 52-week range

2. **Trend Alignment** (30%):

   - Sector alignment with current trends
   - News sentiment analysis
   - Market momentum indicators

3. **Market Position** (30%):
   - Company size and stability
   - Sector growth potential
   - Competitive positioning

## Customization

### Modify Stock Universe

Edit the `stock_universe` list in `investment_agent.py` to add or remove stocks.

### Adjust Sector Keywords

Modify the `sector_keywords` dictionary to change how sectors are mapped to trends.

### Change Confidence Calculation

Update the `calculate_confidence_score` method to adjust scoring weights.

## Example Output

```
🤖 Investment Agent - Stock Recommendation Engine
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📊 Investment Recommendations                                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────┬──────────────────────────────┬─────────┬──────────────────┬──────────┬──────────┬─────────────────────────┐
│ Symbol │ Company                      │ Price   │ Sector           │ Confidence│ P/E Ratio│ Trend Alignment         │
├────────┼──────────────────────────────┼─────────┼──────────────────┼──────────┼──────────┼─────────────────────────┤
│ NVDA   │ NVIDIA Corporation           │ $485.09 │ Technology       │ 0.85     │ 75.2     │ Aligned with AI trends   │
│ TSLA   │ Tesla, Inc.                  │ $248.42 │ Consumer Discret.│ 0.82     │ 62.1     │ Aligned with EV trends   │
│ AAPL   │ Apple Inc.                   │ $175.43 │ Technology       │ 0.78     │ 28.5     │ Aligned with tech trends │
└────────┴──────────────────────────────┴─────────┴──────────────────┴──────────┴──────────┴─────────────────────────┘
```

## Disclaimer

⚠️ **Important**: This tool is for informational and educational purposes only. It does not constitute financial advice. Always:

- Do your own research before making investment decisions
- Consider consulting with a financial advisor
- Understand that past performance doesn't guarantee future results
- Be aware that all investments carry risk

## Troubleshooting

### Common Issues

1. **News API Key Error**: Make sure your NEWS_API_KEY is set in the .env file
2. **Rate Limiting**: The tool includes delays to respect API limits
3. **Network Issues**: Check your internet connection if data fetching fails

### Error Messages

- `News API key not found`: Add your NEWS_API_KEY to .env file
- `Error fetching data`: Usually temporary, try running again
- `No recommendations generated`: Check if all APIs are working

## Contributing

Feel free to contribute by:

- Adding more stocks to the universe
- Improving the confidence score algorithm
- Adding new data sources
- Enhancing the trend analysis

## License

This project is for educational purposes. Use at your own risk.
