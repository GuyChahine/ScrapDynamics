from dataclasses import dataclass, field
from typing import List, Dict
import re

from .settings import Settings

@dataclass
class Url():
    """Dataclass to store information of a specific page
    
    Args:
        url (str): url of the page
        domain (str, optional): domain of the page. Defaults to None
        links (List[str], optional): links found in the page. Defaults to None
        search (Dict[str, List[str]], optional): dict of element searched in the page. Defaults to empty Dict
    """
    
    url: str
    domain: str = None
    links: List[str] = None
    search: Dict[str, List[str]] = field(default_factory=lambda: {})
    
class UrlManager():
    """Store and Manage multiple Url dataclass
    """
    
    s = Settings()
    
    def __init__(self):

        super(UrlManager, self).__init__()
        
        self._url_book: List[Url] = []
    
    def _add_url(self, url: str, page_text: str):
        """Methode that add to url book a new Url dataclass

        Args:
            url (str): url/link to add
            page_text (str): html page of the url
        """
        
        # check if url is already in url book
        if url in [url_object.url for url_object in self._url_book]: return
        
        # create a new Url dataclass
        url_object = Url(url, self._get_domain_from_url(url), links=self._get_links_from_text(url, page_text))
        
        # run through all the regex expression in the settings and store them in search attribute of Url
        for name, expression in self.s.search_expressions.items():
            if expression: url_object.search[name] = [result.strip() for result in re.findall(expression, page_text)]
        self._url_book.append(url_object)
    
    def _get_all_links(self) -> List[str]:
        """Get all links found in the precedent depth

        Returns:
            List[str]: a list of all the links
        """
        
        all_links = []
        for url_object in self._url_book: all_links += url_object.links
        return all_links
    
    def _clean_link(self, url: str, link: str) -> str:
        """Use regex substitution to find if link is schema relative "//google.com/path" 
        or relative "/path/path" or absolute "https://google.com" and add the https: or https://domain
        in front

        Args:
            url (str): url where if link is relative path have complete domain in it
            link (str): link to clean

        Returns:
            str: clean link
        """
        
        link = re.sub(self.s.link_schema_relative_sub[0], self.s.link_schema_relative_sub[1], link)
        link = re.sub(self.s.link_relative_sub[0], self.s.link_relative_sub[1].format(domain=self._get_domain_from_url(url)), link)
        return link
    
    def _get_links_from_text(self, url: str, text: str) -> List[str]:
        """Get all the links from an html page

        Args:
            url (str): url/link where text comes from (to get the domain)
            text (str): html page

        Returns:
            List[str]: list of clean links
        """
        
        links = re.findall(self.s.link_findall, text)
        return [self._clean_link(url, l) for l in links]
    
    def _get_domain_from_url(self, url: str) -> str:
        """Get the domain from a url

        Args:
            url (str): url to get domain

        Returns:
            str: domain
        """
        
        return re.findall(self.s.domain_findall, url)[0]
    
    def _url_to_dict(self) -> Dict[str, List]:
        """Transform url book into a 2 dimentional Dict of List

        Returns:
            Dict[str, List]: 2 dimentional Dict of List
        """
        
        # flatten search dict of Url dict
        flatten_dict: List[Dict[str, str | str, List[str]]] = []
        for url_object in self._url_book:
            d = url_object.__dict__.copy()
            # split search dict of Url dict
            search, remaining = d.pop("search"), d
            # flatten search dict at the same level of the remaining dict
            flatten_dict.append({**remaining, **search})
        
        # Unifie List of Dict that sometimes contain List and str to only contain str
        lod: List[Dict[str: str]] = [{key: ", ".join(value) if type(value) == list else value for key, value in d.items()} for d in flatten_dict]
        # Transform List of Dict into Dict of List
        dol: Dict[str, List[str]] = {key: [d[key] for d in lod] for key in lod[0].keys()}
        return dol