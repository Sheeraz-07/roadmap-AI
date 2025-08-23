"""
LLM Agent implementations for GPT-4.1 (Strategist) and Gemini (Refiner)
"""
import openai
import google.generativeai as genai
from typing import Dict, Optional, List
from config import Config
import logging

# Optional import for component searcher
try:
    from component_searcher import ComponentSearcher
    COMPONENT_SEARCH_AVAILABLE = True
except ImportError:
    COMPONENT_SEARCH_AVAILABLE = False
    ComponentSearcher = None

logger = logging.getLogger(__name__)

class StrategistAgent:
    """GPT-4.1 Agent acting as the Strategist - Initial high-level analysis and roadmap creation"""
    
    def __init__(self):
        # Use legacy OpenAI client (v0.28.1)
        openai.api_key = Config.OPENAI_API_KEY
        self.client = None  # Use module-level functions
        self.model = Config.GPT_MODEL
        self.temperature = Config.STRATEGIST_TEMPERATURE
        self.component_searcher = ComponentSearcher() if COMPONENT_SEARCH_AVAILABLE else None
    
    def generate_initial_roadmap(self, user_input: str) -> str:
        """
        Generate initial project roadmap based on user requirements
        
        Args:
            user_input: User's project description and requirements
            
        Returns:
            Detailed project roadmap as string
        """
        
        # Extract components for pricing research if applicable
        component_data = ""
        
        if self.component_searcher:
            try:
                components = self.component_searcher.extract_components(user_input)
                if components:
                    logger.info(f"Found {len(components)} components to research: {components}")
                    pricing_data = self.component_searcher.search_components(components)
                    if pricing_data:
                        component_data = f"\n\nCOMPONENT PRICING DATA:\n{pricing_data}"
                        logger.info("Successfully retrieved component pricing data")
            except Exception as e:
                logger.warning(f"Could not retrieve component pricing: {e}")
        
        # Determine project type and create appropriate system prompt
        project_type = self._detect_project_type(user_input)
        system_prompt = self._get_system_prompt_for_project_type(project_type)
        
        user_prompt = f"""Create a comprehensive project roadmap for the following requirements:

PROJECT REQUIREMENTS: {user_input}

INSTRUCTIONS:
1. Analyze the project requirements and create a detailed, actionable roadmap
2. Include specific technologies, frameworks, and tools (NO generic placeholders)
3. Provide realistic timelines and milestones
4. Include technical architecture and implementation details
5. Consider scalability, security, and best practices
6. If hardware/IoT components are involved, include specific part numbers and pricing
7. Structure the roadmap with clear phases and deliverables

{component_data}

Provide a detailed roadmap that a developer can immediately start implementing."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Strategist Agent error: {str(e)}")
            raise Exception(f"Strategist Agent error: {str(e)}")
    
    def _detect_project_type(self, user_input: str) -> str:
        """Detect the type of project to customize the system prompt"""
        user_lower = user_input.lower()
        
        # IoT/Hardware project detection
        iot_keywords = ['iot', 'sensor', 'arduino', 'raspberry pi', 'esp32', 'monitoring', 'smart', 'automation']
        if any(keyword in user_lower for keyword in iot_keywords):
            return 'iot_hardware'
        
        # Mobile app detection
        mobile_keywords = ['mobile app', 'ios', 'android', 'smartphone', 'app store', 'mobile']
        if any(keyword in user_lower for keyword in mobile_keywords):
            return 'mobile_app'
        
        # Web platform detection
        web_keywords = ['website', 'web app', 'dashboard', 'portal', 'online platform', 'web']
        if any(keyword in user_lower for keyword in web_keywords):
            return 'web_platform'
        
        # AI/ML project detection
        ai_keywords = ['ai', 'machine learning', 'chatbot', 'recommendation', 'prediction', 'nlp']
        if any(keyword in user_lower for keyword in ai_keywords):
            return 'ai_ml'
        
        # E-commerce detection
        ecommerce_keywords = ['e-commerce', 'marketplace', 'shopping', 'payment', 'cart', 'store']
        if any(keyword in user_lower for keyword in ecommerce_keywords):
            return 'ecommerce'
        
        return 'general_software'
    
    def _get_system_prompt_for_project_type(self, project_type: str) -> str:
        """Get appropriate system prompt based on project type"""
        
        base_prompt = """You are an expert software architect and project strategist with 15+ years of experience in full-stack development, system design, and project management."""
        
        if project_type == 'iot_hardware':
            return f"""{base_prompt}

