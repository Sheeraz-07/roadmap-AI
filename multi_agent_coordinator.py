"""
Multi-Agent Coordinator for Complex AI System Design
Orchestrates specialized agents for comprehensive project analysis
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import json
from specialized_agents import (
    MarketResearchAgent, 
    TechnicalArchitectAgent, 
    AISpecialistAgent, 
    BusinessStrategyAgent, 
    ImplementationAgent
)

logger = logging.getLogger(__name__)

class MultiAgentCoordinator:
    """Coordinates multiple specialized agents for complex project analysis"""
    
    def __init__(self):
        self.agents = {
            'market_research': MarketResearchAgent(),
            'technical_architect': TechnicalArchitectAgent(),
            'ai_specialist': AISpecialistAgent(),
            'business_strategy': BusinessStrategyAgent(),
            'implementation': ImplementationAgent()
        }
        self.analysis_results = {}
        self.workflow_history = []
    
    def analyze_complex_project(self, project_description: str) -> Dict:
        """Coordinate multiple agents to analyze complex AI projects"""
        
        logger.info("Starting multi-agent complex project analysis")
        start_time = datetime.now()
        
        try:
            # Phase 1: Market Research Analysis
            logger.info("Phase 1: Market Research Agent analyzing opportunity")
            market_result = self.agents['market_research'].analyze_market_opportunity(project_description)
            self.analysis_results['market_research'] = market_result
            self._log_agent_result('market_research', market_result)
            
            # Phase 2: Technical Architecture Design
            logger.info("Phase 2: Technical Architect designing system architecture")
            market_analysis = market_result.get('analysis', '')
            tech_result = self.agents['technical_architect'].design_system_architecture(
                project_description, market_analysis
            )
            self.analysis_results['technical_architect'] = tech_result
            self._log_agent_result('technical_architect', tech_result)
            
            # Phase 3: AI/ML Model Design
            logger.info("Phase 3: AI Specialist designing AI/ML models")
            architecture = tech_result.get('architecture', '')
            ai_result = self.agents['ai_specialist'].design_ai_models(
                project_description, architecture
            )
            self.analysis_results['ai_specialist'] = ai_result
            self._log_agent_result('ai_specialist', ai_result)
            
            # Phase 4: Business Strategy Development
            logger.info("Phase 4: Business Strategy Agent developing strategy")
            business_result = self.agents['business_strategy'].develop_business_strategy(
                project_description, market_analysis, architecture
            )
            self.analysis_results['business_strategy'] = business_result
            self._log_agent_result('business_strategy', business_result)
            
            # Phase 5: Implementation Planning
            logger.info("Phase 5: Implementation Agent creating execution plan")
            implementation_result = self.agents['implementation'].create_implementation_plan(
                self.analysis_results
            )
            self.analysis_results['implementation'] = implementation_result
            self._log_agent_result('implementation', implementation_result)
            
            # Generate comprehensive roadmap
            final_roadmap = self._synthesize_comprehensive_roadmap()
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            logger.info("Multi-agent complex project analysis completed successfully")
            
            return {
                'roadmap': final_roadmap,
                'metadata': {
                    'processing_type': 'multi_agent_complex',
                    'agents_used': list(self.agents.keys()),
                    'processing_time': processing_time,
                    'timestamp': datetime.now().isoformat(),
                    'total_tokens': self._estimate_total_tokens(),
                    'confidence_scores': self._get_confidence_scores()
                },
                'agent_analyses': self.analysis_results,
                'workflow_history': self.workflow_history
            }
            
        except Exception as e:
            logger.error(f"Error in multi-agent complex analysis: {str(e)}")
            raise Exception(f"Multi-agent complex analysis failed: {str(e)}")
    
    def _synthesize_comprehensive_roadmap(self) -> str:
        """Synthesize all agent analyses into a comprehensive roadmap"""
        
        roadmap_sections = []
        
        # Executive Summary with enhanced formatting
        roadmap_sections.append("# 🚀 AI Market Research System: Comprehensive Project Roadmap")
        roadmap_sections.append("")
        roadmap_sections.append("## 📋 Executive Summary")
        roadmap_sections.append("This roadmap presents a **comprehensive plan** for developing an advanced AI-powered market research system with specialized multi-agent architecture for identifying untapped market opportunities and generating profitable business ideas.")
        roadmap_sections.append("")
        roadmap_sections.append("---")
        roadmap_sections.append("")
        
        # Market Opportunity Analysis with better structure
        if 'market_research' in self.analysis_results:
            market_data = self.analysis_results['market_research']
            if 'analysis' in market_data:
                roadmap_sections.append("## 📊 Market Opportunity Analysis")
                roadmap_sections.append("")
                # Format the market analysis content better
                market_content = market_data['analysis']
                formatted_content = self._format_section_content(market_content, "Market Analysis")
                roadmap_sections.append(formatted_content)
                roadmap_sections.append("")
                roadmap_sections.append("---")
                roadmap_sections.append("")
        
        # Technical Architecture with enhanced presentation
        if 'technical_architect' in self.analysis_results:
            tech_data = self.analysis_results['technical_architect']
            if 'architecture' in tech_data:
                roadmap_sections.append("## 🏗️ Technical Architecture & System Design")
                roadmap_sections.append("")
                tech_content = tech_data['architecture']
                formatted_content = self._format_section_content(tech_content, "Technical Architecture")
                roadmap_sections.append(formatted_content)
                roadmap_sections.append("")
                roadmap_sections.append("---")
                roadmap_sections.append("")
        
        # AI/ML Model Design with better formatting
        if 'ai_specialist' in self.analysis_results:
            ai_data = self.analysis_results['ai_specialist']
            if 'ai_design' in ai_data:
                roadmap_sections.append("## 🤖 AI/ML Models & Algorithms")
                roadmap_sections.append("")
                ai_content = ai_data['ai_design']
                formatted_content = self._format_section_content(ai_content, "AI/ML Design")
                roadmap_sections.append(formatted_content)
                roadmap_sections.append("")
                roadmap_sections.append("---")
                roadmap_sections.append("")
        
        # Business Strategy with enhanced structure
        if 'business_strategy' in self.analysis_results:
            business_data = self.analysis_results['business_strategy']
            if 'strategy' in business_data:
                roadmap_sections.append("## 💼 Business Strategy & Monetization")
                roadmap_sections.append("")
                business_content = business_data['strategy']
                formatted_content = self._format_section_content(business_content, "Business Strategy")
                roadmap_sections.append(formatted_content)
                roadmap_sections.append("")
                roadmap_sections.append("---")
                roadmap_sections.append("")
                roadmap_sections.append("")
        
        # Implementation Plan with enhanced formatting
        if 'implementation' in self.analysis_results:
            impl_data = self.analysis_results['implementation']
            if 'implementation_plan' in impl_data:
                roadmap_sections.append("## 🎯 Implementation Plan & Execution")
                roadmap_sections.append("")
                impl_content = impl_data['implementation_plan']
                formatted_content = self._format_section_content(impl_content, "Implementation Plan")
                roadmap_sections.append(formatted_content)
                roadmap_sections.append("")
                roadmap_sections.append("---")
                roadmap_sections.append("")
        
        # Multi-Agent System Summary with enhanced presentation
        roadmap_sections.append("## 🤖 Multi-Agent System Architecture Summary")
        roadmap_sections.append("")
        roadmap_sections.append("### 🎯 **Specialized Agent Roles:**")
        roadmap_sections.append("")
        roadmap_sections.append("| Agent | Primary Function | Key Capabilities |")
        roadmap_sections.append("|-------|------------------|------------------|")
        roadmap_sections.append("| 📊 **Market Research Agent** | Market Intelligence | Scans global markets, identifies trends, analyzes gaps |")
        roadmap_sections.append("| 🏗️ **Technical Architect Agent** | System Design | Designs scalable architecture and infrastructure |")
        roadmap_sections.append("| 🤖 **AI Specialist Agent** | ML/AI Development | Develops and optimizes machine learning models |")
        roadmap_sections.append("| 💼 **Business Strategy Agent** | Strategic Planning | Creates monetization and go-to-market strategies |")
        roadmap_sections.append("| 🎯 **Implementation Agent** | Project Execution | Coordinates development, deployment, and operations |")
        roadmap_sections.append("")
        roadmap_sections.append("### 🔄 **Agent Coordination Workflow:**")
        roadmap_sections.append("")
        roadmap_sections.append("```mermaid")
        roadmap_sections.append("graph TD")
        roadmap_sections.append("    A[Daily Market Scanning] --> B[Data Analysis & Processing]")
        roadmap_sections.append("    B --> C[Opportunity Identification]")
        roadmap_sections.append("    C --> D[Feasibility Assessment]")
        roadmap_sections.append("    D --> E[Business Validation]")
        roadmap_sections.append("    E --> F[Idea Generation & Ranking]")
        roadmap_sections.append("    F --> G[Implementation Planning]")
        roadmap_sections.append("    G --> H[Continuous Learning Loop]")
        roadmap_sections.append("    H --> A")
        roadmap_sections.append("```")
        roadmap_sections.append("")
        roadmap_sections.append("### 📈 **Success Metrics & KPIs:**")
        roadmap_sections.append("")
        roadmap_sections.append("| Metric Category | Key Indicators | Target Performance |")
        roadmap_sections.append("|-----------------|----------------|-------------------|")
        roadmap_sections.append("| 💡 **Idea Quality** | Market potential, uniqueness, feasibility scores | 8.5+ out of 10 |")
        roadmap_sections.append("| 🚀 **Implementation Success** | Conversion rate from idea to profitable product | 60%+ success rate |")
        roadmap_sections.append("| 🎯 **Market Accuracy** | Prediction accuracy for trends and opportunities | 85%+ accuracy |")
        roadmap_sections.append("| 💰 **Revenue Generation** | ROI from implemented ideas and products | $10M+ ARR target |")
        roadmap_sections.append("")
        roadmap_sections.append("---")
        roadmap_sections.append("")
        roadmap_sections.append("## 🎉 **Project Completion Summary**")
        roadmap_sections.append("")
        roadmap_sections.append("This comprehensive roadmap provides a **complete blueprint** for building a sophisticated AI-driven market research and opportunity identification system. The multi-agent architecture ensures:")
        roadmap_sections.append("")
        roadmap_sections.append("✅ **Comprehensive Analysis** across all business domains")
        roadmap_sections.append("✅ **Scalable Architecture** for enterprise-grade deployment")
        roadmap_sections.append("✅ **Advanced AI/ML Models** for accurate predictions")
        roadmap_sections.append("✅ **Profitable Business Model** with multiple revenue streams")
        roadmap_sections.append("✅ **Clear Implementation Path** with defined milestones")
        roadmap_sections.append("")
        roadmap_sections.append("**Ready for implementation with high potential for market success!** 🚀")
        
        return "\n".join(roadmap_sections)
    
    def _format_section_content(self, content: str, section_type: str) -> str:
        """Format section content with better structure and readability"""
        if not content:
            return content
            
        # Add proper spacing and structure
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("")
                continue
                
            # Convert headers to proper markdown
            if line.startswith('####'):
                formatted_lines.append(f"### {line[4:].strip()}")
            elif line.startswith('###'):
                formatted_lines.append(f"### {line[3:].strip()}")
            elif line.startswith('##'):
                formatted_lines.append(f"### {line[2:].strip()}")
            elif line.startswith('#'):
                formatted_lines.append(f"### {line[1:].strip()}")
            else:
                # Add bullet points for list items
                if line.startswith('- ') or line.startswith('* '):
                    formatted_lines.append(line)
                elif line.endswith(':') and len(line) < 100:
                    formatted_lines.append(f"**{line}**")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _log_agent_result(self, agent_name: str, result: Dict):
        """Log agent analysis result"""
        workflow_entry = {
            'agent': agent_name,
            'timestamp': datetime.now().isoformat(),
            'success': 'error' not in result,
            'confidence': result.get('confidence', 0.0),
            'content_length': len(str(result))
        }
        self.workflow_history.append(workflow_entry)
        
        if 'error' in result:
            logger.error(f"Agent {agent_name} failed: {result['error']}")
        else:
            logger.info(f"Agent {agent_name} completed successfully (confidence: {result.get('confidence', 'N/A')})")
    
    def _estimate_total_tokens(self) -> int:
        """Estimate total tokens used across all agents"""
        total_tokens = 0
        for agent_result in self.analysis_results.values():
            # Rough estimation: ~4 characters per token
            content_length = len(str(agent_result))
            total_tokens += content_length // 4
        return total_tokens
    
    def _get_confidence_scores(self) -> Dict:
        """Get confidence scores from all agents"""
        confidence_scores = {}
        for agent_name, result in self.analysis_results.items():
            confidence_scores[agent_name] = result.get('confidence', 0.0)
        return confidence_scores
