import cv2
import time
import speech_recognition as sr

def capture_photo(cap):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        return None, None  # Return None if capture fails

    # Generate a timestamp to save the image with a unique name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_filename = f"photo_{timestamp}.jpg"

    # Save the captured frame as an image
    cv2.imwrite(image_filename, frame)
    print(f"Photo saved as {image_filename}")

    return image_filename, frame

def listen_for_keyword(keyword="capture"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for the keyword...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise levels
        audio = recognizer.listen(source)  # Listen to the audio input

    try:
        # Recognize the speech using Google's speech recognition
        recognized_text = recognizer.recognize_google(audio).lower()
        print(f"Heard: {recognized_text}")

        # Check if the recognized text contains the keyword
        if keyword in recognized_text:
            print(f"Keyword '{keyword}' detected!")
            return True
        else:
            print(f"Keyword '{keyword}' not detected.")
            return False
    
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return False
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return False

def main():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam is open! Listening for the 'capture' command.")

    if listen_for_keyword("capture"):
        image_filename, frame = capture_photo(cap)
        if image_filename and frame is not None:
            # Show the captured image in a window
            cv2.imshow('Captured Image', frame)
            cv2.waitKey(0)  # Display the image until a key is pressed

    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the program
main()
