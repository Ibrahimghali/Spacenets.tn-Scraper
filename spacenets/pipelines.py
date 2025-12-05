# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import json
import os
from datetime import datetime

class SpacenetsPipeline:
    def process_item(self, item, spider):
        return item
    

class DataCleaningPipeline:
    def process_item(self, item, spider):
        """
        Process each item to clean and standardize the data.
        """
        # Clean and standardize the 'name' field
        item['name'] = self.clean_name(item.get('name', ''))
        
        # Clean and standardize the 'price' field
        item['price'] = self.clean_price(item.get('price', ''))
        
        # Clean and standardize the 'formatted_price' field
        item['formatted_price'] = self.clean_formatted_price(item.get('formatted_price', ''))
        
        # Clean and standardize 'features' fields
        item['features'] = self.clean_features(item.get('features', {}))
        
        return item

    def clean_name(self, name):
        """
        Clean the product name by removing extra spaces and normalizing text.
        """
        if name:
            # Strip leading/trailing spaces and normalize text
            name_clean = name.strip()
            # Optionally remove special characters if needed
            name_clean = re.sub(r'[^\w\s]', '', name_clean)  # Remove special characters except whitespace
            return name_clean
        return 'N/A'

    def clean_price(self, price):
        """
        Ensure the price is a float, removing any formatting inconsistencies.
        """
        if isinstance(price, str):
            # Remove any non-numeric characters except decimal points
            price_clean = re.sub(r'[^\d.]', '', price)
            try:
                return float(price_clean)
            except ValueError:
                return None
        elif isinstance(price, (int, float)):
            return float(price)
        return None

    def clean_formatted_price(self, formatted_price):
        """
        Remove special characters from formatted price and convert to a standard format.
        """
        if formatted_price:
            # Remove thousands separators and ensure decimal format
            formatted_price_clean = re.sub(r'[^\d,]', '', formatted_price).replace(',', '.')
            return formatted_price_clean
        return 'N/A'

    def clean_features(self, features):
        """
        Clean and standardize the feature values.
        """
        cleaned_features = {}
        for key, value in features.items():
            # Strip leading/trailing spaces and normalize text
            cleaned_key = key.strip()
            cleaned_value = value.strip()
            
            # Normalize values: Remove unnecessary characters or formatting
            cleaned_value = re.sub(r'\s+', ' ', cleaned_value)  # Replace multiple spaces with a single space
            
            # Add cleaned feature to dictionary
            cleaned_features[cleaned_key] = cleaned_value
        
        return cleaned_features

class JsonExportPipeline:
    """Export items to JSON file"""
    
    def open_spider(self, spider):
        """Create data directory and open file"""
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        scraper_id = os.environ.get('SCRAPER_ID', 'local')
        filename = f'data/spacenets_scraper{scraper_id}_{timestamp}.json'
        self.file = open(filename, 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True
        self.item_count = 0
        spider.logger.info(f'📁 Exporting items to: {filename}')
        
    def close_spider(self, spider):
        """Close file"""
        self.file.write('\n]')
        self.file.close()
        spider.logger.info(f'✅ Finished exporting {self.item_count} items to data folder')
        
    def process_item(self, item, spider):
        """Write item to file"""
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        
        line = json.dumps(dict(item), ensure_ascii=False, indent=2)
        self.file.write(line)
        self.item_count += 1
        
        # Log every 10 items
        if self.item_count % 10 == 0:
            spider.logger.info(f'💾 Exported {self.item_count} items so far...')
        
        return item
