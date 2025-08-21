"""
Vercel-compatible Flask application for AI Project Refiner
"""
import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Get the directory containing this file (api/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
parent_dir = os.path.dirname(current_dir)
# Add to Python path
sys.path.insert(0, parent_dir)

# Debug logging for import paths
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Current directory: {current_dir}")
logger.info(f"Parent directory: {parent_dir}")
logger.info(f"Python path: {sys.path[:3]}")

try:
    from multi_agent_orchestrator import ProjectRefinerAPI
    logger.info("Successfully imported ProjectRefinerAPI")
except ImportError as e:
    logger.error(f"Failed to import ProjectRefinerAPI: {e}")
    try:
        # Try alternative import paths
        import multi_agent_orchestrator
        ProjectRefinerAPI = multi_agent_orchestrator.ProjectRefinerAPI
        logger.info("Successfully imported via alternative path")
    except Exception as e2:
        logger.error(f"Alternative import also failed: {e2}")
        ProjectRefinerAPI = None

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Initialize the Project Refiner API
try:
    if ProjectRefinerAPI:
        project_api = ProjectRefinerAPI()
        logger.info("Project Refiner API initialized successfully")
    else:
        project_api = None
        logger.error("ProjectRefinerAPI class not available")
except Exception as e:
    logger.error(f"Failed to initialize Project Refiner API: {str(e)}")
    project_api = None

@app.route('/')
def index():
    """Render the main interface"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_status': 'initialized' if project_api else 'failed'
    })

@app.route('/api/refine-project', methods=['POST'])
def refine_project():
    """Process project refinement request"""
    try:
        if not project_api:
            return jsonify({'error': 'Project Refiner API not initialized'}), 500
        
        data = request.get_json()
        if not data or 'project_description' not in data:
            return jsonify({'error': 'Missing project_description in request'}), 400
        
        project_description = data['project_description']
        detailed = data.get('detailed', False)
        
        logger.info(f"Processing project refinement request (detailed: {detailed})")
        
        if detailed:
            result = project_api.refine_project_detailed(project_description)
        else:
            roadmap = project_api.refine_project(project_description)
            result = {
                'roadmap': roadmap,
                'metadata': {
                    'processing_type': 'standard',
                    'timestamp': datetime.now().isoformat()
                }
            }
        
        logger.info("Project refinement completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing project refinement: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

# Export the Flask app for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
