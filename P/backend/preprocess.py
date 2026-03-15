"""
Protein Sequence Preprocessing Module
Handles encoding of amino acid sequences for deep learning models
"""

import numpy as np
from typing import List, Tuple

class ProteinPreprocessor:
    def __init__(self, max_length: int = 500):
        """
        Initialize the protein preprocessor
        
        Args:
            max_length: Maximum sequence length to pad/truncate to
        """
        self.max_length = max_length
        
        # Standard amino acid alphabet (20 amino acids)
        self.amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
        self.aa_to_idx = {aa: idx for idx, aa in enumerate(self.amino_acids)}
        self.idx_to_aa = {idx: aa for idx, aa in enumerate(self.amino_acids)}
        
        # Add special tokens
        self.pad_token = '<PAD>'
        self.unk_token = '<UNK>'
        self.aa_to_idx[self.pad_token] = len(self.amino_acids)
        self.aa_to_idx[self.unk_token] = len(self.amino_acids) + 1
        
        self.vocab_size = len(self.aa_to_idx)
    
    def validate_sequence(self, sequence: str) -> bool:
        """
        Validate if a sequence contains valid amino acid characters
        
        Args:
            sequence: Amino acid sequence string
            
        Returns:
            True if valid, False otherwise
        """
        if not sequence or len(sequence) == 0:
            return False
        
        # Check if all characters are valid amino acids
        valid_chars = set(self.amino_acids + 'X')  # X for unknown amino acids
        return all(char.upper() in valid_chars for char in sequence)
    
    def clean_sequence(self, sequence: str) -> str:
        """
        Clean and standardize a protein sequence
        
        Args:
            sequence: Raw protein sequence
            
        Returns:
            Cleaned sequence
        """
        # Convert to uppercase
        sequence = sequence.upper()
        
        # Remove whitespace and newlines
        sequence = ''.join(sequence.split())
        
        # Replace invalid characters with X
        cleaned = ''
        for char in sequence:
            if char in self.amino_acids:
                cleaned += char
            else:
                cleaned += 'X'
        
        return cleaned
    
    def encode_sequence(self, sequence: str) -> np.ndarray:
        """
        Encode a protein sequence using one-hot encoding
        
        Args:
            sequence: Protein sequence string
            
        Returns:
            One-hot encoded sequence as numpy array
        """
        # Clean the sequence
        sequence = self.clean_sequence(sequence)
        
        # Pad or truncate to max_length
        if len(sequence) > self.max_length:
            sequence = sequence[:self.max_length]
        else:
            sequence = sequence.ljust(self.max_length, self.pad_token)
        
        # Convert to indices
        indices = []
        for char in sequence:
            if char in self.aa_to_idx:
                indices.append(self.aa_to_idx[char])
            else:
                indices.append(self.aa_to_idx[self.unk_token])
        
        # One-hot encode
        encoded = np.zeros((self.max_length, self.vocab_size))
        for i, idx in enumerate(indices):
            encoded[i, idx] = 1.0
        
        return encoded
    
    def encode_batch(self, sequences: List[str]) -> np.ndarray:
        """
        Encode a batch of protein sequences
        
        Args:
            sequences: List of protein sequence strings
            
        Returns:
            Batch of encoded sequences as numpy array
        """
        encoded_sequences = []
        for sequence in sequences:
            encoded = self.encode_sequence(sequence)
            encoded_sequences.append(encoded)
        
        return np.array(encoded_sequences)
    
    def get_sequence_features(self, sequence: str) -> dict:
        """
        Extract basic features from a protein sequence
        
        Args:
            sequence: Protein sequence string
            
        Returns:
            Dictionary of sequence features
        """
        sequence = self.clean_sequence(sequence)
        
        features = {
            'length': len(sequence),
            'amino_acid_composition': {},
            'hydrophobic_count': 0,
            'charged_count': 0,
            'polar_count': 0
        }
        
        # Amino acid composition
        for aa in self.amino_acids:
            features['amino_acid_composition'][aa] = sequence.count(aa)
        
        # Hydrophobic amino acids (A, V, I, L, M, F, W)
        hydrophobic = 'AVILMFW'
        features['hydrophobic_count'] = sum(sequence.count(aa) for aa in hydrophobic)
        
        # Charged amino acids (D, E, K, R, H)
        charged = 'DEKRH'
        features['charged_count'] = sum(sequence.count(aa) for aa in charged)
        
        # Polar amino acids (S, T, N, Q)
        polar = 'STNQ'
        features['polar_count'] = sum(sequence.count(aa) for aa in polar)
        
        return features

# Global preprocessor instance
preprocessor = ProteinPreprocessor()
