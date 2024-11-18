import scrapy
from coursescraper.items import CourseItem


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

            # code = course.css("div.cols .detail-coursecode strong::text").get()
            code_parts = course.css(
                "div.cols .detail-coursecode strong::text, div.cols .detail-coursecode strong a::text"
            ).getall()
            code = " ".join(code_parts).strip()

            name = course.css("div.cols .detail-title strong::text").get()
            hours = course.css("div.cols .detail-hours_html::text").get()

            # strip and rejoin b/c of a tags
            description_parts = course.css(
                "div.noindent p.courseblockextra::text, div.noindent p.courseblockextra a::text"
            ).getall()
            description = " ".join(description_parts).strip()

            # same thing here
            restrictions = course.css(
                "p.courseblockextra.noindent a::text, p.courseblockextra.noindent::text"
            ).getall()
            restrictions_text = " ".join(restrictions).strip() if restrictions else None

            course_item = CourseItem()

            course_item["code"] = code
            course_item["name"] = name
            course_item["hours"] = hours
            course_item["description"] = description
            course_item["restrictions"] = restrictions_text

            yield course_item
