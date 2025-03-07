import time
import board
import neopixel
import digitalio
import random

# Constants
TORNADO_PIXELS = 40
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Enable the LED Power (Pin 25)
pin_led_en = digitalio.DigitalInOut(board.GP25)
pin_led_en.direction = digitalio.Direction.OUTPUT
pin_led_en.value = True  # Must be True to power the LEDs

# Initialize Tornado LEDs
pixels_DIO_Tornado = neopixel.NeoPixel(
    board.GP10, TORNADO_PIXELS, brightness=0.05, auto_write=False
)

# GPIO13 LED Indicator
pin_led = digitalio.DigitalInOut(board.GP13)
pin_led.direction = digitalio.Direction.OUTPUT

# GPIO Buttons
# Re-enable btn_1 for detection
btn_1 = digitalio.DigitalInOut(board.GP1)
btn_1.direction = digitalio.Direction.INPUT
btn_1.pull = digitalio.Pull.DOWN

# GPIO Buttons
# Re-enable btn_0 for detection
btn_0 = digitalio.DigitalInOut(board.GP0)
btn_0.direction = digitalio.Direction.INPUT
btn_0.pull = digitalio.Pull.DOWN


def clear_leds():
    # Sets all pixesl to blank
    for i in range(TORNADO_PIXELS):
        pixels_DIO_Tornado[i] = (0, 0, 0)
    pixels_DIO_Tornado.show()


def blink(message_toggle, red_toggle):
    # Picks a random LED and blinks it

    # Checks to see if Message is toggled on.
    if message_toggle == True:
        message_mode()
        time.sleep(1)
    elif red_toggle == True:
        set_all_red()
        time.sleep(1)
    else:
        pixel_index = random.randint(0, TORNADO_PIXELS - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Ensure we start with all LEDs off
        clear_leds()

        print(f"Blinking pixel: {pixel_index}, Color: {color}")
        pixels_DIO_Tornado[pixel_index] = color
        pixels_DIO_Tornado.show()
        time.sleep(0.5)


def set_all_red():
    # Toggles on a Full Red LED Array
    for i in range(TORNADO_PIXELS):
        pixels_DIO_Tornado[i] = RED
    pixels_DIO_Tornado.show()


def text_to_morse(text):
    morse_dict = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        " ": "X",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "'": ".----.",
        "!": "-.-.--",
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.-",
        "&": ".-...",
        ":": "---...",
        ";": "-.-.-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "_": "..--.-",
        '"': ".-..-.",
        "$": "...-..-",
        "@": ".--.-.",
    }

    text = text.upper()
    morse_array = []

    for char in text:
        if char in morse_dict:
            morse_array.extend(morse_dict[char])

    return morse_array


def message_mode():
    # Toggles on the Message blinking
    input_text = "benjimanmiller.com"
    morse_code = text_to_morse(input_text)

    dash_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    
    dot_color = (
        random.randint(0, 255), 
        random.randint(0, 255), 
        random.randint(0, 255)
    )

    print(f"Input message to be displayed in Morse Code: {input_text}")
    
    for digit in morse_code:
        if digit == "-":
            print(f"Blinking Pixels: {digit}, Color: {dash_color}")
            for i in range(TORNADO_PIXELS):
                pixels_DIO_Tornado[i] = dash_color
            pixels_DIO_Tornado.show()
            time.sleep(0.8)
            clear_leds()
            time.sleep(0.25)
        if digit == ".":
            print(f"Blinking Pixels: {digit}, Color: {dot_color}")
            for i in range(TORNADO_PIXELS):
                pixels_DIO_Tornado[i] = dot_color
            pixels_DIO_Tornado.show()
            time.sleep(0.4)
            clear_leds()
            time.sleep(0.25)
        if digit == "X":
            print(" ")
            clear_leds()
            time.sleep(0.3)

    time.sleep(1)


def main():
    print("Starting main loop.")

    # Ensure we start with all LEDs off
    clear_leds()

    red_toggle = False
    message_toggle = False

    while True:
        # If button 1 is pressed, keep everything red
        if btn_1.value:
            if red_toggle == True:
                red_toggle = False
            else:
                red_toggle = True
            print(f"btn_1: Pressed, Red Toggle: {red_toggle}")
            time.sleep(1)
        if btn_0.value:
            if message_toggle == True:
                message_toggle = False
            else:
                message_toggle = True
            print(f"btn_0: Pressed, Message Toggle: {message_toggle}")
            time.sleep(1)
        else:
            # Otherwise, run the random blink pattern
            blink(message_toggle, red_toggle)
            time.sleep(0.1)


if __name__ == "__main__":
    main()