SPECIALIZATION: IoT and Hardware Systems
- Expert in microcontrollers (Arduino, ESP32, Raspberry Pi)
- Extensive knowledge of sensors, actuators, and electronic components
- Experience with IoT protocols (MQTT, HTTP, WebSocket)
- Skilled in embedded programming (C++, Python, MicroPython)
- Knowledge of PCB design and hardware integration
- Experience with cloud IoT platforms (AWS IoT, Google Cloud IoT)

MANDATORY REQUIREMENTS:
- Provide SPECIFIC component part numbers and suppliers
- Include detailed wiring diagrams and connection specifications
- Specify exact sensor models and their technical specifications
- Include realistic pricing for all hardware components
- Provide code examples for microcontroller programming
- Consider power consumption and battery life
- Include enclosure and mounting considerations"""

        elif project_type == 'mobile_app':
            return f"""{base_prompt}

SPECIALIZATION: Mobile Application Development
- Expert in iOS (Swift, SwiftUI) and Android (Kotlin, Java) development
- Experience with cross-platform frameworks (React Native, Flutter)
- Knowledge of mobile UI/UX best practices
- Skilled in mobile backend integration and APIs
- Experience with app store deployment and optimization
- Understanding of mobile security and performance optimization

MANDATORY REQUIREMENTS:
- Specify target platforms (iOS, Android, or both)
- Include specific frameworks and development tools
- Provide detailed UI/UX wireframes and user flows
- Include backend API specifications
- Consider offline functionality and data synchronization
- Include app store submission requirements
- Specify testing strategies for different devices"""

        elif project_type == 'web_platform':
            return f"""{base_prompt}

SPECIALIZATION: Web Platform Development
- Expert in modern web frameworks (React, Vue.js, Angular, Next.js)
- Extensive backend experience (Node.js, Python, Java, .NET)
- Database design and optimization (SQL, NoSQL)
- Cloud deployment and DevOps (AWS, Azure, GCP)
- Web security and performance optimization
- API design and microservices architecture

MANDATORY REQUIREMENTS:
- Specify exact tech stack (frontend, backend, database)
- Include detailed database schema design
- Provide API endpoint specifications
- Include authentication and authorization strategy
- Consider scalability and performance requirements
- Include deployment and hosting recommendations
- Specify security measures and compliance requirements"""

        elif project_type == 'ai_ml':
            return f"""{base_prompt}

SPECIALIZATION: AI and Machine Learning Systems
- Expert in ML frameworks (TensorFlow, PyTorch, Scikit-learn)
- Experience with NLP, computer vision, and recommendation systems
- Knowledge of data preprocessing and feature engineering
- Skilled in model deployment and MLOps
- Experience with cloud AI services (AWS SageMaker, Google AI Platform)
- Understanding of AI ethics and bias mitigation

MANDATORY REQUIREMENTS:
- Specify exact ML frameworks and libraries
- Include data collection and preprocessing strategies
- Provide model architecture and training approach
- Include evaluation metrics and validation methods
- Consider model deployment and serving infrastructure
- Include data privacy and security considerations
- Specify monitoring and model maintenance strategies"""

        elif project_type == 'ecommerce':
            return f"""{base_prompt}

SPECIALIZATION: E-commerce Platform Development
- Expert in e-commerce frameworks (Shopify, WooCommerce, Magento)
- Experience with payment processing (Stripe, PayPal, Square)
- Knowledge of inventory management and order fulfillment
- Skilled in e-commerce security and PCI compliance
- Experience with marketing automation and analytics
- Understanding of SEO and conversion optimization

MANDATORY REQUIREMENTS:
- Specify e-commerce platform or custom solution approach
- Include detailed payment gateway integration
- Provide inventory management system design
- Include order processing and fulfillment workflow
- Consider security and PCI compliance requirements
- Include marketing and analytics integration
- Specify mobile responsiveness and performance optimization"""

        else:  # general_software
            return f"""{base_prompt}

SPECIALIZATION: General Software Development
- Expert in multiple programming languages and frameworks
- Experience with system architecture and design patterns
- Knowledge of database design and API development
- Skilled in testing, deployment, and maintenance
- Experience with agile development methodologies
- Understanding of software security and performance optimization

