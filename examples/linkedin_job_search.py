"""
In this example, ScrapDynamics is set for scraping job details. 
It include link of the job, job title, description of the job, 
company name, job location, time of posting, and save the results 
in an Excel file.
"""

import scrapdynamics as sd

def main():
    s = sd.Settings(
        depth=1, # depth is set to 1 to only search for the base page and the jobs pages
        simulate_human=True, # use of selenium to scroll down the search page
        scroll_first_page=True,
        headless=False, # headless is True to look at what the crawler is doing
        # here the xpath is set to get only the divs that contain the job link
        xpath_restrict_link_crawl="""//*[@id="main-content"]/section[2]/ul/li/div/a""",
        search_expressions={}, # search_expression is set to empty dict to remove the premade search_expression
    )
    # we define in regex expressions the elements we want to get
    s.search_expressions["job_title"] = r"""<h1 class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title">(.+?)<\/h1>"""
    s.search_expressions["job_description"] = r"""<div class="show-more-less-html__markup relative overflow-hidden show-more-less-html__markup--clamp-after-5">([\w\W]+?)<\/div>"""
    s.search_expressions["company_name"] = r"""<a class="topcard__org-name-link topcard__flavor--black-link" data-tracking-control-name="public_jobs_topcard-org-name" data-tracking-will-navigate="" href=".+?" rel="noopener" target="_blank">([\w\W]+?)<\/a>"""
    s.search_expressions["job_location"] = r"""<span class="topcard__flavor topcard__flavor--bullet">([\w\W]+?)<\/span>"""
    s.search_expressions["time_job_posted"] = r"""<span class="posted-time-ago__text topcard__flavor--metadata">([\w\W]+?)<\/span>"""
    s.search_expressions["hierarchical level, job type, function, sectors"] = r"""<span class="description__job-criteria-text description__job-criteria-text--criteria">([\w\W]+?)<\/span>"""

    # init and start of the crawler
    c = sd.Crawler(URL, s)
    c.start()

    # save it to excel
    c.to_excel("./results.xlsx")

if __name__ == "__main__":
    # you can make a research with the filters and information you want to for your job
    # and paste the link here
    URL = "https://www.linkedin.com/jobs/search/?currentJobId=3627162179&keywords=example"
    main()