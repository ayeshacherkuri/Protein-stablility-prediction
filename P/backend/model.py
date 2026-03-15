"""
Deep Learning Model for Protein Stability Prediction
CNN-based architecture for sequence analysis
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Tuple

class ProteinStabilityModel:
    def __init__(self, vocab_size: int = 22, max_length: int = 500, embedding_dim: int = 64):
        """
        Initialize the protein stability prediction model
        
        Args:
            vocab_size: Size of amino acid vocabulary
            max_length: Maximum sequence length
            embedding_dim: Embedding dimension
        """
        self.vocab_size = vocab_size
        self.max_length = max_length
        self.embedding_dim = embedding_dim
        self.model = None
        
    def build_model(self) -> keras.Model:
        """
        Build the CNN-based model architecture
        
        Returns:
            Compiled Keras model
        """
        # Input layer
        inputs = layers.Input(shape=(self.max_length, self.vocab_size))
        
        # Reshape for CNN (add channel dimension)
        x = layers.Reshape((self.max_length, self.vocab_size, 1))(inputs)
        
        # Convolutional layers
        x = layers.Conv2D(32, kernel_size=(3, self.vocab_size), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(pool_size=(2, 1))(x)
        x = layers.Dropout(0.25)(x)
        
        x = layers.Conv2D(64, kernel_size=(3, 1), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(pool_size=(2, 1))(x)
        x = layers.Dropout(0.25)(x)
        
        x = layers.Conv2D(128, kernel_size=(3, 1), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(pool_size=(2, 1))(x)
        x = layers.Dropout(0.25)(x)
        
        # Global pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(128, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        
        # Output layer (regression for stability score)
        stability_score = layers.Dense(1, name='stability_score')(x)
        
        # Classification output (stable/unstable)
        classification = layers.Dense(2, activation='softmax', name='classification')(x)
        
        # Create model
        model = keras.Model(inputs=inputs, outputs=[stability_score, classification])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss={
                'stability_score': 'mse',
                'classification': 'sparse_categorical_crossentropy'
            },
            metrics={
                'stability_score': 'mae',
                'classification': 'accuracy'
            }
        )
        
        self.model = model
        return model
    
    def train(self, 
              X_train: np.ndarray, 
              y_stability_train: np.ndarray, 
              y_class_train: np.ndarray,
              X_val: np.ndarray = None,
              y_stability_val: np.ndarray = None,
              y_class_val: np.ndarray = None,
              epochs: int = 50,
              batch_size: int = 32) -> keras.callbacks.History:
        """
        Train the model
        
        Args:
            X_train: Training sequences
            y_stability_train: Training stability scores
            y_class_train: Training classifications
            X_val: Validation sequences
            y_stability_val: Validation stability scores
            y_class_val: Validation classifications
            epochs: Number of training epochs
            batch_size: Batch size for training
            
        Returns:
            Training history
        """
        if self.model is None:
            self.build_model()
        
        # Prepare validation data
        validation_data = None
        if X_val is not None and y_stability_val is not None and y_class_val is not None:
            validation_data = (X_val, {
                'stability_score': y_stability_val,
                'classification': y_class_val
            })
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            )
        ]
        
        # Train model
        history = self.model.fit(
            X_train,
            {
                'stability_score': y_stability_train,
                'classification': y_class_train
            },
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def predict(self, sequences: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions on new sequences
        
        Args:
            sequences: Input sequences
            
        Returns:
            Tuple of (stability_scores, classifications)
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        predictions = self.model.predict(sequences)
        stability_scores = predictions[0].flatten()
        classifications = np.argmax(predictions[1], axis=1)
        
        return stability_scores, classifications
    
    def save_model(self, filepath: str):
        """
        Save the trained model
        
        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train or build model first.")
        
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load a trained model
        
        Args:
            filepath: Path to the saved model
        """
        self.model = keras.models.load_model(filepath)
        print(f"Model loaded from {filepath}")

def create_dummy_model() -> ProteinStabilityModel:
    """
    Create a dummy model for demonstration purposes
    
    Returns:
        ProteinStabilityModel instance
    """
    model = ProteinStabilityModel()
    model.build_model()
    return model
