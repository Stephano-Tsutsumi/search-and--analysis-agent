#!/usr/bin/env python3
"""
Investment Agent - A tool to identify stocks likely to increase in value
based on current political and economic trends worldwide.

This script combines:
- Yahoo Finance data for stock analysis
- Google Search for trend analysis
- News API for current events
- Sentiment analysis for market sentiment
"""

import os
import json
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import requests
from dotenv import load_dotenv

# Import our custom tools
from tools.yahoo_finance_tools import YahooFinanceTool
from tools.google_search_tools import GoogleSearchTool

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

@dataclass
class StockRecommendation:
    """Data class for stock recommendations"""
    symbol: str
    company_name: str
    current_price: float
    confidence_score: float
    reasoning: str
    sector: str
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    news_sentiment: Optional[float] = None
    trend_alignment: Optional[str] = None

class NewsAPITool:
    """Tool for fetching news from NewsAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        self.enabled = bool(self.api_key)
        
        if not self.api_key:
            print("⚠️  News API key not found. News sentiment analysis will be disabled.")
            print("   To enable news analysis, add NEWS_API_KEY to your .env file")
    
    def get_trending_news(self, query: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get trending news for a specific query"""
        if not self.enabled:
            return []
            
        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'from': from_date,
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.api_key,
                'pageSize': 20
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('articles', [])
            
        except Exception as e:
            logger.error(f"Error fetching news for {query}: {e}")
            return []
    
    def get_market_sentiment(self, keywords: List[str]) -> Dict[str, Any]:
        """Analyze market sentiment based on news keywords"""
        if not self.enabled:
            return {}
            
        sentiment_data = {}
        
        for keyword in keywords:
            articles = self.get_trending_news(keyword, days_back=3)
            if articles:
                # Simple sentiment analysis based on article titles
                positive_words = ['surge', 'rise', 'gain', 'up', 'positive', 'growth', 'profit', 'success']
                negative_words = ['fall', 'drop', 'decline', 'down', 'negative', 'loss', 'crash', 'risk']
                
                positive_count = 0
                negative_count = 0
                
                for article in articles:
                    title = article.get('title', '').lower()
                    for word in positive_words:
                        if word in title:
                            positive_count += 1
                    for word in negative_words:
                        if word in title:
                            negative_count += 1
                
                total_articles = len(articles)
                if total_articles > 0:
                    sentiment_score = (positive_count - negative_count) / total_articles
                    sentiment_data[keyword] = {
                        'score': sentiment_score,
                        'articles_count': total_articles,
                        'positive_count': positive_count,
                        'negative_count': negative_count
                    }
        
        return sentiment_data
    


