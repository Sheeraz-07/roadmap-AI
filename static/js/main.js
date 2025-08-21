// Main JavaScript for AI Project Refiner
class ProjectRefinerApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.examples = this.getExamples();
    }

    initializeElements() {
        this.projectInput = document.getElementById('projectInput');
        this.generateBtn = document.getElementById('generateBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        
        this.resultsSection = document.getElementById('resultsSection');
        this.roadmapContainer = document.getElementById('roadmapContainer');
        this.loadingContainer = document.getElementById('loadingContainer');
        this.errorContainer = document.getElementById('errorContainer');
        this.processingInfo = document.getElementById('processingInfo');
        
        // Progress elements
        this.progressSection = document.getElementById('progressSection');
        this.progressBar = document.getElementById('progressBar');
        this.progressPercentage = document.getElementById('progressPercentage');
        this.progressTitle = document.getElementById('progressTitle');
        this.progressStatus = document.getElementById('progressStatus');
        
        this.roadmapContent = document.getElementById('roadmapContent');
        this.errorText = document.getElementById('errorText');
        
        this.processingType = document.getElementById('processingType');
        this.totalTokens = document.getElementById('totalTokens');
        this.processingTime = document.getElementById('processingTime');
        
        this.exampleCards = document.querySelectorAll('.example-card');
    }

    bindEvents() {
        this.generateBtn.addEventListener('click', () => this.generateRoadmap());
        this.downloadBtn.addEventListener('click', () => this.downloadRoadmap());
        
        // Make roadmap content clickable for download
        this.roadmapContent.addEventListener('click', () => this.downloadRoadmap());
        
        this.exampleCards.forEach(card => {
            card.addEventListener('click', () => {
                const exampleType = card.getAttribute('data-example');
                this.loadExample(exampleType);
            });
        });

        // Auto-resize textarea
        this.projectInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
    }

    getExamples() {
        return {
            mobile: `Build a social media mobile app with the following features:
- User authentication and profiles with photo uploads
- Photo and video sharing with filters and editing tools
- Real-time messaging and group chats
- Stories feature with 24-hour expiration
- Push notifications for likes, comments, and messages
- Social feed with algorithmic content recommendation
- Privacy controls and content moderation

Technical Requirements:
- Native iOS and Android apps
- Real-time synchronization
- Cloud storage for media files
- End-to-end encryption for messages
- Offline capability for viewing cached content

Budget: $75,000
Timeline: 8 months
Team: 3 developers (2 mobile, 1 backend), 1 UI/UX designer
Target: 50,000 active users in first year`,

            web: `Create a comprehensive e-learning platform with:
- Course management system for instructors
- Video streaming with adaptive quality
- Interactive quizzes and assignments
- Progress tracking and analytics
- Certificate generation and verification
- Payment processing for course purchases
- Discussion forums and Q&A sections
- Mobile-responsive design
- Multi-language support

Advanced Features:
- AI-powered content recommendations
- Live streaming for webinars
- Integration with popular LMS systems
- White-label solutions for institutions
- Advanced reporting and analytics

Budget: $100,000
Timeline: 10 months
Team: 4 developers, 2 designers, 1 project manager
Target: 10,000 registered users, 500 courses`,

            ai: `Develop an AI-powered customer service chatbot system with:
- Natural Language Processing for intent recognition
- Multi-language support (English, Spanish, French, German)
- Integration with existing CRM systems (Salesforce, HubSpot)
- Real-time analytics and conversation insights
- Escalation to human agents when needed
- Knowledge base management and training
- Voice recognition and text-to-speech capabilities
- Sentiment analysis and customer satisfaction tracking

Technical Requirements:
- Enterprise-grade security and compliance
- API-first architecture for easy integration
- Cloud deployment with auto-scaling
- 99.9% uptime SLA
- GDPR and data privacy compliance
- Custom training on company-specific data

Budget: $150,000
Timeline: 12 months
Team: 3 AI/ML engineers, 2 backend developers, 1 DevOps engineer
Target: Handle 10,000+ conversations per day`
        };
    }

    loadExample(exampleType) {
        if (this.examples[exampleType]) {
            this.projectInput.value = this.examples[exampleType];
            this.autoResizeTextarea();
            this.hideAllSections();
        }
    }

    autoResizeTextarea() {
        this.projectInput.style.height = 'auto';
        this.projectInput.style.height = Math.max(300, this.projectInput.scrollHeight) + 'px';
    }

    updateProgress(percentage, title, status) {
        this.progressBar.style.width = `${percentage}%`;
        this.progressPercentage.textContent = `${percentage}%`;
        this.progressTitle.textContent = title;
        this.progressStatus.textContent = status;
    }

    showProgress() {
        this.progressSection.style.display = 'block';
        this.generateBtn.disabled = true;
        this.generateBtn.querySelector('.btn-text').textContent = 'Processing...';
    }

    hideProgress() {
        this.progressSection.style.display = 'none';
        this.generateBtn.disabled = false;
        this.generateBtn.querySelector('.btn-text').textContent = 'Generate AI Roadmap';
    }

    simulateProgress() {
        const steps = [
            { percentage: 15, title: 'Initializing AI Agents', status: 'Setting up Strategist and Refiner agents...' },
            { percentage: 30, title: 'Analyzing Project Requirements', status: 'Processing your project description...' },
            { percentage: 50, title: 'Strategist Creating Initial Roadmap', status: 'GPT-4 generating comprehensive project plan...' },
            { percentage: 70, title: 'Refiner Analyzing Roadmap', status: 'Gemini analyzing and optimizing structure...' },
            { percentage: 85, title: 'Final Refinement', status: 'Applying improvements and formatting...' },
            { percentage: 95, title: 'Finalizing Results', status: 'Preparing your refined roadmap...' }
        ];

        let currentStep = 0;
        const progressInterval = setInterval(() => {
            if (currentStep < steps.length) {
                const step = steps[currentStep];
                this.updateProgress(step.percentage, step.title, step.status);
                currentStep++;
            } else {
                clearInterval(progressInterval);
            }
        }, 2000); // Update every 2 seconds for better visibility

        return progressInterval;
    }


    async generateRoadmap() {
        const projectDescription = this.projectInput.value.trim();
        
        if (!projectDescription) {
            this.showError('Please provide a project description');
            return;
        }

        this.hideAllSections();
        this.showProgress();
        
        // Start progress simulation
        const progressInterval = this.simulateProgress();

        try {
            console.log('Sending request to /api/refine-project');
            console.log('Project description:', projectDescription);
            
            const response = await fetch('/api/refine-project', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    project_description: projectDescription,
                    detailed: true
                }),
                timeout: 300000 // 5 minute timeout
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('HTTP error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log('Response result:', result);
            
            if (result.error) {
                console.error('API returned error:', result.error);
                throw new Error(result.error);
            }

            // Complete progress
            clearInterval(progressInterval);
            this.updateProgress(100, 'Complete!', 'Your AI-generated roadmap is ready');
            
            setTimeout(() => {
                this.hideProgress();
                this.showRoadmap(result.roadmap, result.metadata);
            }, 1000);
            
        } catch (error) {
            console.error('Full error details:', error);
            console.error('Error stack:', error.stack);
            clearInterval(progressInterval);
            this.hideProgress();
            
            // More detailed error messages
            let errorMessage = 'Failed to generate roadmap: ';
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage += 'Network connection failed. Please check if the server is running.';
            } else if (error.message.includes('timeout')) {
                errorMessage += 'Request timed out. The AI processing is taking longer than expected.';
            } else {
                errorMessage += error.message;
            }
            
            this.showError(errorMessage);
        }
    }

    showRoadmap(roadmap, metadata) {
        this.roadmapContent.innerHTML = this.markdownToHtml(roadmap);
        this.roadmapContainer.style.display = 'block';
        this.resultsSection.style.display = 'block';
        
        // Show download button with animation
        setTimeout(() => {
            this.downloadBtn.style.display = 'flex';
            this.downloadBtn.style.animation = 'slideInRight 0.5s ease-out';
        }, 500);
        
        if (metadata) {
            this.processingType.textContent = metadata.processing_type || 'Standard';
            this.totalTokens.textContent = (metadata.total_tokens || 0).toLocaleString();
            this.processingTime.textContent = `${metadata.processing_time || 0}s`;
            this.processingInfo.style.display = 'block';
        }

        // Store roadmap for download
        this.currentRoadmap = roadmap;
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showLoading(message = 'Processing...') {
        this.loadingContainer.querySelector('p').textContent = message;
        this.loadingContainer.style.display = 'block';
    }

    hideLoading() {
        this.loadingContainer.style.display = 'none';
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorContainer.style.display = 'block';
        this.resultsSection.style.display = 'block';
    }

    hideAllSections() {
        this.resultsSection.style.display = 'none';
        this.roadmapContainer.style.display = 'none';
        this.loadingContainer.style.display = 'none';
        this.errorContainer.style.display = 'none';
        this.processingInfo.style.display = 'none';
        this.progressSection.style.display = 'none';
        this.downloadBtn.style.display = 'none';
    }

    downloadRoadmap() {
        if (!this.currentRoadmap) {
            this.showError('No roadmap available for download');
            return;
        }

        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
        const filename = `project_roadmap_${timestamp}.txt`;
        
        const blob = new Blob([this.currentRoadmap], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        // Show download confirmation
        this.showDownloadConfirmation();
    }

    showDownloadConfirmation() {
        const confirmation = document.createElement('div');
        confirmation.className = 'download-confirmation';
        confirmation.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>Roadmap downloaded successfully!</span>
        `;
        
        document.body.appendChild(confirmation);
        
        setTimeout(() => {
            confirmation.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            confirmation.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(confirmation);
            }, 300);
        }, 3000);
    }

    markdownToHtml(markdown) {
        // Simple markdown to HTML conversion
        let html = markdown
            // Headers
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            // Bold
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            // Italic
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            // Code blocks
            .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
            // Inline code
            .replace(/`([^`]*)`/gim, '<code>$1</code>')
            // Lists
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            .replace(/^\* (.*$)/gim, '<li>$1</li>')
            // Line breaks
            .replace(/\n\n/gim, '</p><p>')
            .replace(/\n/gim, '<br>');

        // Wrap consecutive <li> elements in <ul>
        html = html.replace(/(<li>.*<\/li>)/gims, '<ul>$1</ul>');
        html = html.replace(/<\/ul>\s*<ul>/gim, '');

        // Wrap in paragraphs
        if (!html.startsWith('<h') && !html.startsWith('<ul') && !html.startsWith('<pre')) {
            html = '<p>' + html + '</p>';
        }

        return html;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProjectRefinerApp();
});
