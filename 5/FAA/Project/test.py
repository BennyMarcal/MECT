import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import matplotlib.pyplot as plt

# Load the dataset (change the path to where your X.npy file is located)
data = np.load('X.npy')  # Path to your dataset

# Assuming labels for 10 classes (numbers 0 to 9), we'll create mock labels
num_classes = 10
num_samples = data.shape[0]

# Generate mock labels (cycle through 0-9)
labels = np.array([i % num_classes for i in range(num_samples)])

# One-hot encode the labels for classification
labels_categorical = to_categorical(labels, num_classes)

# Reshape the data to fit the model input (add channel dimension for grayscale images)
X = data.reshape(num_samples, 64, 64, 1)

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, labels_categorical, test_size=0.2, random_state=42)

# Build a simple CNN model
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Plot the training and validation accuracy over epochs
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='validation accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plot the training and validation loss over epochs
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test Accuracy: {test_accuracy:.4f}')
print(f'Test Loss: {test_loss:.4f}')

# --- Real-time hand gesture recognition using the webcam ---

# Function to preprocess the webcam frame to 64x64 grayscale
def preprocess_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (64, 64))  # Resize to 64x64
    reshaped_frame = resized_frame.reshape(1, 64, 64, 1)  # Reshape to fit the model's input
    return reshaped_frame

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame from webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture frame")
        break
    
    # Preprocess the frame for model input
    preprocessed_frame = preprocess_frame(frame)
    
    # Predict the hand gesture (number) using the trained CNN model
    prediction = model.predict(preprocessed_frame)
    predicted_number = np.argmax(prediction)
    
    # Display the prediction on the frame
    cv2.putText(frame, f'Predicted Number: {predicted_number}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Hand Gesture Recognition', frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
