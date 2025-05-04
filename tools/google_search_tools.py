import time
import logging
from typing import List, Optional
from rich import print
from pydantic import BaseModel, Field

try:
    from googlesearch import search
except ImportError:
    raise ImportError("`googlesearch-python` not installed. Please install using `pip install googlesearch-python`")

from rich.logging import RichHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False)],
)
logger = logging.getLogger("GoogleSearchTools")

class GoogleSearchResult(BaseModel):
    url: str = Field(..., description="URL of the search result")
    title: Optional[str] = Field(None, description="Title of the search result")
    description: Optional[str] = Field(None, description="Description of the search result")
    
class GoogleSearchResults(BaseModel):
    result_count: int = Field(..., description="Number of search results")
    results: List[GoogleSearchResult] = Field(..., description="List of search results")

class GoogleSearchTool:
    """
    GoogleSearch is a Python library for searching Google easily.
    It uses requests and BeautifulSoup4 to scrape Google.

    Args:
        default_language (Optional[str]): Default language for search results, default is 'en' (English).
        timeout (Optional[int]): Timeout for the request, default is 10 seconds.
        sleep_interval (Optional[int]): Sleep interval between requests, default is 2 seconds.
    """

    def __init__(
        self,
        default_language: Optional[str] = 'en',
        timeout: Optional[int] = 10,
        sleep_interval: Optional[int] = 2,
    ):
        self.default_language = default_language
        self.timeout = timeout

    @classmethod
    def google_search(
            cls, 
            query: str, 
            max_results: int = 5, 
            start_number: int = 0, 
            language: str = "en", 
            advanced: bool = False,
            unique: bool = False,
            sleep_interval=2
        ) -> GoogleSearchResults:
        """
        Use this function to search Google for a specified query.

        Args:
            query (str): The search query.
            max_results (int): The maximum number of results to return. Default is 5.
            start_number (int): The starting index for the search results. Default is 0.
            language (str): The language for the search results. Default is 'en'.
            advanced (bool): Whether to use advanced search options. Default is False.
            unique (bool): Whether to return unique results. Default is False.

        Returns:
            GoogleSearchResults: A list of search results.
        """
        logger.info(f"Searching Google for: '{query}'")
        logger.info(f"Search parameters: max_results={max_results}, "
                   f"start_number={start_number}, language={language}, "
                   f"advanced={advanced}, unique={unique}, "
                   f"sleep_interval={sleep_interval}")
        
        start_time = time.time()

        # Perform Google search using the googlesearch-python package
        results = search(
            term=query, 
            num_results=max_results, 
            lang=language, 
            advanced=advanced,
            start_num=start_number,
            unique=unique,
            sleep_interval=sleep_interval
        )

        # Collect the search results
        search_results = []
        for result in results:
            if advanced:
                search_results.append(
                    GoogleSearchResult(
                        url=result.url,
                        title=result.title,
                        description=result.description,
                    )
                )
            else:
                search_results.append(
                    GoogleSearchResult(
                        url=result,
                        title=None,
                        description=None,
                    )
                )
             
        end_time = time.time()
        execution_time = end_time - start_time
        
        logger.info(f"Found {len(search_results)} results in {execution_time:.2f} seconds")

        google_search_results = GoogleSearchResults(
            result_count=len(search_results),
            results=search_results
        )
        
        return google_search_results
    
if __name__ == '__main__':
    query = 'Yeti Mug site:reddit.com'

    response = GoogleSearchTool.google_search(
        query=query,
        max_results=20,
        advanced=True
    )

    print(f"Found {response.result_count} results:")
    for result in response.results:
        print(result.url)
        print(result.title)
        print(result.description)
        print()    
