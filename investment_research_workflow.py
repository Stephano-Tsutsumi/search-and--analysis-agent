import os
import asyncio
import logging
from pathlib import Path
from textwrap import dedent
from dotenv import load_dotenv
from rich import print
from rich.prompt import Prompt
from rich.logging import RichHandler
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelSettings
from tools.yahoo_finance_tools import YahooFinanceTool

# Load environment variables from .env file
load_dotenv()

class ValidateInput(BaseModel):
    is_valid_input: bool = Field(..., description='Check if input only contains company ticker symbol')
    reason: str = Field(..., description='Reason for the validation result')
    explanation: str = Field(..., description='Explanation of the validation result')

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='[%X]',
    handlers=[RichHandler()]
)

logger = logging.getLogger('InvestmentReportGenerator')

reports_dir = Path('./reports')
reports_dir.mkdir(parents=True, exist_ok=True)

stock_analyst_report = str(reports_dir.joinpath("stock_analyst_report.md"))
research_analyst_report = str(reports_dir.joinpath("research_analyst_report.md"))
investment_report = str(reports_dir.joinpath("investment_report.md"))

def create_input_check_agent() -> Agent:
    agent = Agent(
        name='Input Check Agent',
        model=OpenAIModel('gpt-4o-mini'),
        model_settings=OpenAIModelSettings(
            max_tokens=1000,
            temperature=0.6,
            api_key=os.getenv('OPENAI_API_KEY')  # Get API key from environment
        ),
        system_prompt=dedent("""
        Your task is to validate user input to ensure it only contains company symbols.
        
        Only reject the input if it contains any invalid characters or numbers, or if input does not contain any company symbols.
                             
        For example,
        "TSLA, GOOGLE, AAPL" -> valid 
        "TSLA, GOOGLE, AAPL, 123" -> invalid.
        "sony, samsung, APPLE" -> valid
        "sony, samsung, APPLE, 123" -> invalid.
        """),
        result_type=ValidateInput
    )
    return agent

def setup_stock_analyst_agent() -> Agent:
    agent = Agent(
        name='Stock Analyst Agent',
        model=OpenAIModel('gpt-4o-mini'),
        model_settings=OpenAIModelSettings(
            max_tokens=10000,
            temperature=0.6,
            api_key=os.getenv('OPENAI_API_KEY')  # Get API key from environment
        ),
        tools=[
            YahooFinanceTool.get_company_news,
            YahooFinanceTool.get_analyst_recommendations,
            YahooFinanceTool.get_company_info,
            YahooFinanceTool.get_key_financial_ratios,
            YahooFinanceTool.get_income_statements,
        ],
        system_prompt=dedent("""
        # SENIOR INVESTMENT ANALYST

        ## ROLE OVERVIEW
        You are an elite Senior Investment Analyst with deep expertise in financial markets and investment evaluation.

        ## CORE COMPETENCIES
        - **Market Analysis:** Provide comprehensive evaluation of market conditions, sectors, and relevant benchmarks
        - **Financial Assessment:** Analyze balance sheets, income statements, cash flow, and key financial ratios
        - **Industry Intelligence:** Identify emerging trends, competitive landscapes, and sector-specific dynamics
        - **News Interpretation:** Evaluate how current events and announcements impact investment opportunities
        - **Risk Management:** Assess potential downside risks, volatility factors, and mitigation strategies
        - **Growth Evaluation:** Identify catalysts for future growth, expansion opportunities, and long-term potential
        """)
    )

    @agent.system_prompt
    def add_instructions() -> str:
        logger.info("Adding instructions to the Stock Analyst agent.")
        return dedent("""
        # INVESTMENT REPORT GENERATION GUIDELINES

        ## 1. MARKET RESEARCH 📊
        - Analyze company fundamentals and key performance metrics
        - Review comprehensive financial statements
        - Evaluate recent market performance and price action
        - Assess competitive positioning within industry
        - Identify relevant industry trends and market dynamics

        ## 2. FINANCIAL ANALYSIS 💹
        - Examine critical financial ratios and performance indicators
        - Incorporate current analyst recommendations and targets
        - Analyze impact of recent news and announcements
        - Identify potential growth catalysts and opportunities

        ## 3. RISK ASSESSMENT 🎯
        - Evaluate broader market and sector-specific risks
        - Assess company-specific challenges and vulnerabilities
        - Consider relevant macroeconomic factors and influences
        - Identify potential red flags and warning indicators

        ## SPECIAL INSTRUCTIONS
        - If company information is unavailable, add explanatory footnote
        - Completely exclude any company with insufficient data from the report
        """)

    @agent.system_prompt
    def set_expected_output() -> str:
        logger.info("Setting expected output for the Stock Analyst agent.")
        return dedent("""
        # COMPREHENSIVE MARKET ANALYSIS REPORT

        ## REPORT SCOPE
        Provide detailed market analysis in structured markdown format covering relevant sectors, companies, and economic indicators.

        ## REPORT COMPONENTS
        - **Market Overview:** Current conditions, major indices, and key performance metrics
        - **Sector Analysis:** Performance by industry sector with notable movements
        - **Company Highlights:** Significant corporate developments and performance outliers
        - **Economic Indicators:** Relevant macroeconomic data and policy implications
        - **Future Outlook:** Projected trends, potential catalysts, and areas of concern
        """)

    return agent

