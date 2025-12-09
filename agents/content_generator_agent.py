from logic_blocks.data_models import ProductModel, ComparisonProductModel, ContentLogicModel
from logic_blocks.content_logic import (
    generate_descriptive_summary_block, 
    generate_categorized_questions,
    generate_faq_answers
)
from typing import List

class ContentGeneratorAgent:
    """
    Agent 3: Content Generator Agent
    Responsibility: Coordinate the Content Logic Blocks to generate all required 
    content components (questions, answers, summary blocks).
    Input: ProductModel and ComparisonProductModel.
    Output: ContentLogicModel.
    """
    def __init__(self, product_data: ProductModel, product_b_data: ComparisonProductModel):
        self.product_data = product_data
        self.product_b_data = product_b_data # Required later for comparison content

    def run(self) -> ContentLogicModel:
        """Executes the content generation pipeline using reusable blocks."""
        print("🤖 Content Generator Agent: Starting content production...")
        
        generated_content = ContentLogicModel()

        # 1. Generate Product Summary Block (for Product Page)
        generated_content.product_summary_block = generate_descriptive_summary_block(self.product_data)
        print("   -> Generated Product Summary Block.")
        
        # 2. Generate Categorized Questions (for FAQ Page planning - must be 15+)
        generated_content.user_questions = generate_categorized_questions(self.product_data)
        print(f"   -> Generated {len(generated_content.user_questions)} Categorized Questions.")
        
        # 3. Generate Q&A Pairs (for FAQ Page - must be 5 minimum)
        generated_content.faq_q_a_pairs = generate_faq_answers(
            generated_content.user_questions, 
            self.product_data
        )
        print(f"   -> Generated {len(generated_content.faq_q_a_pairs)} FAQ Q&A pairs (Minimum 5 met).")
        
        # NOTE: We will add the Comparison Callout Block logic later in a dedicated block
        # since it's a specific, rule-based comparison.

        print("✅ Content Generator Agent: Content generation complete.")
        return generated_content