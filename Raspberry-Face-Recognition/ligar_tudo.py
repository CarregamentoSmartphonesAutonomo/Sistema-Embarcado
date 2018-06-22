import RPi.GPIO as gpio

# GPIO configuring
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)

try:
    # GPIO initial state
    gpio.output(12, gpio.LOW) # desativar tomada
    gpio.output(16, gpio.LOW) # desativar tomada
    gpio.output(18, gpio.LOW) # desativar tomada
    gpio.output(11, gpio.LOW) # cabine fechada
    gpio.output(13, gpio.LOW) # cabine fechada
    gpio.output(15, gpio.LOW) # cabine fechada
except KeyboardInterrupt:
    gpio.cleanup()