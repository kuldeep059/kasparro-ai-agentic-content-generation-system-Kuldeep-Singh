from logic_blocks.data_models import ProductModel
from typing import Dict, Any

class DataIngestionAgent:
    """
    Agent 1: Data Ingestion Agent
    Responsibility: Read the raw text input and convert it into a structured ProductModel.
    Input: Path to the raw data file.
    Output: ProductModel object.
    """
    def __init__(self, data_path: str = "data/raw_product_data.txt"):
        self.data_path = data_path

    def _parse_raw_text(self, raw_text: str) -> Dict[str, str]:
        """Internal function to process the text lines into a key-value dictionary."""
        data = {}
        # Split lines, remove empty ones, and separate by the colon
        for line in raw_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                # Clean up the key and value
                key = key.strip().replace('• ', '').replace('* ', '')
                value = value.strip()
                data[key] = value
        return data

    def run(self) -> ProductModel:
        """The main method that executes the agent's single responsibility."""
        print("🤖 Data Ingestion Agent: Starting parsing...")
        try:
            with open(self.data_path, 'r') as f:
                raw_text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found at: {self.data_path}")

        # 1. Convert raw text to a dictionary
        data_dict = self._parse_raw_text(raw_text)

        # 2. Process data for Pydantic V2 (Handle list splitting and key renaming)
        
        # Keys that need to be split into lists
        list_keys_map = {
            "Skin Type": "skin_type",
            "Key Ingredients": "key_ingredients",
            "Benefits": "benefits"
        }

        final_data = {}
        for raw_key, value in data_dict.items():
            if raw_key in list_keys_map:
                # Split string by comma and space for list conversion
                final_data[list_keys_map[raw_key]] = value.split(', ')
            else:
                # Map other keys to snake_case used in ProductModel
                if raw_key == "Product Name":
                    final_data["product_name"] = value
                elif raw_key == "Concentration":
                    final_data["concentration"] = value
                elif raw_key == "How to Use":
                    final_data["how_to_use"] = value
                elif raw_key == "Side Effects":
                    final_data["side_effects"] = value
                elif raw_key == "Price":
                    final_data["price"] = value

        # 3. Convert dictionary to the internal data model
        try:
            product_model = ProductModel.model_validate(final_data) # Pydantic V2 method
        except Exception as e:
            print(f"Pydantic Validation Error during ingestion: {e}")
            raise

        print(f"✅ Data Ingestion Agent: Successfully parsed '{product_model.product_name}'.")
        return product_model