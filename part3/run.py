#!/usr/bin/env python3
"""
HBnB Application Runner
This script starts the HBnB Flask application
"""

import os
import sys
from api.app import create_app

def main():
    """Main function to run the application"""
    try:
        # Get environment from command line or environment variable
        if len(sys.argv) > 1:
            env = sys.argv[1]
        else:
            env = os.getenv('FLASK_ENV', 'development')
        
        # Validate environment
        valid_envs = ['development', 'testing', 'production']
        if env not in valid_envs:
            print(f"Error: Invalid environment '{env}'. Valid options: {valid_envs}")
            sys.exit(1)
        
        print(f"Starting HBnB application in {env} mode...")
        
        # Create the Flask application
        app = create_app(env)
        
        # Configuration based on environment
        if env == 'development':
            # Development configuration
            app.run(
                debug=True,
                host='0.0.0.0',
                port=int(os.getenv('PORT', 5000)),
                use_reloader=True
            )
        elif env == 'testing':
            # Testing configuration
            app.run(
                debug=True,
                host='127.0.0.1',
                port=int(os.getenv('PORT', 5001)),
                use_reloader=False
            )
        else:
            # Production configuration
            app.run(
                debug=False,
                host='0.0.0.0',
                port=int(os.getenv('PORT', 8000)),
                use_reloader=False
            )
            
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Make sure all dependencies are installed and paths are correct.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

# Simple version - uncomment if you prefer this approach
"""
if __name__ == '__main__':
    from api.app import create_app
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

if __name__ == '__main__':
    main()
