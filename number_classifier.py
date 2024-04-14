from PIL import Image
import numpy as np
import streamlit as st
import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model("trained_model.h5")

# Define a function to preprocess and classify the uploaded image
def classify_image(img):
    # Resize the image to 28x28 pixels
    img = img.resize((28, 28))
    
    # Convert the image to grayscale
    img = img.convert('L')
    
    # Convert the image to a NumPy array and normalize pixel values
    img_np = np.array(img) / 255.0
    
    # Reshape the image to match the model's input shape
    img_np = img_np.reshape(1, 28, 28, 1)
    
    # Classify the image
    prediction = model.predict(img_np)
    
    # Extract the predicted digit
    predicted_digit = np.argmax(prediction)
    
    return predicted_digit


# Main function
def main():
    st.title('Number Classifier App')
    st.sidebar.title('Upload Image')

    # Allow user to upload an image file
    uploaded_img = st.sidebar.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])

    # Display the uploaded image
    if uploaded_img is not None:
        img = Image.open(uploaded_img)
        st.image(img, caption='Uploaded Image', use_column_width=True)

        # Classify the uploaded image if the user clicks the 'Classify' button
        if st.sidebar.button('Classify'):
            prediction = classify_image(img)
            st.write(f'Predicted Digit: {prediction}')

if __name__ == "__main__":
    main()
