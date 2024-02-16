import RPi.GPIO as GPIO
import time

interval = 5

# Pin Definitions
iot1_button = 14  # TXD
iot2_button = 15  # RXD

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(iot1_button, GPIO.OUT)
GPIO.setup(iot2_button, GPIO.OUT)

def emulate_button_press(board_pin):
    GPIO.output(board_pin, GPIO.HIGH)
    time.sleep(0.1)  # Emulate button press duration
    GPIO.output(board_pin, GPIO.LOW)

try:
    while True:
        # Emulate button press on both boards
        emulate_button_press(iot1_button)
        emulate_button_press(iot2_button)

        # Wait for 5 seconds before next iteration
        time.sleep(interval)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO to default state
