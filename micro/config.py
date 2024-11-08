from esp_helper import *

# connection constants
RANGE = -100
HOOD = 5

# capacitor constants
FREQ = 1            # endogenous frequency in Hz
BUMP = 0.013        # capacitor bump amount when neighbor flashes
REST = 0.1          # percent of cycle to be unresponsive after flash
TICK = 1            # cycle resolution in ms

# automatic constants
PITCH = randint(3500, 4500)
HUM = randint(10, 20)

# debug server port
HTTP = 8088

