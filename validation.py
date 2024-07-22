import os
import json
import re

class Validation:
    def __init__(self, data):
        self.data = data
        self.failed_validations = []

    def validate(self):
        validations = [
            self.validate_mandatory_fields,
            self.validate_prices,
            self.validate_variants,
            self.validate_images,
            self.validate_url,
            self.validate_brand
        ]
        
        valid = True
        for validation in validations:
            try:
                if not validation():
                    valid = False
            except KeyError as e:
                self.failed_validations.append(f"Missing key: {e}")
                valid = False
            except Exception as e:
                self.failed_validations.append(f"Other issue: {e}")
                valid = False
        return valid

    def validate_mandatory_fields(self):
        mandatory_fields = ['product_id', 'title', 'price', 'url', 'brand', 'models']
        for field in mandatory_fields:
            if field not in self.data or not self.data[field]:
                self.failed_validations.append(f"Mandatory field {field} is missing or empty.")
                return False
        return True

    def validate_prices(self):
        sale_prices = self.data.get('sale_prices', [])
        prices = self.data.get('prices', [])
        for sale_price in sale_prices:
            if sale_price > self.data['price']:
                self.failed_validations.append(f"Sale price {sale_price} is greater than original price {self.data['price']}.")
                return False
        for price in prices:
            if price > self.data['price']:
                self.failed_validations.append(f"Price {price} is greater than original price {self.data['price']}.")
                return False
        return True

    def validate_variants(self):
        models = self.data.get('models', [])
        if not models:
            self.failed_validations.append(f"No variants available for product {self.data['product_id']}.")
            return True  # Assuming it's valid if no variants are available
        for model in models:
            for variant in model.get('variants', []):
                if 'id' not in variant or 'price' not in variant or 'image' not in variant:
                    self.failed_validations.append(f"Variant is missing mandatory fields in product {self.data['product_id']}.")
                    return False
        return True

    def validate_images(self):
        if 'images' not in self.data or not self.data['images']:
            self.failed_validations.append(f"No images found for product {self.data['product_id']}.")
            return False
        return True

    def validate_url(self):
        url_pattern = re.compile(r'^(http|https)://')
        if not self.data['url'] or not url_pattern.match(self.data['url']):
            self.failed_validations.append(f"Invalid URL {self.data['url']} for product {self.data['product_id']}.")
            return False
        return True

    def validate_brand(self):
        if not self.data.get('brand'):
            self.failed_validations.append(f"Brand is missing for product {self.data['product_id']}.")
            return False
        return True

def validate_data(input_directory, output_directory):
    unique_product_ids = set()
    output_data = []
    duplicate_data = []
    product_id_index = {}

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.jsonl'):
            file_path = os.path.join(input_directory, file_name)
            with open(file_path, 'r') as file:
                for index, line in enumerate(file):
                    data = json.loads(line.strip())
                    product_id = data.get('product_id', 'unknown')
                    
                    if product_id in product_id_index:
                        duplicate_info = product_id_index[product_id]
                        duplicate_info['count'] += 1
                        duplicate_info['indices'].append(index)
                        duplicate_info['file_names'].append(file_name)
                    else:
                        product_id_index[product_id] = {
                            'count': 1,
                            'indices': [index],
                            'file_names': [file_name]
                        }

                    if product_id in unique_product_ids:
                        print(f"Duplicate product_id found: {product_id}")
                        continue
                    unique_product_ids.add(product_id)

                    validator = Validation(data)
                    is_valid = validator.validate()
                    validation_result = {
                        "file_name": file_name,
                        "product_id": product_id,
                        "valid": is_valid,
                        "failed_validations_count": len(validator.failed_validations),
                        "failed_validations": validator.failed_validations
                    }
                    output_data.append(validation_result)

    # Output file in the output directory
    output_file_path = os.path.join(output_directory, 'validation_results.jsonl')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w') as output_file:
        for result in output_data:
            output_file.write(json.dumps(result) + '\n')
    
    # Duplicate file in the output directory
    duplicate_file_path = os.path.join(output_directory, 'duplicate_results.jsonl')
    with open(duplicate_file_path, 'w') as duplicate_file:
        for product_id, info in product_id_index.items():
            if info['count'] > 1:
                duplicate_result = {
                    "product_id": product_id,
                    "duplicated": True,
                    "count": info['count'],
                    "indices": info['indices'],
                    "file_names": info['file_names']
                }
                duplicate_data.append(duplicate_result)
                duplicate_file.write(json.dumps(duplicate_result) + '\n')
    
    print(f"Validation results written to {output_file_path}")
    print(f"Duplicate records written to {duplicate_file_path}")

if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), 'output')
    output_directory = os.path.join(os.getcwd(), 'output')
    validate_data(input_directory, output_directory)