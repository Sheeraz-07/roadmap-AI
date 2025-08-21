"""
Main orchestrator for the Multi-Agent Project Refiner AI System
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time
import traceback
from config import Config
from text_processor import TextProcessor
from llm_agents import StrategistAgent, RefinerAgent
from multi_agent_coordinator import MultiAgentCoordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiAgentOrchestrator:
    """
    Main orchestrator that manages the multi-agent workflow between
    Strategist (GPT-4.1) and Refiner (Gemini) agents
    """
    
    def __init__(self):
        # Validate configuration
        Config.validate_config()
        
        # Initialize components
        self.strategist = StrategistAgent()
        self.refiner = RefinerAgent()
        self.text_processor = TextProcessor()
        self.multi_agent_coordinator = MultiAgentCoordinator()
        
        # Workflow state
        self.current_iteration = 0
        self.max_iterations = 3
        self.workflow_history = []
    
    def process_project_request(self, user_input: str) -> Dict[str, any]:
        """
        Main entry point for processing user project requests
        
        Args:
            user_input: Large text containing project requirements
            
        Returns:
            Dict containing the final roadmap and process metadata
        """
        logger.info("Starting multi-agent project refinement process")
        
        # Step 1: Process input
        processed_input = self.text_processor.process_input(user_input)
        
        logger.info(f"Input prepared: {processed_input['processing_type']}, {processed_input['token_count']} tokens")
        
        # Check if this is a complex AI project requiring specialized analysis
        if self._is_complex_ai_project(user_input):
            logger.info("Detected complex AI/multi-agent project - using specialized coordinator")
            return self._process_complex_ai_project(user_input)
        
        # Check if this is an IoT/hardware project requiring specialized analysis
        if self._is_iot_hardware_project(user_input):
            logger.info("Detected IoT/hardware project - using specialized IoT coordinator")
            return self._process_iot_hardware_project(user_input)
        
        # Route to appropriate processing method
        if processed_input['processing_type'] == 'direct':
            return self._process_direct_input(processed_input['content'])
        else:
            return self._process_chunked_input(processed_input['chunks'])
    
    def _process_direct_input(self, content: str) -> Dict:
        """Process direct input through the workflow"""
        prepared_input = {
            'type': 'direct',
            'content': content
        }
        return self._execute_workflow(prepared_input)
    
    def _process_chunked_input(self, chunks: List[str]) -> Dict:
        """Process chunked input through the workflow"""
        # Create summary from chunks
        summary = self.text_processor.summarize_chunks(chunks)
        prepared_input = {
            'type': 'chunked',
            'summary': summary,
            'chunks': chunks,
            'chunk_count': len(chunks),
            'token_count': sum(self.text_processor.count_tokens(chunk) for chunk in chunks)
        }
        return self._execute_workflow(prepared_input)
    
    def _execute_workflow(self, prepared_input: Dict[str, any]) -> Dict[str, any]:
        """Execute the 3-iteration workflow between Strategist and Refiner"""
        
        start_time = datetime.now()
        
        # Determine input content for strategist
        if prepared_input['type'] == 'direct':
            strategist_input = prepared_input['content']
        else:
            # Use summary for large inputs
            strategist_input = f"""Project Requirements Summary:
{prepared_input['summary']}