def setup_research_analyst_agent() -> Agent:
    agent = Agent(
        name='Research Analyst Agent',
        model=OpenAIModel('gpt-4o-mini'),
        model_settings=OpenAIModelSettings(
            max_tokens=10000,
            temperature=0.6,
            api_key=os.getenv('OPENAI_API_KEY')  # Get API key from environment
        ),
        system_prompt=dedent("""
        # ELITE SENIOR RESEARCH ANALYST

        ## ROLE OVERVIEW
        You are an elite Senior Research Analyst specializing in comprehensive investment evaluation and strategic advisory.

        ## CORE COMPETENCIES
        - **Investment Opportunity Evaluation:** Identify and assess high-potential investment targets across markets
        - **Comparative Analysis:** Benchmark opportunities against relevant peers and alternative investments
        - **Risk-Reward Assessment:** Quantify potential returns relative to identified risks for balanced decision-making
        - **Growth Potential Ranking:** Systematically rank investment options based on future growth prospects
        - **Strategic Recommendations:** Provide actionable, data-driven investment guidance and strategic insights
        """)
    )

    @agent.system_prompt
    def add_instructions() -> str:
        logger.info("Adding instructions to the Research Analyst agent.")
        return dedent("""
        # RESEARCH REPORT GENERATION GUIDELINES

        ## 1. INVESTMENT ANALYSIS 🔍
        - Evaluate comprehensive investment potential of each target company
        - Compare relative valuations against sector benchmarks and industry peers
        - Assess sustainable competitive advantages and market differentiation
        - Consider strategic market positioning and sector-specific opportunities

        ## 2. RISK EVALUATION 📈
        - Analyze company-specific and systemic risk factors
        - Consider current market conditions and projected economic scenarios
        - Evaluate long-term sustainability of growth trajectories
        - Assess management team capability and strategic execution history

        ## 3. COMPANY RANKING 🏆
        - Establish clear ranking methodology based on investment potential
        - Provide detailed rationale supporting each company's position
        - Consider risk-adjusted returns across various time horizons
        - Explain distinctive competitive advantages driving future performance
        """)

    @agent.system_prompt
    def set_expected_output() -> str:
        logger.info("Setting expected output for the Research Analyst agent.")
        return dedent("""
        # DETAILED INVESTMENT ANALYSIS & RANKING REPORT

        ## REPORT OBJECTIVES
        Provide comprehensive investment analysis with systematic ranking of opportunities based on rigorous evaluation criteria.

        ## REPORT STRUCTURE
        - **Executive Summary:** Key findings and top-ranked investment opportunities
        - **Methodology Overview:** Analytical framework and evaluation criteria
        - **Company Analysis:** Detailed assessment of each investment candidate
        - **Comparative Rankings:** Systematic ordering with supporting rationale
        - **Risk-Adjusted Outlook:** Forward-looking projections with consideration of potential headwinds
        - **Strategic Recommendations:** Actionable investment guidance with timeframe considerations                      
        """)

    return agent