MANDATORY REQUIREMENTS:
- Analyze requirements and recommend appropriate tech stack
- Provide detailed system architecture and component design
- Include specific frameworks, libraries, and tools
- Consider scalability, maintainability, and performance
- Include testing strategy and quality assurance
- Provide deployment and hosting recommendations
- Consider security and data protection requirements"""
    
    def refine_roadmap(self, original_roadmap: str, refiner_feedback: str) -> str:
        """Refine the roadmap based on Refiner's feedback"""
        
        system_prompt = """You are an expert project strategist. You previously created a project roadmap, and now you've received detailed feedback from a specialist reviewer. Your task is to integrate this feedback and improve the original roadmap.

Focus on:
1. Addressing all concerns and suggestions raised in the feedback
2. Incorporating better approaches and alternatives suggested
3. Fixing any logical inconsistencies or gaps identified
4. Enhancing the practical implementation aspects
5. Maintaining the overall structure while improving details

Create an improved version that addresses the feedback while maintaining clarity and actionability."""

        user_prompt = f"""Here is the original roadmap you created:

{original_roadmap}

Here is the detailed feedback from the specialist reviewer:

{refiner_feedback}

Please create an improved version of the roadmap that addresses all the feedback points and incorporates the suggested improvements."""

        try:
            # Use legacy OpenAI client
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Strategist Agent refinement error: {str(e)}")


class RefinerAgent:
    """Gemini Agent acting as the Refiner - Critical evaluation and improvement suggestions"""
    
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.temperature = Config.REFINER_TEMPERATURE
    
    def analyze_roadmap(self, roadmap: str, iteration: int = 1) -> str:
        """Analyze the roadmap and provide critical feedback and improvements"""
        
        if iteration == 1:
            prompt = f"""You are an expert project analyst and critic specializing in identifying weaknesses and improvement opportunities in project roadmaps. Your role is to provide constructive, detailed feedback.

Analyze the following project roadmap and provide comprehensive feedback focusing on:

1. **Logical Consistency**: Are there any contradictions or gaps in the plan?
2. **Feasibility Assessment**: Are the proposed timelines and resource requirements realistic?
3. **Risk Analysis**: What potential challenges or risks are missing or underestimated?
4. **Technical Soundness**: Are the technical approaches appropriate and current?
5. **Implementation Details**: What critical implementation details are missing?
6. **Alternative Approaches**: What better or more efficient alternatives exist?
7. **Scalability & Maintenance**: How well does the plan address long-term considerations?

For each area, provide:
- Specific issues identified
- Detailed recommendations for improvement
- Alternative approaches where applicable
- Practical implementation suggestions

Be thorough, constructive, and focus on actionable improvements.

ROADMAP TO ANALYZE:
{roadmap}

Provide your detailed analysis and recommendations:"""
        
        else:  # Final iteration
            prompt = f"""You are conducting a final review of a refined project roadmap. This roadmap has already been through one iteration of improvement based on previous feedback.

Your task is to:
1. Verify that previous concerns have been adequately addressed
2. Identify any remaining issues or new concerns
3. Provide final polish suggestions
4. Confirm the roadmap's readiness for implementation

Focus on:
- Overall coherence and completeness
- Practical implementability
- Clear next steps for the user
- Final quality assurance

If the roadmap is satisfactory, acknowledge its strengths and provide any final minor suggestions.

REFINED ROADMAP TO REVIEW:
{roadmap}

Provide your final evaluation and any remaining recommendations:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=4000
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Refiner Agent error: {str(e)}")
    
    def final_evaluation(self, final_roadmap: str) -> str:
        """Provide final evaluation and present the polished roadmap"""
        
        prompt = f"""You are presenting the final, refined project roadmap to the user. This roadmap has been through multiple iterations of improvement and refinement.

Your task is to:
1. Present the roadmap in a clean, professional format
2. Highlight the key strengths and benefits
3. Provide clear next steps for implementation
4. Remove any references to the refinement process
5. Ensure the content is user-friendly and actionable

Format the final output as a comprehensive, standalone project roadmap that the user can immediately act upon.

FINAL ROADMAP:
{final_roadmap}

Present this as the definitive project roadmap:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower temperature for final formatting
                    max_output_tokens=4000
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Refiner Agent final evaluation error: {str(e)}")
