# Multi-Agent Project Refiner AI System

A sophisticated AI system that uses **GPT-4.1** and **Google Gemini** in collaboration to create comprehensive, refined project roadmaps from user requirements.

## 🎯 System Overview

This system implements a **multi-agent architecture** where two specialized LLMs work together through an iterative refinement process:

- **Strategist (GPT-4.1)**: Creates initial high-level project roadmaps and strategic analysis
- **Refiner (Gemini)**: Provides critical evaluation, identifies weaknesses, and suggests improvements

## 🏗️ Architecture

### Core Components

1. **Multi-Agent Orchestrator** (`multi_agent_orchestrator.py`)
   - Manages the 3-iteration workflow between agents
   - Handles large input processing and chunking
   - Coordinates the feedback loop

2. **LLM Agents** (`llm_agents.py`)
   - `StrategistAgent`: GPT-4.1 for strategic planning
   - `RefinerAgent`: Gemini for critical analysis and refinement

3. **Text Processor** (`text_processor.py`)
   - Handles large inputs through intelligent chunking
   - Maintains context with overlapping segments
   - Summarizes content for processing

4. **Web Interface** (`streamlit_app.py`)
   - User-friendly Streamlit interface
   - Real-time processing with progress indicators
   - Download functionality for generated roadmaps

## 🔄 Workflow Process

### 3-Iteration Refinement Loop

1. **Iteration 1**: Strategist analyzes requirements → Creates initial roadmap
2. **Iteration 2**: Refiner evaluates roadmap → Provides detailed feedback
3. **Iteration 3**: Strategist integrates feedback → Creates refined roadmap
4. **Final**: Refiner polishes and formats → Delivers final roadmap

### Large Input Handling

- **Chunking**: Splits large inputs into manageable segments with overlap
- **Summarization**: Extracts key points for context preservation
- **Token Management**: Optimizes processing within model limits

## 🚀 Quick Start

### 1. Installation

```bash
# Activate virtual environment
venv11/Scripts/Activate

# Install dependencies
python -m pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run Web Interface

```bash
streamlit run streamlit_app.py
```

### 4. Programmatic Usage

```python
from multi_agent_orchestrator import ProjectRefinerAPI

# Initialize API
api = ProjectRefinerAPI()

# Process project description
roadmap = api.refine_project(your_project_description)
print(roadmap)
```

## 📋 Usage Examples

### Web Interface
1. Open the Streamlit app
2. Enter your API keys in the sidebar
3. Describe your project requirements
4. Click "Generate Refined Roadmap"
5. Download the result as a markdown file

### Command Line
```bash
python example_usage.py
```

## 🔧 Configuration Options

### Model Settings (`config.py`)
- **GPT Model**: `gpt-4-turbo-preview` (GPT-4.1)
- **Gemini Model**: `gemini-pro` (Free tier)
- **Max Iterations**: 3 rounds of refinement
- **Chunk Size**: 3000 characters for large inputs

### Temperature Settings
- **Strategist**: 0.7 (balanced creativity/consistency)
- **Refiner**: 0.8 (higher creativity for alternatives)

## 📊 Features

### ✅ Core Capabilities
- **Multi-agent collaboration** between GPT-4.1 and Gemini
- **Large input processing** with intelligent chunking
- **3-iteration refinement** for optimal results
- **Web interface** with real-time processing
- **Downloadable roadmaps** in markdown format
- **Detailed metadata** and processing insights

### ✅ Input Handling
- **Direct processing** for inputs under 2000 tokens
- **Chunked processing** for larger inputs
- **Context preservation** through overlapping segments
- **Key point extraction** for summaries

### ✅ Output Quality
- **Comprehensive roadmaps** with clear structure
- **Executive summaries** and implementation details
- **Risk assessments** and mitigation strategies
- **Timeline estimates** and resource allocation
- **Clean formatting** without technical jargon

## 🔒 Security & Best Practices

- **Environment variables** for API key management
- **Error handling** with graceful degradation
- **Logging** for debugging and monitoring
- **Token optimization** to minimize costs

## 📁 Project Structure

```
project_refiner_ai_agent/
├── config.py                    # Configuration settings
├── text_processor.py           # Large input handling
├── llm_agents.py              # GPT-4.1 and Gemini agents
├── multi_agent_orchestrator.py # Main workflow orchestrator
├── streamlit_app.py           # Web interface
├── example_usage.py           # Usage examples
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🛠️ API Reference

### ProjectRefinerAPI

```python
# Simple usage
roadmap = api.refine_project(project_description)

# Detailed usage with metadata
result = api.refine_project_detailed(project_description)
# Returns: {'roadmap': str, 'metadata': dict}
```

### Metadata Structure
```python
{
    'processing_type': 'direct' | 'chunked',
    'total_tokens': int,
    'iterations_completed': int,
    'processing_time': float,
    'timestamp': str
}
```

## 🎯 Use Cases

- **Startup Planning**: Transform business ideas into actionable roadmaps
- **Software Development**: Plan complex technical projects
- **Product Management**: Create comprehensive product development plans
- **Consulting**: Generate detailed project proposals
- **Research Projects**: Structure academic and R&D initiatives

## 🤝 Contributing

This system is designed to be extensible. Key areas for enhancement:
- Additional LLM integrations
- Custom refinement strategies
- Industry-specific templates
- Advanced output formatting

## 📄 License

This project is designed for educational and commercial use. Please ensure compliance with OpenAI and Google API terms of service.

---

**Built with ❤️ using GPT-4.1 and Google Gemini**
