# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class CoursescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        # remove non breaking spaces (mostly from course codes)
        for field_name in field_names:
            value = adapter.get(field_name)

            if value is not None and isinstance(value, str):
                adapter[field_name] = value.replace("\xa0", " ")

        # get credit hours
        for field_name in field_names:
            if field_name is "hours":
                hours = adapter.get(field_name)

                if hours is not None:
                    match = re.search(r"\(([\d-]+) credit hours\)", hours)
                    if match:
                        adapter[field_name] = match.group(1)

        return item
