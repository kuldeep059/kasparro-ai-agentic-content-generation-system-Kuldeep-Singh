from logic_blocks.data_models import ProductModel, ComparisonProductModel, ContentLogicModel
from templates.page_templates import FAQ_PAGE_TEMPLATE, PRODUCT_PAGE_TEMPLATE, COMPARISON_PAGE_TEMPLATE
from datetime import date
import json

class PageAssemblerAgent:
    """
    Agent 4: Page Assembler Agent
    Responsibility: Take all structured data models and apply them to the templates, 
    then output the final content as machine-readable JSON files.
    Input: ProductModel, ComparisonProductModel, ContentLogicModel.
    Output: Three JSON files in the 'output/' directory.
    """
    def __init__(self, product_data: ProductModel, product_b_data: ComparisonProductModel, content_data: ContentLogicModel):
        self.product_data = product_data
        self.product_b_data = product_b_data
        self.content_data = content_data
        self.output_dir = "output/"

    def _apply_template(self, template: dict) -> dict:
        """
        Simple recursive function to replace placeholders in the template with 
        actual values from the data models.
        """
        assembled_page = template.copy()
        
        # Prepare data points for easy access
        prod_data_dict = self.product_data.model_dump()
        prod_b_data_dict = self.product_b_data.model_dump()
        content_data_dict = self.content_data.model_dump()
        
        # Add string representations of lists for the templates
        prod_data_dict['skin_type_str'] = ", ".join(self.product_data.skin_type)
        prod_data_dict['benefits_str'] = "; ".join(self.product_data.benefits)
        prod_b_data_dict['skin_type_str'] = ", ".join(self.product_b_data.skin_type)
        
        # Simple string replacement (simulation of a proper template engine)
        assembled_json_str = json.dumps(assembled_page)
        
        # 1. Product Data Replacements (GlowBoost)
        for key, value in prod_data_dict.items():
            if isinstance(value, list):
                 value = "; ".join(value) # Use the string versions for template text
            
            # Handle list-to-string conversion for placeholders
            if f"{{{{product_data.{key}_str}}}}" in assembled_json_str:
                assembled_json_str = assembled_json_str.replace(f"{{{{product_data.{key}_str}}}}", str(value).replace('"', ''))
            elif f"{{{{product_data.{key}}}}}" in assembled_json_str:
                assembled_json_str = assembled_json_str.replace(f"{{{{product_data.{key}}}}}" , str(value).replace('"', ''))
        
        # 2. Comparison Product Data Replacements (Product B)
        for key, value in prod_b_data_dict.items():
            if f"{{{{product_b_data.{key}}}}}" in assembled_json_str:
                assembled_json_str = assembled_json_str.replace(f"{{{{product_b_data.{key}}}}}" , str(value).replace('"', ''))

        # 3. Content Data Replacements
        assembled_json_str = assembled_json_str.replace("{{content_data.product_summary_block}}", self.content_data.product_summary_block)
        
        # 4. Global Replacements
        assembled_json_str = assembled_json_str.replace("{{current_date}}", date.today().isoformat())

        # Convert back to dict and handle complex lists (FAQ/Questions)
        final_dict = json.loads(assembled_json_str)
        
        if final_dict.get("page_type") == "faq":
            # Map the generated lists directly into the template structure
            for block in final_dict['content_blocks']:
                if block.get('block_type') == 'questions_for_planning':
                    block['questions'] = content_data_dict['user_questions']
                elif block.get('block_type') == 'published_qa_list':
                    block['qa_pairs'] = content_data_dict['faq_q_a_pairs']
        
        # Handle ingredient/benefit access for the comparison page (manual list access)
        if final_dict.get("page_type") == "comparison_table":
            final_dict['comparison_points'][0]['glowboost'] = self.product_data.key_ingredients[0]
            final_dict['comparison_points'][0]['competitor'] = self.product_b_data.key_ingredients[0]
            final_dict['comparison_points'][2]['glowboost'] = self.product_data.benefits[0]
            final_dict['comparison_points'][2]['competitor'] = self.product_b_data.benefits[0]
            
        return final_dict

    def run(self):
        """Executes the agent's single responsibility: assembling and saving pages."""
        print("🤖 Page Assembler Agent: Starting page assembly and file output...")

        pages = {
            "faq.json": self._apply_template(FAQ_PAGE_TEMPLATE),
            "product_page.json": self._apply_template(PRODUCT_PAGE_TEMPLATE),
            "comparison_page.json": self._apply_template(COMPARISON_PAGE_TEMPLATE),
        }

        for filename, content in pages.items():
            file_path = f"{self.output_dir}{filename}"
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=4)
            print(f"✅ Page Assembler Agent: Saved final output to {file_path}")
        
        print("--- Pipeline Complete: 4 Agents Orchestrated ---")