Note: This is a summary of a larger document with {prepared_input['chunk_count']} sections totaling {prepared_input['token_count']} tokens."""
        
        try:
            # Iteration 1: Strategist creates initial roadmap
            logger.info("Iteration 1: Strategist generating initial roadmap")
            self.current_iteration = 1
            
            initial_roadmap = self.strategist.generate_initial_roadmap(strategist_input)
            self._log_workflow_step("strategist_initial", initial_roadmap)
            
            # Iteration 1: Refiner analyzes and provides feedback
            logger.info("Iteration 1: Refiner analyzing roadmap")
            
            refiner_feedback_1 = self.refiner.analyze_roadmap(initial_roadmap, iteration=1)
            self._log_workflow_step("refiner_feedback_1", refiner_feedback_1)
            
            # Iteration 2: Strategist refines based on feedback
            logger.info("Iteration 2: Strategist refining roadmap")
            self.current_iteration = 2
            
            refined_roadmap = self.strategist.refine_roadmap(initial_roadmap, refiner_feedback_1)
            self._log_workflow_step("strategist_refined", refined_roadmap)
            
            # Iteration 3: Refiner final evaluation and formatting
            logger.info("Iteration 3: Refiner final evaluation")
            self.current_iteration = 3
            
            final_roadmap = self.refiner.final_evaluation(refined_roadmap)
            self._log_workflow_step("refiner_final", final_roadmap)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                'roadmap': final_roadmap,
                'metadata': {
                    'iterations': self.current_iteration,
                    'processing_time': processing_time,
                    'workflow_history': self.workflow_history
                }
            }
            
        except Exception as e:
            logger.error(f"Error in multi-agent refinement: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise Exception(f"Multi-agent refinement failed: {str(e)}")
    
    def _is_complex_ai_project(self, user_input: str) -> bool:
        """Detect if project requires complex multi-agent analysis"""
        ai_keywords = [
            'ai agent', 'multi-agent', 'market research', 'ai system', 
            'machine learning', 'automated research', 'ai team',
            'intelligent system', 'data analysis', 'market intelligence',
            'business intelligence', 'opportunity identification',
            'trend analysis', 'competitive intelligence', 'search all projects',
            'study different industries', 'identify problems', 'solutions',
            'market potential', 'daily idea', 'unbeatable', 'profit',
            'internet search', 'analyze market', 'product launch'
        ]
        
        user_lower = user_input.lower()
        keyword_matches = sum(1 for keyword in ai_keywords if keyword in user_lower)
        
        # Enhanced detection logic for complex AI projects
        has_ai_terms = any(term in user_lower for term in ['ai agent', 'ai system', 'ai team', 'multi-agent'])
        has_research_terms = any(term in user_lower for term in ['research', 'analysis', 'study', 'identify', 'search'])
        has_market_terms = any(term in user_lower for term in ['market', 'industry', 'profit', 'product', 'business'])
        
        # Debug logging
        logger.info(f"Complex AI detection - Keywords: {keyword_matches}, AI terms: {has_ai_terms}, Research: {has_research_terms}, Market: {has_market_terms}")
        
        # If has AI terms AND (research terms OR market terms) OR high keyword count
        return (has_ai_terms and (has_research_terms or has_market_terms)) or keyword_matches >= 5
    
    def _is_iot_hardware_project(self, user_input: str) -> bool:
        """Detect if project is an IoT/hardware project requiring specialized analysis"""
        iot_keywords = [
            'iot', 'esp32', 'arduino', 'raspberry pi', 'sensor', 'microcontroller',
            'smart home', 'automation', 'monitoring', 'control system',
            'aquarium', 'greenhouse', 'weather station', 'security system',
            'temperature sensor', 'ph sensor', 'ultrasonic', 'relay',
            'wifi module', 'bluetooth', 'mqtt', 'cloud integration'
        ]
        
        hardware_terms = [
            'components', 'pricing', 'wiring', 'circuit', 'pcb',
            'breadboard', 'soldering', 'enclosure', 'power supply'
        ]
        
        user_lower = user_input.lower()
        iot_matches = sum(1 for keyword in iot_keywords if keyword in user_lower)
        hardware_matches = sum(1 for keyword in hardware_terms if keyword in user_lower)
        
        # Check for specific IoT project indicators
        has_iot_terms = any(term in user_lower for term in ['iot', 'esp32', 'arduino', 'sensor', 'smart'])
        has_hardware_terms = any(term in user_lower for term in ['components', 'pricing', 'wiring', 'setup'])
        has_monitoring_terms = any(term in user_lower for term in ['monitoring', 'control', 'tracking', 'automation'])
        
        logger.info(f"IoT detection - IoT keywords: {iot_matches}, Hardware: {hardware_matches}, IoT terms: {has_iot_terms}, Hardware terms: {has_hardware_terms}, Monitoring: {has_monitoring_terms}")
        
        # If has IoT terms AND (hardware terms OR monitoring terms) OR high IoT keyword count
        return (has_iot_terms and (has_hardware_terms or has_monitoring_terms)) or iot_matches >= 3
    
    def _process_complex_ai_project(self, user_input: str) -> Dict:
        """Process complex AI projects using specialized multi-agent coordinator"""
        try:
            logger.info("Starting complex AI project analysis with specialized agents")
            result = self.multi_agent_coordinator.analyze_complex_project(user_input)
            logger.info("Complex AI project analysis completed successfully")
            
            # Ensure proper format for frontend
            if 'roadmap' in result and 'metadata' in result:
                return result
            else:
                # Convert old format to new format
                return {
                    'roadmap': result.get('final_roadmap', result.get('roadmap', str(result))),
                    'metadata': result.get('metadata', {
                        'processing_method': 'complex_ai_coordinator',
                        'timestamp': datetime.now().isoformat()
                    })
                }
        except Exception as e:
            logger.error(f"Error in complex AI project processing: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # Fallback to standard processing
            logger.info("Falling back to standard processing")
            processed_input = self.text_processor.process_input(user_input)
            return self._process_direct_input(processed_input['content'])
    
    def _process_iot_hardware_project(self, user_input: str) -> Dict:
        """Process IoT/hardware projects using specialized IoT coordinator"""
        try:
            logger.info("Starting IoT/hardware project analysis with specialized agents")
            
            # Create IoT-specific coordinator if not exists
            if not hasattr(self, 'iot_coordinator'):
                from specialized_agents import IoTHardwareCoordinator
                self.iot_coordinator = IoTHardwareCoordinator()
            
            result = self.iot_coordinator.analyze_iot_project(user_input)
            logger.info("IoT/hardware project analysis completed successfully")
            
            # Ensure proper format for frontend
            if 'roadmap' in result and 'metadata' in result:
                return result
            else:
                # Convert old format to new format
                return {
                    'roadmap': result.get('final_roadmap', result.get('roadmap', str(result))),
                    'metadata': result.get('metadata', {
                        'processing_method': 'iot_hardware_coordinator',
                        'timestamp': datetime.now().isoformat()
                    })
                }
        except Exception as e:
            logger.error(f"Error in IoT/hardware project processing: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # Fallback to standard processing
            logger.info("Falling back to standard processing")
            processed_input = self.text_processor.process_input(user_input)
            return self._process_direct_input(processed_input['content'])
    
    def _log_workflow_step(self, step_type: str, content: str):
        """Log workflow step for debugging and analysis"""
        step_info = {
            'iteration': self.current_iteration,
            'step_type': step_type,
            'timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'content_preview': content[:200] + "..." if len(content) > 200 else content
        }
        self.workflow_history.append(step_info)
        logger.info(f"Workflow step completed: {step_type} (iteration {self.current_iteration})")
    
    def get_workflow_summary(self) -> Dict[str, any]:
        """Get a summary of the last workflow execution"""
        if not self.workflow_history:
            return {"status": "No workflow executed yet"}
        
        return {
            "total_steps": len(self.workflow_history),
            "iterations_completed": self.current_iteration,
            "steps": [
                {
                    "step": step['step_type'],
                    "iteration": step['iteration'],
                    "content_length": step['content_length']
                }
                for step in self.workflow_history
            ]
        }


class ProjectRefinerAPI:
    """
    Simple API wrapper for the Multi-Agent system
    """
    
    def __init__(self):
        self.orchestrator = MultiAgentOrchestrator()
    
    def refine_project(self, project_description: str) -> str:
        """
        Public API method to refine a project description
        
        Args:
            project_description: User's project requirements and goals
            
        Returns:
            Refined project roadmap as a clean string
        """
        try:
            result = self.orchestrator.process_project_request(project_description)
            return result['roadmap']
        except Exception as e:
            return f"Error processing project: {str(e)}"
    
    def refine_project_detailed(self, project_description: str) -> Dict[str, any]:
        """
        Detailed API method that returns full result with metadata
        
        Args:
            project_description: User's project requirements and goals
            
        Returns:
            Complete result dictionary with roadmap and metadata
        """
        return self.orchestrator.process_project_request(project_description)
