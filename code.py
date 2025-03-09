import board
import neopixel
import digitalio
import random
import pulseio
import adafruit_irremote
import asyncio

# Constants
TORNADO_PIXELS = 40
RED = (255, 0, 0)

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
btn_0 = digitalio.DigitalInOut(board.GP0)
btn_0.direction = digitalio.Direction.INPUT
btn_0.pull = digitalio.Pull.DOWN

btn_1 = digitalio.DigitalInOut(board.GP1)
btn_1.direction = digitalio.Direction.INPUT
btn_1.pull = digitalio.Pull.DOWN

# IR Receiver and Transmitters
pulsein = pulseio.PulseIn(board.GP23, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
nonblocking_decoder = adafruit_irremote.NonblockingGenericDecode(pulsein)
pulsein.clear()
pulsein.resume()

pulseout = pulseio.PulseOut(board.GP24, frequency=38000, duty_cycle=2 ** 15)
transmitter = adafruit_irremote.GenericTransmit(
    header=[9000, 4500],  # Example NEC header
    one=[560, 1690],      # Example NEC "1" pulses
    zero=[560, 560],      # Example NEC "0" pulses
    trail=560
)

def clear_leds():
    # Sets all pixels to blank
    for i in range(TORNADO_PIXELS):
        pixels_DIO_Tornado[i] = (0, 0, 0)
    pixels_DIO_Tornado.show()

async def blink(message_toggle, attack_toggle):
    # Blinks the LEDs. 
    # If message_toggle is True and if so activates message mode.
    # If attack_toggle is True all LEDs are red. 
    # Otherwise, clear all leds and blink a random LED a random color. 

    # Checks to see if Message is toggled on.
    if message_toggle:
        await message_mode()
    elif attack_toggle:
        await ir_attack()
    else:
        pixel_index = random.randint(0, TORNADO_PIXELS - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Ensure we start with all LEDs off
        clear_leds()

        print(f"Blinking pixel: {pixel_index}, Color: {color}")
        pixels_DIO_Tornado[pixel_index] = color
        pixels_DIO_Tornado.show()
        await asyncio.sleep(0.5)

async def ir_listen():
    # An asynchronous ir listener that listens for all incoming IR transmissions
    while True:
        pulsein.resume()

        try:
            while len(pulsein) == 0:
                await asyncio.sleep(0.1)
                
            # Process the pulses once they are available
            pulses = decoder.read_pulses(pulsein)
            print(f"Pulse Statistics: {adafruit_irremote.bin_data(pulses)}")
            
            # Convert each byte in the decoded_bits tuple to 0x format
            decoded_bits = decoder.decode_bits(pulses)
            decoded_hex = " ".join(f"0x{byte:02X}" for byte in decoded_bits)
            print("Decoded bits (Hex):", decoded_hex)

        except adafruit_irremote.IRNECRepeatException:
            print("NEC repeat detected, continuing.")
        except Exception as e:
            print("Failed to decode:", e)
        finally:
            pulsein.pause()

async def ir_attack():
    # And IR attack mode that transmitter NEX encoded IR blasts to push buttons on NEC controlled devices. 
    global transmitter, pulseout
    try:

        # Vizio = 0x20
        # LG = 0x01
        # Samsung = 0xE0
        # Sharp = 0x01
        # Toshiba = 0xF2
        tv_vendors = [0x20, 0x01, 0xE0, 0x01, 0xF2]
        common_cmds = [0x0C, 0x02, 0x1A, 0x30, 0xE0, 0x10, 0xF4]

        for address in range(256): #tv_vendors for a smaller list.. range(256) for a bruteforce
            for command in range(256): #common_cmds for a smaller list.. range(256) for a bruteforce
                nec_codes = [address, ~address & 0xFF, command, ~command & 0xFF]

                bit_list = []
                for byte in nec_codes:
                    bit_list.append(byte)
                print(f"Bit List: {bit_list}")    
                
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                
                print("Transmitting - Address: {0:#04x} Command: {1:#04x} => {2}".format(address, command, nec_codes))
                for i in range(TORNADO_PIXELS):
                    pixels_DIO_Tornado[i] = color
                pixels_DIO_Tornado.show()

                for i in range(1):
                    transmitter.transmit(pulseout, bit_list)
                    await asyncio.sleep(0.2)

    except Exception as e:
        print(f"Error Transmitting: {e}")

def text_to_morse(text):
    # Encodes an Input text into an list of Morse Code characters
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

async def message_mode():
    # Blinks the LEDS in Morse Code to display the input message visually. 
    message_text = "benjimanmiller.com"
    morse_code = text_to_morse(message_text)

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

    print(f"Input message to be displayed in Morse Code: {message_text}")

    for digit in morse_code:
        if digit == "-": 
            print(f"Blinking Pixels: {digit}, Color: {dash_color}")
            for i in range(TORNADO_PIXELS):
                pixels_DIO_Tornado[i] = dash_color
            pixels_DIO_Tornado.show()
            await asyncio.sleep(0.8)
            clear_leds()
            await asyncio.sleep(0.1)

        if digit == ".":
            print(f"Blinking Pixels: {digit}, Color: {dot_color}")
            for i in range(TORNADO_PIXELS):
                pixels_DIO_Tornado[i] = dot_color
            pixels_DIO_Tornado.show()
            await asyncio.sleep(0.4)
            clear_leds()
            await asyncio.sleep(0.1)

        if digit == "X":
            print(" ")
            clear_leds()
            await asyncio.sleep(0.3)

    await asyncio.sleep(1)

async def main():
    print("Starting main loop.")

    clear_leds()

    running_tasks = set()
    task = asyncio.create_task(ir_listen())
    running_tasks.add(task)

    attack_toggle = False
    message_toggle = False

    while True:
        
        if btn_0.value:
            message_toggle = not message_toggle
            print(f"btn_0: Pressed, Message Toggle: {message_toggle}")
            await asyncio.sleep(1)
        if btn_1.value:
            attack_toggle = not attack_toggle
            print(f"btn_1: Pressed, IR Attack Toggle: {attack_toggle}")
            await asyncio.sleep(1)
        else:
            await blink(message_toggle, attack_toggle)
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(main())
