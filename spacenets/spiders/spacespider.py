import scrapy


class SpacespiderSpider(scrapy.Spider):
    name = 'spacespider'
    allowed_domains = ['spacenet.tn']
    start_urls = ['https://spacenet.tn/74-pc-portable-tunisie']

    def parse(self, response):
        laptops = response.css('div.item.col-xs-6.col-sm-4.col-md-3.col-lg-3')
        for laptop in laptops:
            absolute_url = laptop.css('h2.product_name a::attr(href)').get()
            yield response.follow(absolute_url, callback=self.parse_laptop_page)
        
        next_page = response.css('li a.js-search-link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_laptop_page(self, response):
        yield {
            'name': response.css('h1::text').get().strip(),
            'price': response.css('div.current-price span::attr(content)').get(),
            'formatted_price': response.css('div.current-price span::text').get().strip(),
            'operating_system': response.css('dt.name:contains("Système d\'exploitation") + dd.value::text').get().strip(),
            'memory': response.css('dt.name:contains("Mémoire") + dd.value::text').get().strip(),
            'ports': response.css('dt.name:contains("Ports") + dd.value::text').get().strip(),
            'wireless_connectivity': response.css('dt.name:contains("Connectivité sans-fil") + dd.value::text').get().strip(),
            'garranty': response.css('dt.name:contains("Garantie") + dd.value::text').get().strip(),
            'screen_size': response.css('dt.name:contains("Taille de l\'écran") + dd.value::text').get().strip(),
            'processor_type': response.css('dt.name:contains("Type de Processeur") + dd.value::text').get().strip(),
            'hard_drive': response.css('dt.name:contains("Disque Dur") + dd.value::text').get().strip(),
            'cache': response.css('dt.name:contains("Cache") + dd.value::text').get().strip(),
            'graphics_card': response.css('dt.name:contains("Carte Graphique") + dd.value::text').get().strip(),
            'processor_details': response.css('dt.name:contains("processeur") + dd.value::text').get().strip(),
            'color': response.css('dt.name:contains("Couleur") + dd.value::text').get().strip(),
            'touchscreen': response.css('dt.name:contains("Tactile") + dd.value::text').get().strip(),
            'gamer': response.css('dt.name:contains("Gamer") + dd.value::text').get().strip(),
            'graphics_card_ref': response.css('dt.name:contains("Réf Carte Graphique") + dd.value::text').get().strip(),
            'pc_range': response.css('dt.name:contains("Gamme PC") + dd.value::text').get().strip(),
        }
