"""
Model Training Script
Trains the protein stability prediction model using dummy data
"""

import numpy as np
import random
from preprocess import ProteinPreprocessor
from model import ProteinStabilityModel
import os

def generate_dummy_data(num_samples: int = 1000) -> tuple:
    """
    Generate dummy protein sequences and stability data for training
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        Tuple of (sequences, stability_scores, classifications)
    """
    # Amino acid alphabet
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    sequences = []
    stability_scores = []
    classifications = []
    
    for i in range(num_samples):
        # Generate random sequence length (50-300 amino acids)
        seq_length = random.randint(50, 300)
        
        # Generate random sequence
        sequence = ''.join(random.choices(amino_acids, k=seq_length))
        sequences.append(sequence)
        
        # Generate dummy stability score based on sequence properties
        # More hydrophobic amino acids (A, V, I, L, M, F, W) tend to be more stable
        hydrophobic_count = sum(1 for aa in sequence if aa in 'AVILMFW')
        charged_count = sum(1 for aa in sequence if aa in 'DEKRH')
        
        # Calculate dummy stability score (-15 to 5 kcal/mol)
        base_score = -5.0
        hydrophobic_bonus = (hydrophobic_count / len(sequence)) * 10
        charged_penalty = (charged_count / len(sequence)) * 5
        length_factor = (len(sequence) - 100) / 200  # Longer sequences slightly less stable
        
        stability_score = base_score + hydrophobic_bonus - charged_penalty - length_factor
        stability_score += random.normalvariate(0, 2)  # Add some noise
        
        stability_scores.append(stability_score)
        
        # Classification: negative scores are stable, positive are unstable
        classification = 0 if stability_score < 0 else 1  # 0=Stable, 1=Unstable
        classifications.append(classification)
    
    return sequences, np.array(stability_scores), np.array(classifications)

def train_model():
    """
    Train the protein stability prediction model
    """
    print("Generating dummy training data...")
    
    # Generate training data
    train_sequences, train_stability, train_class = generate_dummy_data(800)
    
    # Generate validation data
    val_sequences, val_stability, val_class = generate_dummy_data(200)
    
    print(f"Training samples: {len(train_sequences)}")
    print(f"Validation samples: {len(val_sequences)}")
    
    # Initialize preprocessor
    preprocessor = ProteinPreprocessor(max_length=500)
    
    print("Encoding sequences...")
    
    # Encode sequences
    X_train = preprocessor.encode_batch(train_sequences)
    X_val = preprocessor.encode_batch(val_sequences)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_val.shape}")
    
    # Initialize and build model
    print("Building model...")
    model = ProteinStabilityModel(
        vocab_size=preprocessor.vocab_size,
        max_length=preprocessor.max_length
    )
    model.build_model()
    
    # Print model summary
    model.model.summary()
    
    # Train model
    print("Training model...")
    history = model.train(
        X_train=X_train,
        y_stability_train=train_stability,
        y_class_train=train_class,
        X_val=X_val,
        y_stability_val=val_stability,
        y_class_val=val_class,
        epochs=15,  # Reduced for demo
        batch_size=32
    )
    
    # Save model
    model_path = 'model.h5'
    model.save_model(model_path)
    
    print(f"Model training completed!")
    print(f"Model saved to: {model_path}")
    
    # Print some training statistics
    print("\nTraining Statistics:")
    print(f"Final training loss: {history.history['loss'][-1]:.4f}")
    print(f"Final validation loss: {history.history['val_loss'][-1]:.4f}")
    print(f"Final classification accuracy: {history.history['classification_accuracy'][-1]:.4f}")
    
    return model, preprocessor

def test_model(model, preprocessor):
    """
    Test the trained model with sample sequences
    
    Args:
        model: Trained ProteinStabilityModel
        preprocessor: ProteinPreprocessor instance
    """
    print("\nTesting model with sample sequences...")
    
    # Sample sequences for testing
    test_sequences = [
        "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",  # Human insulin
        "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR",  # Hemoglobin
        "MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNLW",  # Lysozyme
    ]
    
    for i, sequence in enumerate(test_sequences):
        # Encode sequence
        encoded = preprocessor.encode_sequence(sequence)
        encoded_batch = np.expand_dims(encoded, axis=0)
        
        # Make prediction
        stability_score, classification = model.predict(encoded_batch)
        
        # Get classification label
        class_label = "Stable" if classification[0] == 0 else "Unstable"
        
        print(f"\nTest Sequence {i+1}:")
        print(f"Sequence: {sequence[:50]}...")
        print(f"Length: {len(sequence)} amino acids")
        print(f"Predicted Stability Score: {stability_score[0]:.2f} kcal/mol")
        print(f"Classification: {class_label}")
        
        # Get sequence features
        features = preprocessor.get_sequence_features(sequence)
        print(f"Hydrophobic amino acids: {features['hydrophobic_count']}")
        print(f"Charged amino acids: {features['charged_count']}")

if __name__ == "__main__":
    # Train the model
    model, preprocessor = train_model()
    
    # Test the model
    test_model(model, preprocessor)
    
    print("\nModel training and testing completed successfully!")
    print("You can now use the trained model for predictions.")
