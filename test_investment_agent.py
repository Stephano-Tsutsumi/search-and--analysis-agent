#!/usr/bin/env python3
"""
Test script for the Investment Agent components
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_yahoo_finance():
    """Test Yahoo Finance tools"""
    print("Testing Yahoo Finance tools...")
    try:
        from tools.yahoo_finance_tools import YahooFinanceTool
        
        # Test current price
        price = YahooFinanceTool.get_current_price("AAPL")
        print(f"✓ AAPL current price: {price}")
        
        # Test company info
        info = YahooFinanceTool.get_company_info("AAPL")
        print(f"✓ AAPL company info retrieved (length: {len(info)})")
        
        print("✅ Yahoo Finance tools working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Yahoo Finance tools error: {e}")
        return False

def test_google_search():
    """Test Google Search tools"""
    print("\nTesting Google Search tools...")
    try:
        from tools.google_search_tools import GoogleSearchTool
        
        # Test search
        results = GoogleSearchTool.google_search("AI technology trends", max_results=3)
        print(f"✓ Google search returned {results.result_count} results")
        
        print("✅ Google Search tools working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Google Search tools error: {e}")
        return False

def test_news_api():
    """Test News API (if key is available)"""
    print("\nTesting News API...")
    api_key = os.getenv('NEWS_API_KEY')
    
    if not api_key:
        print("⚠️  NEWS_API_KEY not found in .env file")
        print("   To test News API, add your key to .env file:")
        print("   NEWS_API_KEY=your_api_key_here")
        return False
    
    try:
        from investment_agent import NewsAPITool
        
        news_tool = NewsAPITool(api_key)
        articles = news_tool.get_trending_news("AI technology", days_back=1)
        print(f"✓ News API returned {len(articles)} articles")
        
        print("✅ News API working correctly")
        return True
        
    except Exception as e:
        print(f"❌ News API error: {e}")
        return False

def test_investment_agent():
    """Test Investment Agent components"""
    print("\nTesting Investment Agent components...")
    try:
        from investment_agent import InvestmentAgent
        
        agent = InvestmentAgent()
        print("✓ Investment Agent initialized successfully")
        
        # Test stock universe
        print(f"✓ Stock universe contains {len(agent.stock_universe)} stocks")
        
        # Test sector keywords
        print(f"✓ Sector keywords defined for {len(agent.sector_keywords)} sectors")
        
        print("✅ Investment Agent components working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Investment Agent error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Investment Agent Components")
    print("=" * 50)
    
    tests = [
        test_yahoo_finance,
        test_google_search,
        test_news_api,
        test_investment_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Investment Agent is ready to use.")
        print("\nTo run the full analysis:")
        print("python investment_agent.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        
        if passed < total - 1:  # If News API is the only failure
            print("\nNote: The agent will work without News API, but with reduced functionality.")

if __name__ == "__main__":
    main() 