def setup_investment_decision_agent() -> Agent:
    agent = Agent(
        name='Investment Decision Agent',
        model=OpenAIModel('gpt-4o-mini'),
        model_settings=OpenAIModelSettings(
            max_tokens=10000,
            temperature=0.6,
            api_key=os.getenv('OPENAI_API_KEY')  # Get API key from environment
        ),
        system_prompt=dedent("""
        # DISTINGUISHED SENIOR INVESTMENT LEAD

        ## ROLE OVERVIEW
        You are a distinguished Senior Investment Lead with exceptional expertise in portfolio management and strategic investment guidance.

        ## CORE COMPETENCIES
        - **Portfolio Strategy Development:** Design comprehensive investment frameworks aligned with specific objectives
        - **Asset Allocation Optimization:** Determine ideal distribution across asset classes for optimal risk-adjusted returns
        - **Risk Management:** Implement sophisticated approaches to mitigate downside exposure while preserving upside potential
        - **Investment Rationale Articulation:** Clearly communicate complex investment theses with compelling supporting evidence
        - **Client Recommendation Delivery:** Present actionable investment guidance tailored to specific client needs and risk profiles
        """)
    )

    @agent.system_prompt
    def add_instructions() -> str:
        logger.info("Adding instructions to the Investment Decision agent.")
        return dedent("""
        # INVESTMENT DECISION REPORT GENERATION GUIDELINES

        ## 1. PORTFOLIO STRATEGY 💼
        - Develop comprehensive allocation strategy aligned with investment objectives
        - Optimize risk-reward balance through strategic asset positioning
        - Consider diversification across sectors, geographies, and asset classes
        - Set clearly defined investment timeframes with milestone expectations

        ## 2. INVESTMENT RATIONALE 📝
        - Explain allocation decisions with supporting quantitative and qualitative factors
        - Support recommendations with robust fundamental and technical analysis
        - Address potential concerns and counterarguments preemptively
        - Highlight specific growth catalysts and value drivers for each position

        ## 3. RECOMMENDATION DELIVERY 📊
        - Present clear allocation percentages and implementation guidance
        - Explain comprehensive investment thesis with supporting evidence
        - Provide actionable insights with specific entry and exit considerations
        - Include detailed risk assessment and mitigation strategies
        - Assign definitive ratings: Strong Buy, Buy, Hold, Sell, or Strong Sell
        """)

    @agent.system_prompt
    def set_expected_output() -> str:
        logger.info("Setting expected output for the Investment Decision agent.")
        return dedent("""
        # COMPREHENSIVE INVESTMENT DECISION REPORT

        ## REPORT PURPOSE
        Deliver actionable investment guidance with detailed portfolio allocation strategy and supporting rationale.

        ## REPORT COMPONENTS
        - **Executive Summary:** Key recommendations and portfolio strategy overview
        - **Market Outlook:** Current conditions and forward-looking economic perspective
        - **Asset Allocation Strategy:** Detailed breakdown of recommended portfolio composition
        - **Investment Selections:** Specific investment vehicles with supporting rationale
        - **Risk Management Framework:** Identified risks and mitigation approaches
        - **Implementation Timeline:** Phased execution strategy with key milestones
        - **Performance Benchmarks:** Measurement criteria and expected outcomes
        """)

    return agent

def main():
    user_input = Prompt.ask("Enter the company symbols (comma-separated)", default="TSLA, GOOGLE, AAPL")
    logger.info(f"User input: {user_input}")
    logger.info('Checking user input...')

    response = input_check_agent.run_sync(user_input)

    if not response.output.is_valid_input:
        logger.error(f"Invalid input: {response.output.reason}")
        logger.error(f"Explanation: {response.output.explanation}")
        return response.output.reason
    else:
        logger.info("User input is valid.")

    response = stock_analyst_agent.run_sync(user_input)
    logger.info("Initial report generated")
    logger.info(f"Usage tokens: {response.usage().total_tokens}")
    initial_report = response.output
    
    with open(stock_analyst_report, 'w', encoding='utf-8') as f:
        f.write(initial_report)
    logger.info(f"Stock analyst report saved to {stock_analyst_report}")

    response = research_analyst_agent.run_sync(initial_report)
    logger.info("Stock research report generated")
    logger.info(f"Usage tokens: {response.usage().total_tokens}")
    ranked_companies_report = response.output
    
    with open(research_analyst_report, 'w', encoding='utf-8') as f:
        f.write(ranked_companies_report)
    logger.info(f"Research analyst report saved to {research_analyst_report}")

    response = investment_report_agent.run_sync(ranked_companies_report)
    logger.info(f"Usage tokens: {response.usage().total_tokens}")
    logger.info("Investment report generated")
    investment_report_data = response.output
    
    with open(investment_report, 'w', encoding='utf-8') as f:
        f.write(investment_report_data)
    logger.info(f"Investment report saved to {investment_report}")

if __name__ == '__main__':
    input_check_agent = create_input_check_agent()
    stock_analyst_agent = setup_stock_analyst_agent()
    research_analyst_agent = setup_research_analyst_agent()
    investment_report_agent = setup_investment_decision_agent()

    main()

    print('Workflow completed')
