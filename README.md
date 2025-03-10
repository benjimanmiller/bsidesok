# BsidesOK
Collection of scripts related to the BsidesOK convention.

## code.py
This script is to be placed in the main directory of the Bsides2024 badge's RPI Pico board.

This script has three modes:  
- **Default - Random Blink**: A random LED blinks a random color.  
- **BTN_0 - Morse Code Message**: This mode blinks the LEDs to display a message encoded in Morse code.  
- **BTN_1 - IR Attack**: This mode uses the badge's built-in IR transceiver to blast all possible command codes for all possible vendors of devices that use NEC IR encoding. The LEDs will blink as the attack blasts IR signals.  

Additionally, running passively in the background is an IR listener that will display all received IR signals on the console and blink the 2024 LEDs red. 
