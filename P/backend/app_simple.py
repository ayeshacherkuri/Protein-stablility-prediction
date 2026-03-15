"""
Simplified Flask Application for Protein Stability Prediction API
Uses a simple model instead of TensorFlow for demonstration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from preprocess import ProteinPreprocessor
from simple_model import SimpleProteinStabilityModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model and preprocessor
model = None
preprocessor = None

def load_model():
    """
    Load the simple model and preprocessor
    """
    global model, preprocessor
    
    try:
        # Initialize preprocessor
        preprocessor = ProteinPreprocessor(max_length=500)
        
        # Initialize simple model
        model = SimpleProteinStabilityModel()
        
        # Mark model as trained
        model.is_trained = True
        
        logger.info("Simple model and preprocessor initialized successfully")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

@app.route('/')
def home():
    """
    Home endpoint with API information
    """
    return jsonify({
        'message': 'Protein Stability Prediction API (Simple Model)',
        'version': '1.0.0',
        'endpoints': {
            '/predict': 'POST - Predict protein stability',
            '/health': 'GET - Health check'
        },
        'usage': {
            'method': 'POST',
            'url': '/predict',
            'body': {
                'sequence': 'MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG'
            },
            'response': {
                'stability_score': -8.5,
                'classification': 'Stable',
                'confidence': 0.92
            }
        }
    })

@app.route('/health')
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'preprocessor_loaded': preprocessor is not None,
        'model_type': 'simple_heuristic'
    })

@app.route('/predict', methods=['POST'])
def predict_stability():
    """
    Predict protein stability from amino acid sequence
    
    Expected JSON input:
    {
        "sequence": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    }
    
    Returns:
    {
        "stability_score": -8.5,
        "classification": "Stable",
        "confidence": 0.92,
        "sequence_length": 51,
        "features": {
            "hydrophobic_count": 15,
            "charged_count": 8,
            "polar_count": 12
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'sequence' not in data:
            return jsonify({
                'error': 'Missing sequence in request body'
            }), 400
        
        sequence = data['sequence'].strip()
        
        # Validate sequence
        if not sequence:
            return jsonify({
                'error': 'Empty sequence provided'
            }), 400
        
        if not preprocessor.validate_sequence(sequence):
            return jsonify({
                'error': 'Invalid amino acid sequence. Only standard amino acids (ACDEFGHIKLMNPQRSTVWY) are allowed.'
            }), 400
        
        # Check sequence length
        if len(sequence) > 500:
            return jsonify({
                'error': 'Sequence too long. Maximum length is 500 amino acids.'
            }), 400
        
        # Encode sequence
        encoded_sequence = preprocessor.encode_sequence(sequence)
        encoded_batch = np.expand_dims(encoded_sequence, axis=0)
        
        # Make prediction
        stability_score, classification = model.predict(encoded_batch)
        
        # Get classification label
        class_label = "Stable" if classification[0] == 0 else "Unstable"
        
        # Calculate confidence (simplified - based on score magnitude)
        confidence = min(0.95, max(0.5, abs(stability_score[0]) / 10))
        
        # Get sequence features
        features = preprocessor.get_sequence_features(sequence)
        
        # Prepare response
        response = {
            'stability_score': float(stability_score[0]),
            'classification': class_label,
            'confidence': float(confidence),
            'sequence_length': len(sequence),
            'features': {
                'hydrophobic_count': features['hydrophobic_count'],
                'charged_count': features['charged_count'],
                'polar_count': features['polar_count']
            }
        }
        
        logger.info(f"Prediction completed for sequence of length {len(sequence)}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({
            'error': 'Internal server error during prediction'
        }), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    Predict protein stability for multiple sequences
    
    Expected JSON input:
    {
        "sequences": [
            "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
            "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"
        ]
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'sequences' not in data:
            return jsonify({
                'error': 'Missing sequences in request body'
            }), 400
        
        sequences = data['sequences']
        
        if not isinstance(sequences, list) or len(sequences) == 0:
            return jsonify({
                'error': 'Sequences must be a non-empty list'
            }), 400
        
        if len(sequences) > 100:
            return jsonify({
                'error': 'Too many sequences. Maximum batch size is 100.'
            }), 400
        
        results = []
        
        for i, sequence in enumerate(sequences):
            try:
                sequence = sequence.strip()
                
                # Validate sequence
                if not sequence:
                    results.append({
                        'index': i,
                        'error': 'Empty sequence'
                    })
                    continue
                
                if not preprocessor.validate_sequence(sequence):
                    results.append({
                        'index': i,
                        'error': 'Invalid amino acid sequence'
                    })
                    continue
                
                if len(sequence) > 500:
                    results.append({
                        'index': i,
                        'error': 'Sequence too long'
                    })
                    continue
                
                # Encode sequence
                encoded_sequence = preprocessor.encode_sequence(sequence)
                encoded_batch = np.expand_dims(encoded_sequence, axis=0)
                
                # Make prediction
                stability_score, classification = model.predict(encoded_batch)
                
                # Get classification label
                class_label = "Stable" if classification[0] == 0 else "Unstable"
                
                # Calculate confidence
                confidence = min(0.95, max(0.5, abs(stability_score[0]) / 10))
                
                # Get sequence features
                features = preprocessor.get_sequence_features(sequence)
                
                results.append({
                    'index': i,
                    'stability_score': float(stability_score[0]),
                    'classification': class_label,
                    'confidence': float(confidence),
                    'sequence_length': len(sequence),
                    'features': {
                        'hydrophobic_count': features['hydrophobic_count'],
                        'charged_count': features['charged_count'],
                        'polar_count': features['polar_count']
                    }
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'error': f'Prediction failed: {str(e)}'
                })
        
        return jsonify({
            'results': results,
            'total_processed': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error in batch prediction: {str(e)}")
        return jsonify({
            'error': 'Internal server error during batch prediction'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Load model on startup
    print("Loading simple protein stability prediction model...")
    load_model()
    
    # Run Flask app
    print("Starting Flask server...")
    print("API available at: http://localhost:5000")
    print("Try: curl -X POST http://localhost:5000/predict -H 'Content-Type: application/json' -d '{\"sequence\": \"MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG\"}'")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
