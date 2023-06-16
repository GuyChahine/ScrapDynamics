![scrapdynamics](https://drive.google.com/uc?export=view&id=18H85TiBbdMD5fcxKxKPHMRqX8cY8KOkF)

# ScrapDynamics

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [CLI](#cli)
  - [Library](#library)
- [Advance Usage](#advance-usage)
  - [Settings](#settings)
- [Features](#features)
- [Examples](#examples)

## Introduction

ScrapDynamics is a powerful framework for exploring and crawling websites, extracting links and finding information using regex expressions, making it easy to automate the process of collecting any data on a web.

## Installation

To install ScrapDynamics, you can use the following commands:

```bash
pip install scrapdyanmics
```

## Getting Started

### CLI

To use ScrapDynamics from the command line interface, you can use the following command:

```bash
python -m scrapdynamics -u https://example.org -o ./results.json
```

In this example it starts the crawler at the specified URL "https://example.org" and saves the results in a JSON file at the path "./results.json".

You can also use the following options:

```bash
usage: ScrapDynamics [-h] [-v] [-u URL] [-o OUTPUT]
options:
  -h           --help             show this help message and exit
  -v           --version          show version
  -u URL       --url URL          base url
  -o OUTPUT    --output OUTPUT    path/filename.extention
```

### Library

When using ScrapDynamics as a library, you can import it into your Python code and use the following code snippet:

```python
import scrapdynamics as sd

crawler = sd.Crawler("https://example.org")
crawler.start()
crawler.to_json("./results.json")
```

This code creates a Crawler object with the specified URL, starts the crawling process, and saves the results in a JSON file.

## Advance Usage

### Settings

You can customize the behavior of ScrapDynamics by modifying the settings. Here's an example of how to create a Settings object and set various options:

```python
from scrapdynamics.settings import Settings

settings = Settings()
```

You can modify the following settings:

- **link_findall:** *regex expression to find links*
```python
link_findall = "href=\"((?:https?|\/\w|\/\/\w).+?)\""
```
- **link_relative_sub:** *regex expression to substitute relative links*
```python
link_relative_sub = ["(^\/\w.+?$)", "https://{domain}\1"]
```
- **link_schema_relative_sub:** *regex expression to substitute schema relative links*
```python
link_schema_relative_sub = ["(^(?:\/\/\w).*?$)", "https:\1"]
```
- **domain_findall:** *regex expression to find domain from a url*
```python
domain_findall = "https?:\/\/(?:www\.)?([^\/\s\'\"]+)"
```
- **search_expressions:** *dict of regex expression to look for in the html page*
```python
search_expressions = {
    "title": "(?:<title>|<meta.*?property=\"og:title\".*?content=\")(.*?)(?:<\/title>|\".*?>)",
    "emails": "[\w\-\.]+?\@[\w\-\.]+?\.[\w]+",
    "phones": "(?:tel\:)(\+?[\d\-\ ]{6,20})(?!\d)",
}
```
- **restrict_to_domain:** *restrict future urls to the domain given at the start*
```python
restrict_to_domain = True
```
- **depth:** *max depth to crawl*
```python
depth = 1
```
- **simulate_human:** *use selenium webdriver to get html page*
```python
simulate_human = False
```
- **scroll_first_page:** *selenium webdriver scroll down the first url given at the start*
```python
scroll_first_page = False
```
- **scroll_all_page:** *selenium webdriver scroll down all the url found*
```python
scroll_all_page = False
```
- **headless:** *don't show the page of selenium webdriver*
```python
headless = False
```
- **get_timeout:** *time in seconds of a GET timeout*
```python
get_timeout = 3
```
- **progress_bar:** *use progress bar or simple prints*
```python
progress_bar = False
```
- **request_header:** *header to add when doing a GET request with the module requests*
```python
request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
```
- **valid_content_type:** *content type of page content to allow the crawler to explore*
```python
valid_content_type = ["text/html"]
```

- **xpath_restrict_link_crawl:** *xpath where children elements will be used to find links for depth 1*
```python
xpath_restrict_link_crawl = "/html"
```

Here's an example of how to use the Settings object with ScrapDynamics:

```python
import scrapdynamics as sd
from scrapdynamics.settings import Settings

settings = Settings(progress_bar=True)
crawler = sd.Crawler("https://example.org", settings)
crawler.start()
print(crawler.show())
```

This code creates a Settings object with the progress_bar option set to True, creates a Crawler object with the specified URL and settings, starts the crawling process, and displays the results.

## Features

- **Regex-based Information Extraction:** ScrapDynamics supports the use of regular expressions to search for specific information within the explored website. In addition to the regular expression patterns already implemented, you can define custom regular expression patterns and extract any other structured information.

- **Website Crawling:** ScrapDynamics provides a robust web crawling functionality that allows you to navigate through a website and discover all its accessible pages. It follows links, collects URLs, and traverses the website structure efficiently.

- **Customizable Scraping Rules:** You have full control over the scraping process. You can define the starting URL, specify the depth of crawling, set exclusion rules for certain URLs, and fine-tune the behavior of the crawler according to your requirements.

- **Data Export:** The extracted information can be easily exported to various formats, such as EXCEL, CSV or JSON, allowing you to further analyze or integrate the scraped data into your existing workflows.

## Examples

- [Linkedin Job Scrapping](./examples/linkedin_job_search.py) In this example, ScrapDynamics is set for scraping job details. It include link of the job, job title, description of the job, company name, job location, time of posting, and save the results in an Excel file.
