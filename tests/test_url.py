from json import load

from scrapdynamics.url import Url, UrlManager

class TestUrl():
    
    def test_call(self):
        Url("https://example.com")
        
class TestUrlManager():
    
    def setup_class(self):
        with open("./tests/data/test_site/site1.html", "r") as f: self.test_site1 = f.read()
        with open("./tests/data/test_site/site1_results.json") as f: self.test_site1_results = load(f)
        
    def teardown_class(self):
        self.test_site1 = None
        self.test_site1_results = None
        
    def setup_method(self):
        self.um = UrlManager()
        
    def teardown_method(self):
        self.um = None
            
    def test_add_url(self):
        self.um._add_url("https://example.example.com/path/path/path", self.test_site1)
          
    def test_get_all_links(self):
        url_object = Url(
            "https://example.com", "example.com", ["link1", "link2"]
        )
        self.um._url_book.append(url_object)
        self.um._url_book.append(url_object)
        assert self.um._get_all_links() == ["link1", "link2", "link1", "link2"]
        
    def test_clean_link_relative(self):
        assert self.um._clean_link("https://example.org", "/path/path") == "https://example.org/path/path"
        
    def test_clean_link_schema_relative(self):
        assert self.um._clean_link("https://example.org", "//example2.com/path") == "https://example2.com/path"
        
    def test_clean_link_absolute(self):
        assert self.um._clean_link("https://example.org", "https://example3.org/path/path/path") == "https://example3.org/path/path/path"
        
    def test_get_link_from_text(self):
        links = self.um._get_links_from_text("https://example.com/path/path", self.test_site1)
        assert links == self.test_site1_results["links"]
        
    def test_get_domain_from_url(self):
        assert self.um._get_domain_from_url("https://example.example.net/path/path") == "example.example.net"
        
    def test_url_to_dict(self):
        self.um._url_book.append(Url(
            "https://example.com",
            "example.com",
            ["link1", "link2"],
            {
                "title": ["title1", "title2"],
                "emails": ["email1", "email2"]
            }
        ))
        assert self.um._url_to_dict() == {
            "url": ["https://example.com"],
            "domain": ["example.com"],
            "links": ["link1, link2"],
            "title": ["title1, title2"],
            "emails": ["email1, email2"],
        }
        
    def test_search_expression_title(self):
        self.um._add_url("https://example.org", self.test_site1)
        assert self.um._url_book[0].search["title"] == self.test_site1_results["title"]
        
    def test_search_expression_emails(self):
        self.um._add_url("https://example.org", self.test_site1)
        assert self.um._url_book[0].search["emails"] == self.test_site1_results["emails"]
        
    def test_search_expression_phones(self):
        self.um._add_url("https://example.org", self.test_site1)
        assert self.um._url_book[0].search["phones"] == self.test_site1_results["phones"]