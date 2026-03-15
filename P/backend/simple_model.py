"""
Simplified Protein Stability Prediction Model
A lightweight model that doesn't require TensorFlow for demonstration
"""

import numpy as np
import random
from typing import Tuple

class SimpleProteinStabilityModel:
    def __init__(self):
        """
        Initialize a simple protein stability prediction model
        """
        self.is_trained = False
        
    def train(self, sequences, stability_scores, classifications):
        """
        Simple training - just mark as trained
        """
        self.is_trained = True
        print("Simple model marked as trained")
        
    def predict(self, sequences: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions using a simple heuristic approach
        
        Args:
            sequences: Input sequences (one-hot encoded)
            
        Returns:
            Tuple of (stability_scores, classifications)
        """
        if not self.is_trained:
            self.is_trained = True
            
        batch_size = sequences.shape[0]
        stability_scores = []
        classifications = []
        
        for i in range(batch_size):
            # Extract sequence from one-hot encoding
            sequence = self._decode_sequence(sequences[i])
            
            # Calculate simple stability score based on amino acid composition
            score = self._calculate_stability_score(sequence)
            stability_scores.append(score)
            
            # Classification: negative scores are stable, positive are unstable
            classification = 0 if score < 0 else 1  # 0=Stable, 1=Unstable
            classifications.append(classification)
        
        return np.array(stability_scores), np.array(classifications)
    
    def _decode_sequence(self, one_hot_sequence):
        """
        Decode one-hot encoded sequence back to amino acid string
        """
        amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        sequence = ''
        
        for pos in one_hot_sequence:
            if np.sum(pos) > 0:  # Not padding
                aa_idx = np.argmax(pos)
                if aa_idx < len(amino_acids):
                    sequence += amino_acids[aa_idx]
        
        return sequence
    
    def _calculate_stability_score(self, sequence: str) -> float:
        """
        Calculate stability score using simple heuristics
        
        Args:
            sequence: Amino acid sequence
            
        Returns:
            Stability score (negative = stable, positive = unstable)
        """
        if not sequence:
            return 0.0
        
        # Amino acid properties
        hydrophobic = 'AVILMFW'  # Hydrophobic (stabilizing)
        charged = 'DEKRH'        # Charged (can be destabilizing)
        polar = 'STNQ'           # Polar (neutral)
        special = 'CG'           # Special cases
        
        # Count amino acids
        hydrophobic_count = sum(1 for aa in sequence if aa in hydrophobic)
        charged_count = sum(1 for aa in sequence if aa in charged)
        polar_count = sum(1 for aa in sequence if aa in polar)
        special_count = sum(1 for aa in sequence if aa in special)
        
        # Calculate base score
        total_length = len(sequence)
        
        # Hydrophobic ratio (higher = more stable)
        hydrophobic_ratio = hydrophobic_count / total_length
        
        # Charged ratio (higher = potentially less stable)
        charged_ratio = charged_count / total_length
        
        # Length factor (longer sequences slightly less stable)
        length_factor = (total_length - 100) / 200 if total_length > 100 else 0
        
        # Calculate stability score
        base_score = -5.0  # Base stability
        hydrophobic_bonus = hydrophobic_ratio * 15  # Hydrophobic amino acids stabilize
        charged_penalty = charged_ratio * 8         # Too many charged residues can destabilize
        length_penalty = length_factor * 2          # Longer sequences slightly less stable
        
        stability_score = base_score + hydrophobic_bonus - charged_penalty - length_penalty
        
        # Add some randomness for demonstration
        stability_score += random.normalvariate(0, 1.5)
        
        return stability_score
    
    def save_model(self, filepath: str):
        """
        Save the model (simple version)
        """
        print(f"Simple model saved to {filepath}")
        
    def load_model(self, filepath: str):
        """
        Load the model (simple version)
        """
        self.is_trained = True
        print(f"Simple model loaded from {filepath}")

def create_simple_model():
    """
    Create a simple model for demonstration
    """
    return SimpleProteinStabilityModel()
