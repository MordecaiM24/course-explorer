import scrapy


class CoursespiderSpider(scrapy.Spider):
    name = "coursespider"
    allowed_domains = ["catalog.ncsu.edu"]
    start_urls = ["https://catalog.ncsu.edu/course-descriptions/"]

    def parse(self, response):
        department_links = response.css("div.az_sitemap ul li a::attr(href)").getall()
        for link in department_links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_department)

    def parse_department(self, response):
        courses = response.css("div.courseblock")
        for course in courses:

            code = course.css("div.cols .detail-coursecode strong::text").get()
            name = course.css("div.cols .detail-title strong::text").get()
            hours = course.css("div.cols .detail-hours_html::text").get()

            description_parts = course.css(
                "div.noindent p.courseblockextra::text, div.noindent p.courseblockextra a::text"
            ).getall()
            description = " ".join(description_parts).strip()

            restrictions = course.css(
                "p.courseblockextra.noindent a::text, p.courseblockextra.noindent::text"
            ).getall()
            restrictions_text = " ".join(restrictions).strip() if restrictions else None

            yield {
                "code": code,
                "name": name,
                "hours": hours,
                "description": description,
                "restrictions": restrictions_text,
            }