class InvestmentAgent:
    """Main investment agent class (headline-based version)"""
    
    @staticmethod
    def _is_valid_json(s: str) -> bool:
        try:
            json_object = json.loads(s)
            return True
        except Exception:
            return False
    
    def __init__(self):
        self.yahoo_tool = YahooFinanceTool()
        self.google_tool = GoogleSearchTool()
        self.news_tool = NewsAPITool()
        self.sector_keywords = {
            'Technology': ['AI', 'artificial intelligence', 'machine learning', 'cloud computing', 'cybersecurity'],
            'Healthcare': ['biotech', 'pharmaceuticals', 'medical devices', 'healthcare innovation'],
            'Energy': ['renewable energy', 'solar', 'wind', 'electric vehicles', 'battery technology'],
            'Finance': ['fintech', 'digital banking', 'blockchain', 'cryptocurrency'],
            'Consumer': ['e-commerce', 'digital transformation', 'retail innovation'],
            'Industrial': ['automation', 'robotics', 'manufacturing', 'supply chain'],
            'Real Estate': ['prop tech', 'real estate technology', 'smart cities'],
            'Materials': ['sustainable materials', 'recycling', 'green technology']
        }
        # S&P 500 stocks - Top companies by market cap and influence
        self.stock_universe = [
            # Technology (Mega Cap)
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
            'ORCL', 'CSCO', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'MU', 'INTU', 'ADP',
            'IBM', 'NOW', 'SNPS', 'KLAC', 'LRCX', 'ADI', 'CDNS', 'MCHP', 'MRVL', 'WDAY',
            
            # Healthcare
            'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'DHR', 'LLY', 'ABT', 'BMY', 'AMGN',
            'CVS', 'CI', 'ANTM', 'GILD', 'REGN', 'VRTX', 'BIIB', 'HUM', 'ISRG', 'BDX',
            'DVA', 'HCA', 'CNC', 'AET', 'WBA', 'CAH', 'MCK', 'ABC', 'ZTS', 'ALGN',
            
            # Financial Services
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'V', 'MA', 'AXP', 'C',
            'USB', 'PNC', 'TFC', 'COF', 'SCHW', 'CB', 'AIG', 'MET', 'PRU', 'ALL',
            'TRV', 'AFL', 'HIG', 'PFG', 'BEN', 'IVZ', 'TROW', 'AMP', 'NTRS', 'STT',
            
            # Consumer Discretionary
            'AMZN', 'TSLA', 'HD', 'MCD', 'DIS', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX',
            'BKNG', 'MAR', 'HLT', 'CMG', 'YUM', 'DPZ', 'SBUX', 'ULTA', 'ROST', 'TJX',
            'ORLY', 'AZO', 'KMX', 'LVS', 'WYNN', 'MGM', 'CCL', 'RCL', 'NCLH', 'UAL',
            
            # Consumer Staples
            'PG', 'KO', 'PEP', 'WMT', 'COST', 'PM', 'MO', 'MDLZ', 'GIS', 'K',
            'HSY', 'SJM', 'CAG', 'KMB', 'CL', 'EL', 'ULTA', 'DG', 'DLTR', 'FIVE',
            'KR', 'SFM', 'SPLS', 'BBY', 'GME', 'TSCO', 'ORLY', 'AZO', 'KMX', 'CVNA',
            
            # Energy
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'ENPH', 'SEDG', 'FSLR', 'NEE', 'DUK',
            'SO', 'D', 'NEE', 'AEP', 'XEL', 'DTE', 'ED', 'PEG', 'WEC', 'CMS',
            'CNP', 'AEE', 'EIX', 'PCG', 'SRE', 'VLO', 'MPC', 'PSX', 'VLO', 'MPC',
            
            # Industrials
            'CAT', 'DE', 'BA', 'GE', 'MMM', 'HON', 'UPS', 'FDX', 'LMT', 'RTX',
            'NOC', 'GD', 'LHX', 'TDG', 'TXT', 'EMR', 'ETN', 'ITW', 'DOV', 'XYL',
            'PH', 'AME', 'FTV', 'IEX', 'PNR', 'DCI', 'GWW', 'FAST', 'GPC', 'WSO',
            
            # Real Estate
            'AMT', 'PLD', 'CCI', 'EQIX', 'DLR', 'PSA', 'O', 'SPG', 'VICI', 'WELL',
            'EQR', 'AVB', 'MAA', 'ESS', 'UDR', 'CPT', 'AIV', 'BXP', 'VNO', 'SLG',
            'KIM', 'FRT', 'REG', 'MAC', 'PEAK', 'ARE', 'BMRN', 'HST', 'PK', 'AHT',
            
            # Materials
            'LIN', 'APD', 'FCX', 'NEM', 'BHP', 'RIO', 'VALE', 'AA', 'X', 'NUE',
            'SHW', 'ECL', 'APTV', 'ALB', 'LVS', 'WYNN', 'MGM', 'CCL', 'RCL', 'NCLH',
            'DOW', 'DD', 'EMN', 'LYB', 'BLL', 'IP', 'PKG', 'WRK', 'SEE', 'BMS',
            
            # Communication Services
            'GOOGL', 'META', 'NFLX', 'DIS', 'CMCSA', 'CHTR', 'VZ', 'T', 'TMUS', 'ATVI',
            'EA', 'TTWO', 'ZNGA', 'MTCH', 'SNAP', 'PINS', 'TWTR', 'LYV', 'FOX', 'NWSA',
            'PARA', 'WBD', 'LUMN', 'CTL', 'VZ', 'T', 'TMUS', 'S', 'LBRDK', 'LBRDA',
            
            # Utilities
            'NEE', 'DUK', 'SO', 'D', 'AEP', 'XEL', 'DTE', 'ED', 'PEG', 'WEC',
            'CMS', 'CNP', 'AEE', 'EIX', 'PCG', 'SRE', 'AEP', 'XEL', 'DTE', 'ED',
            'PEG', 'WEC', 'CMS', 'CNP', 'AEE', 'EIX', 'PCG', 'SRE', 'VLO', 'MPC'
        ]

    def get_headline_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze sentiment of recent news and Google headlines for a stock symbol."""
        # Get news headlines
        news_articles = self.news_tool.get_trending_news(symbol, days_back=5)
        news_titles = [a.get('title', '') for a in news_articles]
        # Get Google headlines
        google_results = self.google_tool.google_search(query=f"{symbol} stock news", max_results=5, advanced=True)
        google_titles = [r.title or '' for r in getattr(google_results, 'results', [])]
        # Combine all headlines
        all_titles = news_titles + google_titles
        # Simple sentiment: count positive/negative words
        positive_words = ['surge', 'rise', 'gain', 'up', 'positive', 'growth', 'profit', 'success', 'beat', 'record', 'strong']
        negative_words = ['fall', 'drop', 'decline', 'down', 'negative', 'loss', 'crash', 'risk', 'miss', 'weak', 'lawsuit']
        pos = sum(any(word in t.lower() for word in positive_words) for t in all_titles)
        neg = sum(any(word in t.lower() for word in negative_words) for t in all_titles)
        total = len(all_titles)
        sentiment_score = (pos - neg) / total if total > 0 else 0
        return {
            'symbol': symbol,
            'positive_headlines': pos,
            'negative_headlines': neg,
            'total_headlines': total,
            'sentiment_score': sentiment_score,
            'sample_headlines': all_titles[:3]
        }

    def generate_recommendations(self, top_n: int = 10) -> List[StockRecommendation]:
        """Generate stock recommendations based on headline sentiment only."""
        console.print(Panel.fit("🚀 Generating Headline-Based Investment Recommendations", style="bold green"))
        recommendations = []
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("Analyzing stocks...", total=len(self.stock_universe))
            for symbol in self.stock_universe:
                progress.update(task, description=f"Analyzing {symbol}...")
                try:
                    sentiment = self.get_headline_sentiment(symbol)
                    if sentiment['total_headlines'] == 0:
                        progress.advance(task)
                        continue
                    # Get company name from Yahoo (but don't fetch full fundamentals)
                    company_info = self.yahoo_tool.get_company_info(symbol)
                    if isinstance(company_info, str) and self._is_valid_json(company_info):
                        company_data = json.loads(company_info)
                        company_name = company_data.get('Name', symbol)
                        sector = company_data.get('Sector', 'Unknown')
                    else:
                        company_name = symbol
                        sector = 'Unknown'
                    rec = StockRecommendation(
                        symbol=symbol,
                        company_name=company_name,
                        current_price=0.0,  # Skip price for speed
                        confidence_score=sentiment['sentiment_score'],
                        reasoning=f"Headline sentiment: {sentiment['sentiment_score']:.2f}. Sample: {sentiment['sample_headlines']}",
                        sector=sector,
                        market_cap=None,
                        pe_ratio=None,
                        trend_alignment=None
                    )
                    recommendations.append(rec)
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                progress.advance(task)
        # Sort by sentiment score
        recommendations = [r for r in recommendations if r.confidence_score > 0]
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        return recommendations[:top_n]
    
    def display_recommendations(self, recommendations: List[StockRecommendation]):
        """Display recommendations in a formatted table"""
        console.print(Panel.fit("📊 Investment Recommendations", style="bold yellow"))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Symbol", style="cyan", no_wrap=True)
        table.add_column("Company", style="white")
        table.add_column("Sentiment Score", justify="right", style="green")
        table.add_column("Reasoning", style="white")
        
        for rec in recommendations:
            table.add_row(
                rec.symbol,
                rec.company_name[:30] + "..." if len(rec.company_name) > 30 else rec.company_name,
                f"{rec.confidence_score:.2f}",
                rec.reasoning[:50] + "..." if len(rec.reasoning) > 50 else rec.reasoning
            )
        
        console.print(table)
        
        # Display detailed reasoning for top recommendations
        console.print("\n" + "="*80)
        console.print(Panel.fit("💡 Detailed Analysis", style="bold blue"))
        
        for i, rec in enumerate(recommendations[:5], 1):
            console.print(f"\n[bold cyan]{i}. {rec.symbol} - {rec.company_name}[/bold cyan]")
            console.print(f"   [green]Sentiment Score: {rec.confidence_score:.2f}[/green]")
            console.print(f"   [white]Reasoning: {rec.reasoning}[/white]")
    
    def save_recommendations(self, recommendations: List[StockRecommendation], filename: str = None):
        """Save recommendations to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"investment_recommendations_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'recommendations': [
                {
                    'symbol': rec.symbol,
                    'company_name': rec.company_name,
                    'current_price': rec.current_price,
                    'confidence_score': rec.confidence_score,
                    'reasoning': rec.reasoning,
                    'sector': rec.sector,
                    'market_cap': rec.market_cap,
                    'pe_ratio': rec.pe_ratio,
                    'trend_alignment': rec.trend_alignment
                }
                for rec in recommendations
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        console.print(f"\n[green]Recommendations saved to {filename}[/green]")

def main():
    """Main function to run the investment agent"""
    console.print(Panel.fit("🤖 Investment Agent - Stock Recommendation Engine", style="bold blue"))
    console.print("Analyzing news and search headlines to identify promising investment opportunities...\n")
    try:
        agent = InvestmentAgent()
        recommendations = agent.generate_recommendations(top_n=10)
        agent.display_recommendations(recommendations)
        agent.save_recommendations(recommendations)
        console.print("\n[bold green]✅ Analysis complete![/bold green]")
        console.print("[yellow]Note: This is for informational purposes only. Always do your own research before investing.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main() 