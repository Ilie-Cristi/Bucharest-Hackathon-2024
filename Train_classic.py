import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_recall_fscore_support
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf


# Read the CSV file (replace 'your_file.csv' with your actual file path)
df = pd.read_csv('phishing-dataset-variation.csv')

# Split the data (70% for training, 30% for testing)
msk = np.random.rand(len(df)) <= 0.7
train_data = df[msk].to_numpy()
test_data = df[~msk].to_numpy()

# Convert to NumPy arrays
X_train = train_data[:,:-1]
y_train = train_data[:,-1]

X_test = test_data[:,:-1]
y_test = test_data[:,-1]

print('Done splitting')

knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

print('Done KNN')

logreg_classifier = LogisticRegression(max_iter=5000)
logreg_classifier.fit(X_train, y_train)

rf_classifier = RandomForestClassifier(n_estimators=100)
rf_classifier.fit(X_train, y_train)

print('Done RF')

# Create a simple feedforward neural network
model = Sequential()
model.add(Dense(units=X_train.shape[1], activation='relu'))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))  # Binary classification

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, batch_size=32)

print('Done NN')

knn_predictions = knn_classifier.predict(X_test)
knn_f1 = f1_score(y_test, knn_predictions)
print(f"KNN F1-score: {knn_f1:.2f}")

logreg_predictions = logreg_classifier.predict(X_test)
logreg_f1 = f1_score(y_test, logreg_predictions)
print(f"Logistic Regression F1-score: {logreg_f1:.2f}")

rf_predictions = rf_classifier.predict(X_test)
rf_f1 = f1_score(y_test, rf_predictions)
print(f"Random Forest F1-score: {rf_f1:.2f}")

nn_predictions = model.predict(X_test)
nn_predictions = (nn_predictions > 0.5).astype(int) 
nn_f1 = f1_score(y_test, nn_predictions)
print(f"Neural Network F1-score: {nn_f1:.2f}")