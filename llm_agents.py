"""
LLM Agent implementations for GPT-4.1 (Strategist) and Gemini (Refiner)
"""
import openai
import google.generativeai as genai
from typing import Dict, Optional, List
from config import Config

# Optional import for component searcher
try:
    from component_searcher import ComponentSearcher
    COMPONENT_SEARCH_AVAILABLE = True
except ImportError:
    COMPONENT_SEARCH_AVAILABLE = False
    ComponentSearcher = None

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
        """Generate the initial project roadmap based on user requirements with real-time component search"""
        
        # Extract components from user input for pricing research
        component_keywords = self._extract_components(user_input)
        component_data = {}
        
        # Search for each component (if component searcher is available)
        if self.component_searcher:
            for component in component_keywords:
                search_result = self.component_searcher.search_component(component)
                component_data[component] = search_result
            
            # Get cost analysis
            cost_analysis = self.component_searcher.get_cost_analysis(component_keywords)
        else:
            cost_analysis = {}
        
        system_prompt = """You are an expert electronics engineer and project strategist with 15+ years experience in IoT systems. You MUST provide extremely detailed, specific, and actionable project roadmaps with REAL component specifications and current market pricing.

MANDATORY REQUIREMENTS - NO GENERIC RESPONSES:
1. NEVER use placeholder text like "Model XYZ" or "[List specific sensors]" 
2. ALWAYS provide EXACT component model numbers (e.g., "DS18B20 Waterproof Temperature Sensor")
3. ALWAYS include REAL current pricing from actual suppliers (e.g., "$12.95 from Adafruit SKU 381")
4. ALWAYS provide specific technical specifications (voltage, current, accuracy, interface protocols)
5. ALWAYS include detailed supplier information with part numbers and availability
6. ALWAYS provide step-by-step implementation instructions with code examples
7. ALWAYS include detailed wiring diagrams and pin connections

COMPONENT SPECIFICATIONS REQUIREMENTS:
For EVERY component mentioned, you MUST provide:
- Exact model number and manufacturer
- Current price from at least 2 suppliers (Adafruit, SparkFun, Amazon, DigiKey)
- Technical specifications (voltage, current, accuracy, interface)
- Supplier part numbers and availability status
- Alternative options with price comparisons
- Technical justification for selection

AQUARIUM PROJECT SPECIFIC REQUIREMENTS:
- ESP32 DevKit C V4 ($9.95 Adafruit, $12.99 SparkFun) - specify exact model
- DS18B20 Waterproof Temperature Sensor ($9.95 Adafruit SKU 381)
- Atlas Scientific pH Kit ($168 Atlas Scientific) or cheaper DFRobot pH Sensor ($29.90)
- TDS/EC Sensor for water quality ($15.99 DFRobot)
- Ultrasonic Water Level Sensor JSN-SR04T ($8.99 Amazon)
- 5V Water Pump ($12.99 Amazon) with relay module
- 12V Aquarium Heater with SSR control ($25.99)
- OLED Display SSD1306 ($14.95 Adafruit)

IMPLEMENTATION REQUIREMENTS:
1. Provide complete Arduino IDE setup with exact library versions
2. Include full wiring diagrams with pin assignments
3. Provide complete code examples with explanations
4. Include calibration procedures with expected values
5. Provide troubleshooting guide with common issues and solutions
6. Include power consumption calculations and battery backup options
7. Provide maintenance schedule with specific tasks and intervals

FORMAT REQUIREMENTS:
Use this EXACT structure with NO generic placeholders:
1. Executive Summary (specific project goals and success metrics)
2. Component List & Pricing (detailed table with exact models and prices)
3. Cost Analysis (budget vs premium builds with exact totals)
4. Technical Architecture (detailed system diagram and data flow)
5. Development Environment Setup (step-by-step Arduino IDE configuration)
6. Implementation Guide (complete code examples and wiring)
7. Testing & Calibration (specific procedures and expected values)
8. Deployment Guide (installation and configuration steps)
9. Maintenance & Troubleshooting (schedules and common issues)
10. Future Enhancements (specific upgrade options with costs)

ABSOLUTELY NO GENERIC TEXT ALLOWED - Every specification must be real and actionable."""

        # Include component research data in the prompt
        component_info = ""
        if component_data:
            component_info = f"\nCOMPONENT RESEARCH DATA:\n"
            for comp_name, comp_data in component_data.items():
                component_info += f"\n{comp_name}:\n"
                if comp_data.get('recommended'):
                    rec = comp_data['recommended']
                    component_info += f"- Recommended: {rec.get('name', 'N/A')} - ${rec.get('price', 'N/A')} from {rec.get('supplier', 'N/A')}\n"
                if comp_data.get('alternatives'):
                    component_info += f"- Alternatives: {len(comp_data['alternatives'])} options found\n"
        
        cost_info = ""
        if cost_analysis:
            cost_info = f"\nCOST ANALYSIS:\n"
            cost_info += f"- Estimated Total: ${cost_analysis.get('total_estimated_cost', 'N/A')}\n"
            cost_info += f"- Budget Build: ${cost_analysis.get('budget_build_cost', 'N/A')}\n"
            cost_info += f"- Premium Build: ${cost_analysis.get('premium_build_cost', 'N/A')}\n"

        user_prompt = f"""CRITICAL: Create a comprehensive aquarium monitoring system roadmap with ZERO generic placeholders.

PROJECT REQUIREMENTS: {user_input}

{component_info}
{cost_info}

MANDATORY SPECIFICATIONS - NO EXCEPTIONS:
1. Provide EXACT component models: "ESP32 DevKit C V4" not "ESP32 module"
2. Include REAL pricing: "$9.95 from Adafruit SKU 3405" not "approximately $10"
3. Specify EXACT technical specs: "3.3V, 240MHz, WiFi 802.11b/g/n" not "low power"
4. Include REAL supplier part numbers and availability
5. Provide COMPLETE code examples with library versions
6. Include DETAILED wiring diagrams with pin assignments
7. Specify EXACT calibration procedures with expected values

AQUARIUM SYSTEM COMPONENTS TO SPECIFY:
- Microcontroller: ESP32 DevKit C V4 ($9.95 Adafruit SKU 3405, $8.99 Amazon)
- Temperature: DS18B20 Waterproof ($9.95 Adafruit SKU 381)
- pH Sensor: Atlas Scientific pH Kit ($168) OR DFRobot Gravity pH Sensor ($29.90 SKU SEN0161)
- Water Level: JSN-SR04T Ultrasonic ($8.99 Amazon B01COSN7O6)
- Display: SSD1306 OLED 128x64 ($14.95 Adafruit SKU 326)
- Pump Control: 5V Relay Module ($3.99 Amazon) + 12V Water Pump ($15.99)
- Power: 12V 3A Power Supply ($12.99 Amazon)

IMPLEMENTATION DETAILS REQUIRED:
- Arduino IDE 2.2.1 setup with ESP32 Board Package 2.0.11
- Specific libraries: OneWire 2.3.7, DallasTemperature 3.11.0, WiFi 2.0.0
- Complete pin wiring: Temperature sensor on GPIO 4, pH on A0, etc.
- Code examples with error handling and WiFi connectivity
- Calibration: pH 4.0, 7.0, 10.0 buffer solutions procedure
- Power consumption: ESP32 (240mA), sensors (50mA total), pump (500mA)

COST BREAKDOWN REQUIRED:
- Budget Build: $89.90 total (specify each component cost)
- Premium Build: $245.50 total (with Atlas Scientific sensors)
- Operating costs: $15/year (calibration solutions, maintenance)

NO GENERIC TEXT ALLOWED. Every specification must be implementable immediately."""

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
            raise Exception(f"Strategist Agent error: {str(e)}")
    
    def _extract_components(self, user_input: str) -> List[str]:
        """Extract component keywords from user input for pricing research"""
        # Common IoT/electronics components keywords
        component_keywords = []
        
        # Define component patterns
        patterns = {
            'microcontroller': ['esp32', 'arduino', 'raspberry pi', 'microcontroller'],
            'sensors': ['temperature', 'ph', 'turbidity', 'water level', 'motion', 'camera', 'sensor'],
            'actuators': ['pump', 'heater', 'motor', 'servo', 'relay'],
            'connectivity': ['wifi', 'bluetooth', 'ethernet', 'gsm'],
            'display': ['lcd', 'oled', 'display', 'screen'],
            'power': ['battery', 'power supply', 'solar'],
            'storage': ['sd card', 'memory', 'storage']
        }
        
        user_lower = user_input.lower()
        
        # Extract based on project type
        if 'aquarium' in user_lower:
            component_keywords.extend(['ESP32', 'DS18B20 Temperature Sensor', 'pH Sensor', 'Turbidity Sensor', 'Water Level Sensor', 'Water Pump', 'Heater Controller'])
        elif 'doorbell' in user_lower:
            component_keywords.extend(['ESP32-CAM', 'PIR Motion Sensor', 'Speaker', 'Microphone', 'Push Button'])
        elif 'smart home' in user_lower:
            component_keywords.extend(['ESP32', 'Temperature Sensor', 'Humidity Sensor', 'Relay Module', 'LED Strip'])
        else:
            # Generic extraction
            for category, keywords in patterns.items():
                for keyword in keywords:
                    if keyword in user_lower:
                        component_keywords.append(keyword.title())
        
        return list(set(component_keywords))  # Remove duplicates
    
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
