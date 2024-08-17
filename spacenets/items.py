import scrapy

class LaptopItem(scrapy.Item):
    # Define fields specific to laptops
    name = scrapy.Field()
    price = scrapy.Field()
    formatted_price = scrapy.Field()
    operating_system = scrapy.Field()
    memory = scrapy.Field()
    ports = scrapy.Field()
    wireless_connectivity = scrapy.Field()
    warranty = scrapy.Field()
    screen_size = scrapy.Field()
    processor_type = scrapy.Field()
    hard_drive = scrapy.Field()
    cache = scrapy.Field()
    graphics_card = scrapy.Field()
    processor_details = scrapy.Field()
    color = scrapy.Field()
    touchscreen = scrapy.Field()
    gamer = scrapy.Field()
    graphics_card_ref = scrapy.Field()
    pc_range = scrapy.Field()

class ComputerItem(scrapy.Item):
    # Define fields specific to computers
    name = scrapy.Field()
    price = scrapy.Field()
    formatted_price = scrapy.Field()
    warranty = scrapy.Field()
    screen_size = scrapy.Field()
    brightness = scrapy.Field()
    contrast_ratio = scrapy.Field()
    response_time = scrapy.Field()
    screen_format = scrapy.Field()
    connectors = scrapy.Field()
    color = scrapy.Field()
    panel_type = scrapy.Field()
    touchscreen = scrapy.Field()
    gamer = scrapy.Field()
    refresh_rate = scrapy.Field()
