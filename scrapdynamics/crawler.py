from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
import pandas as pd
import requests
from time import sleep
from json import dump
from typing import List
from lxml import etree

from .settings import Settings
from .progressbar import ProgressBar
from .url import UrlManager


class Crawler(UrlManager):
    """A web crawler

    Args:
        base_url (str): url where crawling begins
        settings (Settings, optional): settings of the crawler. Defaults to False.
    """
    
    def __init__(self, base_url: str, settings: Settings = False):
        
        super(Crawler, self).__init__()
        
        # change the settings that UrlManager created
        if settings: self.s = settings
        
        self.base_url = base_url
        self.base_domain = self._get_domain_from_url(base_url)
        
        # open and configure selenium webdriver
        if self.s.simulate_human:
            driver_options = Options()
            driver_options.headless = self.s.headless
            self.driver = Firefox(options=driver_options)
            self.driver.set_page_load_timeout(self.s.get_timeout)
            
    def start(self):
        """Start the crawler
        """
        
        # create progress_bar
        if self.s.progress_bar:
            self.pb = ProgressBar()
            self.pb.update_task(self.s.depth, 0)
        
        page_text = self._get_page_selenium(self.base_url, True) if self.s.simulate_human else self._get_page_request(self.base_url)
        
        # add base url to UrlManager and collect info
        self._add_url(self.base_url, self._children_element_xpath(page_text))
        
        for d in range(self.s.depth):
            
            # get all links found in precedent pages
            all_links = self._get_all_links()
            
            if self.s.progress_bar: self.pb.make_advance(True, False)
            else: print(f"Depth = {d+1}/{self.s.depth} | Nb Links = {len(all_links)}")
            
            self._run_layer(all_links)
            
        if self.s.progress_bar: self.pb.close()
    
    def show(self) -> pd.DataFrame:
        """Show results in a pd.Dataframe

        Returns:
            pd.DataFrame: results with info of the page in a column
        """
        
        return pd.DataFrame(self._url_to_dict())
              
    def to_json(self, path: str):
        """Save results to JSON format

        Args:
            path (str): path of the results file
        """
        
        with open(path, "w") as f: dump(self._url_to_dict(), f)
            
    def to_csv(self, path: str):
        """Save results to CSV format

        Args:
            path (str): path of the results file
        """
        
        df = pd.DataFrame(self._url_to_dict())
        df.to_csv(path, index=False)
        
    def to_excel(self, path: str):
        """Save results to CSV format

        Args:
            path (str): path of the results file
        """
        
        df = pd.DataFrame(self._url_to_dict())
        df.to_excel(path)

    def _run_layer(self, layer_sub_links: List[str]):
        """Run all links in the current depth and add them to the UrlManager

        Args:
            layer_sub_links (List[str]): all the links found in the precedent depth
        """
        
        length_layer_sub_links = len(layer_sub_links)
        
        # update and reset link progress bar for a new depth
        if self.s.progress_bar:
            self.pb.update_task(0, length_layer_sub_links)
            self.pb.make_reset(False, True)
            
        for i, url in enumerate(layer_sub_links):
            
            if self.s.progress_bar: self.pb.make_advance(False, True)
            else: print(f"    {i+1}/{length_layer_sub_links}", end="\r")
            
            # skip current url if base domain not in current url
            if self.s.restrict_to_domain and self.base_domain not in url: continue
            
            if not self._verify_headers(url): continue
            self._add_url(url, self._get_page_selenium(url) if self.s.simulate_human else self._get_page_request(url))
    
    def _verify_headers(self, url: str) -> bool:
        """Verify if link return a 200 status code and is a valid content type or if it's a 301 or 302 recall function with the new location.

        Args:
            url (str): url/link to verify

        Returns:
            bool: return True if status code 200 and is a valid content type
        """               
        
        try: head = requests.head(url)
        except: return False
        else:
            # return True if content type is in the valid content types
            if head.status_code == 200: return any([vct in head.headers["Content-Type"] for vct in self.s.valid_content_type])
            # if status code is 301 or 302 recall verify_headers with new location 
            elif head.status_code == 301 or head.status_code == 302: return self._verify_headers(self._clean_link(url, head.headers["Location"]))
            else: return False
    
    def _get_page_request(self, url: str) -> str:
        """Make a GET request and get the html page of a specific url using requests module

        Args:
            url (str): url/link

        Returns:
            str: html page or None 
        """
        
        try: return requests.get(url, headers=self.s.request_header, timeout=self.s.get_timeout).text
        except: return "None"
    
    def _get_page_selenium(self, url: str, first_page: bool = False) -> str:
        """Make a GET request and get the html page of a specific url using selenium module

        Args:
            url (str): url/link
            first_page (bool, optional): True if url is the base url. Defaults to False.

        Returns:
            str: html page or NOne
        """
        
        try:
            self.driver.get(url)
            # scroll down all page or first is settings is set True
            if self.s.scroll_all_page or (first_page and self.s.scroll_first_page): self._selenium_scroll_page(self.driver)
            return self.driver.page_source
        except: return "None"
    
    def _selenium_scroll_page(self, driver: WebDriver):
        """Script to scroll down a page on selenim webdriver

        Args:
            driver (WebDriver): driver with set page to scroll down
        """
        
        def check_for_end_page(driver: WebDriver, last_height: int, occurence: int = 0, waittime: int = 0.05) -> bool:
            """Check if page height has not move since last scroll down and page has not load new content

            Args:
                driver (WebDriver): selenium webdriver
                last_height (int): height after last scroll down
                occurence (int, optional): number of time function have wait the page to load new content. Defaults to 0.
                waittime (int, optional): wait time between each occurence. Defaults to 0.05.

            Returns:
                bool: True if no new content has been generated, or False if no new content has been generated.
            """
            
            MAX_OCCURENCE = 20
            if occurence == MAX_OCCURENCE: return True
            if driver.execute_script("return document.body.scrollHeight") == last_height:
                sleep(waittime)
                return check_for_end_page(driver, last_height, occurence+1)
            else: return False
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if check_for_end_page(driver, last_height): break
            last_height = driver.execute_script("return document.body.scrollHeight")
    
    def _children_element_xpath(self, text: str) -> str:
        """Use to filter some elements of a page with xpath, that will be used to find links

        Args:
            text (str): html page

        Returns:
            str: joined found childrens elements
        """
        
        # give the html (text) to the etree and search for element with xpath
        elements: List[etree._Element] = etree.HTML(text).xpath(self.s.xpath_restrict_link_crawl)
        # get and join all the childrens elements to form a single string
        return "\n".join([etree.tostring(elem).decode() for elem in elements])
    
    def __del__(self):
        if self.s.simulate_human: self.driver.quit()