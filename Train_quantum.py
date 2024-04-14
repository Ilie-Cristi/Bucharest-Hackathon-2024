import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from qiskit.circuit.library import ZZFeatureMap
from qiskit.circuit.library import RealAmplitudes
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit_machine_learning.algorithms.classifiers import VQC
from sklearn.decomposition import PCA



# Read the CSV file (replace 'your_file.csv' with your actual file path)
df = pd.read_csv('phishing-dataset-variation.csv')

features = df.to_numpy()[:,:-1]
labels = df.to_numpy()[:,-1]

# Feature selection
features = PCA(n_components=20).fit_transform(features)

# Scale data
features = MinMaxScaler().fit_transform(features)

# Train test split
train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, train_size=0.8, random_state=1999)

# Feature encoding
num_features = features.shape[1]

feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)

# Ansatz 
ansatz = RealAmplitudes(num_qubits=num_features, reps=3)

# Optimizer
optimizer = COBYLA(maxiter=100)

# Sampler
sampler = Sampler()

# VQC
vqc = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=optimizer
)

# clear objective value history
objective_func_vals = []

start = time.time()
vqc.fit(train_features, train_labels)
elapsed = time.time() - start

print(f"Training time: {round(elapsed)} seconds")


#Testing
train_score_q4 = vqc.score(train_features, train_labels)
test_score_q4 = vqc.score(test_features, test_labels)

print(f"Quantum VQC on the training dataset: {train_score_q4:.2f}")
print(f"Quantum VQC on the test dataset:     {test_score_q4:.2f}")
