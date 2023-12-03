import RPi.GPIO as GPIO
import pygame
import time

# Set up GPIO
GPIO_PIN = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Set up Pygame
pygame.mixer.init()

# Define the audio file name
file_name = "output.mp3"

try:
    # Play the audio file
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    pass

finally:
    # Clean up GPIO and Pygame
    GPIO.cleanup()
    pygame.mixer.quit()
