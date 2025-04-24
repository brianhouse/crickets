# connection constants
POWER = 7
MAX_HOOD = 7
INIT_HOOD = 5
MIN_HOOD = 3
FRIEND_LINK = .2
GROUP_LEADER = .2
SEVER = -3

# capacitor constants
FREQ = 1            # endogenous frequency in Hz
BUMP = 0.01         # capacitor bump amount when neighbor flashes
REST = 0.10         # percent of cycle to be unresponsive after flash (in practice, the time it takes to flash overrides this ~145ms)
TICK = 0.01         # cycle resolution in seconds

# automatic constants
PITCH_LOW, PITCH_HIGH = 3000, 4500
HUM_LOW, HUM_HIGH = 10, 20

# behavior constants
MOTION = False
STATUS = False
BLINK = True
CHIRP = False


from util import *





