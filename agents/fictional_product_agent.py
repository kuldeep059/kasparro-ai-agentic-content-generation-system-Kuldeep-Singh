from logic_blocks.data_models import ProductModel, ComparisonProductModel
from typing import Dict, Any

class FictionalProductAgent:
    """
    Agent 2: Fictional Product Agent
    Responsibility: Create structured data for the fictional Product B, 
    ensuring it is a reasonable competitor to GlowBoost.
    Input: The parsed ProductModel (for context).
    Output: ComparisonProductModel object.
    """
    def __init__(self, primary_product: ProductModel):
        self.primary_product = primary_product

    def run(self) -> ComparisonProductModel:
        """The main method to generate the fictional comparison data."""
        print("🤖 Fictional Product Agent: Generating Product B data...")
        
        # Define the fictional data based on the required structure 
        # (name, ingredients, benefits, price) .
        fictional_data = {
            # Invent a name
            "product_name": "Radiance 12x Brightening Serum",
            
            # Make the concentration slightly different/higher to create a point of comparison
            "concentration": "12% Niacinamide",
            
            # Different skin type target
            "skin_type": ["Dry", "Normal"],
            
            # Different primary active ingredient
            "key_ingredients": ["Niacinamide", "Ceramides"],
            
            # Complementary but different benefits
            "benefits": ["Texture smoothing", "Minimizes pores", "Hydration"],
            
            # Invent usage and side effects (must be structured)
            "how_to_use": "Apply a pea-sized amount to clean skin twice daily (morning and night).",
            "side_effects": "Slight redness for first-time users.",
            
            # Invent a price point (slightly higher for differentiation)
            "price": "₹999",
            
            # Use the comparison name field
            "comparison_name": "Radiance 12x Brightening Serum"
        }

        # Convert the dictionary into the structured ComparisonProductModel
        try:
            product_b_model = ComparisonProductModel.parse_obj(fictional_data)
        except Exception as e:
            # Handle potential Pydantic errors during manual creation
            print(f"Error creating ComparisonProductModel: {e}")
            raise

        print(f"✅ Fictional Product Agent: Generated '{product_b_model.product_name}'.")
        return product_b_model