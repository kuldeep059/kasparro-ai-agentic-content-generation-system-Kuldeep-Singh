from agents.data_ingestion_agent import DataIngestionAgent
from agents.fictional_product_agent import FictionalProductAgent
from agents.content_generator_agent import ContentGeneratorAgent
from agents.page_assembler_agent import PageAssemblerAgent # Final Agent Import
from logic_blocks.data_models import ProductModel, ComparisonProductModel, ContentLogicModel

def run_pipeline():
    """
    The main orchestrator function. Executes the multi-agent content generation 
    system pipeline in a step-by-step sequence (step pipeline/DAG).
    """
    print("\n===================================================")
    print("--- Starting Agentic Content Generation Pipeline ---")
    print("===================================================")
    
    # --- STEP 1: Data Ingestion (Agent 1) ---
    ingestion_agent = DataIngestionAgent()
    product_data: ProductModel = ingestion_agent.run()
    
    # --- STEP 2: Fictional Product Creation (Agent 2) ---
    fictional_product_agent = FictionalProductAgent(product_data)
    product_b_data: ComparisonProductModel = fictional_product_agent.run()

    # --- STEP 3: Content Generation (Agent 3) ---
    content_agent = ContentGeneratorAgent(product_data, product_b_data)
    generated_content: ContentLogicModel = content_agent.run()
    
    # --- STEP 4: Page Assembly (Agent 4) ---
    # Agent 4 takes all three structured outputs as input.
    assembler_agent = PageAssemblerAgent(product_data, product_b_data, generated_content)
    assembler_agent.run()
    
    print("\nAll required output files are now available in the 'output/' directory.")
    print("----------------------------------------------------------------------\n")

if __name__ == "__main__":
    run_pipeline()