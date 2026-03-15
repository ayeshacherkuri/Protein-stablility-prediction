# Protein Stability Prediction from Amino Acid Sequence using Deep Learning

A web-based application that predicts protein stability from amino acid sequences using deep learning.

## Features

- **Backend API**: Flask-based REST API for protein stability prediction
- **Deep Learning Model**: CNN-based model trained on protein sequences
- **Frontend**: Simple HTML/CSS/JavaScript interface
- **Real-time Prediction**: Get stability scores and classifications instantly

## Project Structure

```
protein-stability-prediction/
├── backend/
│   ├── app.py                 # Flask application
│   ├── model.py              # Deep learning model definition
│   ├── preprocess.py         # Sequence preprocessing utilities
│   ├── train_model.py        # Model training script
│   ├── model.h5              # Trained model file
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Main webpage
│   ├── style.css             # Styling
│   └── script.js             # JavaScript functionality
├── data/
│   └── sample_sequences.txt  # Sample protein sequences
└── README.md                 # This file
```

## Quick Start (Windows, recommended)

### 1) Start the backend (simple server, no TensorFlow)

Open PowerShell and run:

```powershell
cd C:\Users\jyots\Downloads\P\backend
py -3 -m pip install --user Flask==2.3.3 flask-cors==4.0.0
py -3 simple_server.py
```

This starts the API at `http://127.0.0.1:5000`.

### 2) Start the frontend (serve static files)

Open a second PowerShell window and run:

```powershell
cd C:\Users\jyots\Downloads\P\frontend
py -3 -m http.server 5500 --bind 127.0.0.1
```

Open the app at `http://127.0.0.1:5500`.

### 3) Use the app

- Enter a protein sequence
- Click "Predict Stability"
- Results will be fetched from `http://127.0.0.1:5000`

## Alternative: Full backend with TensorFlow (optional)

If you want the full TensorFlow model, install the dependencies in `backend/requirements.txt` and run `app.py`. Note that some TensorFlow versions may not be available for the latest Python releases; you might need Python 3.10–3.11.

```powershell
cd backend
py -3 -m pip install -r requirements.txt
py -3 app.py
```

## Troubleshooting

- If your browser tries to open `http://[::]:5500/` or you see `ERR_ADDRESS_INVALID`, use `http://127.0.0.1:5500` instead. We bind the frontend server explicitly to `127.0.0.1` to avoid IPv6-only addresses.
- If the frontend says it cannot reach the backend, ensure the backend is running at `http://127.0.0.1:5000` and that `frontend/script.js` has `API_BASE_URL = 'http://localhost:5000';` (this works for `127.0.0.1` too).

## API Endpoints

- `POST /predict`: Predict protein stability
  - Input: `{"sequence": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"}`
  - Output: `{"stability_score": -8.5, "classification": "Stable", "confidence": 0.92}`

## Technologies Used

- **Backend**: Flask, TensorFlow/Keras
- **Frontend**: HTML, CSS, JavaScript
- **ML**: CNN for sequence analysis
- **Deployment**: Ready for Heroku/Render/PythonAnywhere

## License

MIT License
