"""
Example usage of the Multi-Agent Project Refiner AI System
"""
import os
from multi_agent_orchestrator import ProjectRefinerAPI

def main():
    # Set up API keys (you'll need to provide these)
    # os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
    # os.environ['GEMINI_API_KEY'] = 'your-gemini-api-key'
    
    # Example project description
    project_description = """
    I want to create a comprehensive e-commerce platform for small businesses with the following requirements:

    Core Features:
    - Multi-vendor marketplace with seller onboarding
    - Product catalog management with categories and search
    - Shopping cart and checkout with multiple payment methods
    - Order management and tracking system
    - Customer reviews and ratings
    - Inventory management for sellers
    - Admin dashboard for platform management

    Technical Requirements:
    - Web-based platform (responsive design)
    - Mobile app for customers (iOS and Android)
    - Seller mobile app for inventory management
    - Real-time notifications
    - Analytics and reporting
    - SEO optimization
    - Security compliance (PCI DSS)

    Business Requirements:
    - Support for 1000+ concurrent users
    - Multi-language support (English, Spanish, French)
    - Multi-currency support
    - Commission-based revenue model
    - Integration with shipping providers
    - Customer support system

    Constraints:
    - Budget: $200,000
    - Timeline: 12 months
    - Team: 4 developers, 2 designers, 1 project manager
    - Must be scalable to 50,000 products
    - 99.9% uptime requirement
    """

    try:
        # Initialize the API
        api = ProjectRefinerAPI()
        
        print("🤖 Starting multi-agent project refinement...")
        print("=" * 60)
        
        # Get detailed result
        result = api.refine_project_detailed(project_description)
        
        print("📋 REFINED PROJECT ROADMAP")
        print("=" * 60)
        print(result['roadmap'])
        
        print("\n" + "=" * 60)
        print("📊 PROCESSING METADATA")
        print("=" * 60)
        metadata = result['metadata']
        print(f"Processing Type: {metadata['processing_type']}")
        print(f"Total Tokens: {metadata['total_tokens']:,}")
        print(f"Iterations: {metadata['iterations_completed']}")
        print(f"Processing Time: {metadata['processing_time']:.2f} seconds")
        print(f"Timestamp: {metadata['timestamp']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure to:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Set your GEMINI_API_KEY environment variable")
        print("3. Install all required dependencies")

if __name__ == "__main__":
    main()
