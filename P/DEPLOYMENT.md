# Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd protein-stability-prediction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Train the Model
```bash
# Train the model (this will create model.h5)
python train_model.py
```

### Step 4: Start the Backend Server
```bash
# Start Flask server
python app.py
```

The API will be available at: `http://localhost:5000`

### Step 5: Open the Frontend
Open `frontend/index.html` in your web browser or serve it using a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## Testing the Application

### Test the API
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test prediction endpoint
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"sequence": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"}'
```

### Expected Response
```json
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
```

## Cloud Deployment

### Option 1: Render (Recommended - Free)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Connect Repository**
   - Connect your GitHub repository
   - Create a new Web Service

3. **Configure Build Settings**
   ```
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && python app.py
   ```

4. **Environment Variables**
   - Add any required environment variables in Render dashboard

5. **Deploy**
   - Render will automatically deploy your application
   - Your API will be available at: `https://your-app-name.onrender.com`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Download and install from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Create Procfile**
   Create `Procfile` in the root directory:
   ```
   web: cd backend && gunicorn app:app
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 3: PythonAnywhere

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Sign up for a free account

2. **Upload Files**
   - Upload your project files to PythonAnywhere

3. **Install Dependencies**
   ```bash
   pip install --user -r backend/requirements.txt
   ```

4. **Configure WSGI**
   - Edit the WSGI configuration file
   - Point to your Flask app

5. **Deploy**
   - Your app will be available at: `yourusername.pythonanywhere.com`

## Production Considerations

### Environment Variables
Create a `.env` file for production:
```env
FLASK_ENV=production
FLASK_DEBUG=False
MODEL_PATH=model.h5
```

### Security
- Enable HTTPS in production
- Add rate limiting
- Implement API authentication if needed
- Validate all inputs

### Performance
- Use a production WSGI server (Gunicorn)
- Enable caching for model predictions
- Optimize model loading
- Monitor API performance

### Monitoring
- Add logging for production
- Monitor API health
- Track prediction accuracy
- Set up error alerts

## Troubleshooting

### Common Issues

1. **Model Loading Error**
   ```bash
   # Ensure model.h5 exists
   ls backend/model.h5
   
   # Retrain if missing
   python backend/train_model.py
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill process
   kill -9 <PID>
   ```

3. **CORS Issues**
   - Ensure `flask-cors` is installed
   - Check frontend API URL configuration

4. **Memory Issues**
   - Reduce model complexity
   - Use smaller batch sizes
   - Optimize sequence encoding

### Performance Optimization

1. **Model Optimization**
   ```python
   # In app.py, add model caching
   import tensorflow as tf
   tf.config.optimizer.set_jit(True)
   ```

2. **API Response Caching**
   ```python
   # Add caching for repeated sequences
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def cached_predict(sequence):
       # prediction logic
   ```

## Support

For issues and questions:
- Check the logs in your deployment platform
- Verify all dependencies are installed
- Ensure the model file exists and is valid
- Test with sample sequences first

## Example Usage

### Frontend Integration
```javascript
// Example API call from frontend
const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        sequence: 'MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG'
    })
});

const result = await response.json();
console.log('Stability Score:', result.stability_score);
console.log('Classification:', result.classification);
```

### Batch Processing
```bash
# Process multiple sequences
curl -X POST http://localhost:5000/predict_batch \
  -H "Content-Type: application/json" \
  -d '{
    "sequences": [
      "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
      "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"
    ]
  }'
```
