from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class Settings():
    """All the Settings of the Crawler.
    
    Args:
        link_findall (str): regex expression to find links.
        link_relative_sub (List[str]): regex expression to substitute relative links.
        link_schema_relative_sub (List[str]): regex expression to substitute schema relative links.
        domain_findall (str): regex expression to find domain from a url.
        search_expressions (Dict[str, str]): dict of regex expression to look for in the html page.
        restrict_to_domain (bool): restrict future urls to the domain given at the start.
        depth (int): max depth to crawl.
        simulate_human (bool): use selenium webdriver to get html page.
        scroll_first_page (bool): selenium webdriver scroll down the first url given at the start.
        scroll_all_page (bool): selenium webdriver scroll down all the url found.
        headless (bool): don't show the page of selenium webdriver.
        get_timeout (int): time in seconds of a GET timeout.
        progress_bar (bool): use progress bar or simple prints.
        request_header (Dict[str, str]): header to add when doing a GET request with the module requests.
        valid_content_type (List[str]): content type of page content to allow the crawler to explore.
        xpath_restrict_link_crawl (str): xpath where children elements will be used to find links for depth 1.
    """    
    
    link_findall: str = r"href=\"((?:https?|\/\w|\/\/\w).+?)\""
    link_relative_sub: List[str] = field(default_factory=lambda: [r"(^\/\w.+?$)", r"https://{domain}\1"])
    link_schema_relative_sub: List[str] = field(default_factory=lambda: [r"(^(?:\/\/\w).*?$)", r"https:\1"])
    domain_findall: str = r"https?:\/\/(?:www\.)?([^\/\s\'\"]+)"
    search_expressions: Dict[str, str] = field(default_factory=lambda: {
        "emails": r"[\w\-\.]+?\@[\w\-\.]+?\.[\w]+",
        "phones": r"(?:tel\:)(\+?[\d\-\ ]{6,20})(?!\d)",
        "title": r"(?:<title>|<meta.*?property=\"og:title\".*?content=\")(.*?)(?:<\/title>|\".*?>)",
    })
    
    restrict_to_domain: bool = True
    depth: int = 1
    simulate_human: bool = False
    scroll_first_page: bool = True
    scroll_all_page: bool = False
    headless: bool = True
    get_timeout: int = 3
    progress_bar: bool = True
    
    request_header: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36}",
    })
    valid_content_type: List[str] = field(default_factory=lambda: [
        "text/html",
    ])
    xpath_restrict_link_crawl: str = "/html"