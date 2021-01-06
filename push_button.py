import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from printer import print_function

def button_callback(channel):
    print_function()
    print("Button was pushed!")

def push_button_command():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(37, GPIO.IN,
               pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(37, GPIO.RISING, callback=button_callback)  # Setup event on pin 10 rising edge
    message = input("Press enter to quit\n\n")  # Run until someone presses enter
    GPIO.cleanup()  # Clean up