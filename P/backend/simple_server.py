"""
Very Simple Protein Stability Prediction Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Protein Stability Prediction API (Simple)',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        sequence = data.get('sequence', '')
        
        if not sequence:
            return jsonify({'error': 'No sequence provided'}), 400
        
        # Simple prediction logic
        length = len(sequence)
        hydrophobic_count = sum(1 for aa in sequence if aa in 'AVILMFW')
        charged_count = sum(1 for aa in sequence if aa in 'DEKRH')
        
        # Calculate simple stability score
        hydrophobic_ratio = hydrophobic_count / length
        charged_ratio = charged_count / length
        
        # Simple heuristic: more hydrophobic = more stable
        base_score = -5.0
        stability_score = base_score + (hydrophobic_ratio * 10) - (charged_ratio * 5)
        stability_score = base_score + (hydrophobic_ratio * 10) - (charged_ratio * 5)
        # Removed random noise for deterministic results
        
        # Classification
        classification = "Stable" if stability_score < 0 else "Unstable"
        # Improved confidence calculation
        # Map score magnitude to confidence more effectively
        # 0.5 base + up to 0.45 based on score magnitude
        magnitude = abs(stability_score)
        confidence = 0.5 + min(0.48, (magnitude / 8.0))
        magnitude = abs(stability_score)
        confidence = 0.5 + min(0.48, (magnitude / 8.0))
        confidence = round(confidence, 2) # Deterministic confidence
        
        return jsonify({
            'stability_score': round(stability_score, 2),
            'classification': classification,
            'confidence': round(confidence, 2),
            'sequence_length': length,
            'features': {
                'hydrophobic_count': hydrophobic_count,
                'charged_count': charged_count,
                'polar_count': sum(1 for aa in sequence if aa in 'STNQ')
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting simple protein stability prediction server...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
