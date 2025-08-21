"""
Flask web application for the AI Project Refiner
Modern HTML/CSS interface replacing Streamlit
"""
from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime
from multi_agent_orchestrator import ProjectRefinerAPI

# Configure comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project_refiner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the Project Refiner API
try:
    project_api = ProjectRefinerAPI()
    logger.info("Project Refiner API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Project Refiner API: {str(e)}")
    project_api = None

@app.route('/')
def index():
    """Serve the main HTML interface"""
    from flask import make_response
    response = make_response(render_template('index_new.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/refine-project', methods=['POST'])
def refine_project():
    """API endpoint to refine project descriptions"""
    try:
        logger.debug("Received project refinement request")
        
        # Check if API is available
        if project_api is None:
            logger.error("Project Refiner API is not available")
            return jsonify({
                'error': 'Project Refiner API not available. Please check your API keys in .env file.'
            }), 500

        # Get request data
        data = request.get_json()
        logger.debug(f"Request data: {data}")
        
        if not data or 'project_description' not in data:
            logger.error("Missing project_description in request")
            return jsonify({
                'error': 'Missing project_description in request'
            }), 400

        project_description = data['project_description'].strip()
        if not project_description:
            logger.error("Project description is empty")
            return jsonify({
                'error': 'Project description cannot be empty'
            }), 400

        detailed = data.get('detailed', False)
        
        logger.info(f"Processing project refinement request (detailed: {detailed})")
        logger.debug(f"Project description: {project_description[:100]}...")
        
        # Process the project
        if detailed:
            logger.debug("Processing detailed project refinement")
            result = project_api.refine_project_detailed(project_description)
            logger.info("Detailed project refinement completed successfully")
            return jsonify(result)
        else:
            logger.debug("Processing standard project refinement")
            roadmap = project_api.refine_project(project_description)
            logger.info("Standard project refinement completed successfully")
            return jsonify({
                'roadmap': roadmap,
                'metadata': {
                    'processing_type': 'standard',
                    'timestamp': datetime.now().isoformat()
                }
            })

    except Exception as e:
        logger.error(f"Error processing project refinement: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'Failed to process project: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check if API keys are configured
        from config import Config
        Config.validate_config()
        api_status = "configured"
    except Exception as e:
        api_status = f"error: {str(e)}"
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_status': api_status,
        'project_api_available': project_api is not None
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if running in development mode
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    logger.info(f"Starting Flask application on port {port} (debug: {debug_mode})")
    
    # Print startup information
    print("🤖 AI Project Refiner - Web Interface")
    print("=" * 50)
    print(f"🌐 Server starting on: http://localhost:{port}")
    print("📁 Static files: /static/")
    print("📄 Templates: /templates/")
    print("🔧 API endpoint: /api/refine-project")
    print("❤️  Health check: /api/health")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )
