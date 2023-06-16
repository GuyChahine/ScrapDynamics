from json import load

import scrapdynamics as sd
from scrapdynamics.settings import Settings

class TestCrawler():
        
    def setup_class(self):
        with open("./tests/data/test_site/site1.html", "r") as f: self.test_site1 = f.read()
        with open("./tests/data/test_site/site1_results.json") as f: self.test_site1_results = load(f)
        
    def teardown_class(self):
        self.test_site1 = None
        self.test_site1_results = None
        
    def test_start_requests(self):
        s = Settings(
            simulate_human=False,
            progress_bar=False,
            depth=1,
            restrict_to_domain=True
        )
        c = sd.Crawler("https://testpages.herokuapp.com/", s)
        c.start()
        
    def test_start_selenium(self):
        s = Settings(
            simulate_human=True,
            headless=True,
            scroll_first_page=True,
            progress_bar=False,
            depth=1,
            restrict_to_domain=True
        )
        c = sd.Crawler("https://testpages.herokuapp.com/", s)
        c.start()
        
    def test_start_progress_bar(self):
        s = Settings(
            simulate_human=False,
            progress_bar=True,
            depth=1,
            restrict_to_domain=True
        )
        c = sd.Crawler("https://testpages.herokuapp.com/", s)
        c.start()
        
    def test_children_element_xpath(self):
        s = Settings(
            simulate_human=False,
            progress_bar=False,
            depth=1,
            restrict_to_domain=True,
            xpath_restrict_link_crawl="/html/body/div"
        )
        c = sd.Crawler("https://example.org", s)
        assert c._children_element_xpath(self.test_site1) == self.test_site1_results["div_children_elements"]