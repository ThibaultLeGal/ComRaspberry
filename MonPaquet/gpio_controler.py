import RPi.GPIO as GPIO
import val_def

def setupOutput(gpiolist):
    print("Outputs setup")
    GPIO.setmode(GPIO.BOARD)
    for key in gpiolist.keys():
        GPIO.setup(gpiolist[key].pin, GPIO.OUT, initial=GPIO.LOW)
        
def setupInput(gpioInlist):
    print("Inputs setup")
    GPIO.setmode(GPIO.BOARD)
    for key in gpioInlist.keys():
        GPIO.setup(gpioInlist[key].pin, GPIO.IN)


def apply(gpiolist):
    print("apply gpios")
    for key in gpiolist.keys():
        l_value = gpiolist[key].value
        #if l_value == "true" or l_value == "1" or l_value == "On":
        if l_value in val_def.setHigh :
            GPIO.output(gpiolist[key].pin, GPIO.HIGH)
        #elif l_value == "false" or l_value == "0" or l_value == "Off":
        if l_value in val_def.setLow :
            GPIO.output(gpiolist[key].pin, GPIO.LOW)
        elif l_value == "BlinkFast":
            p = GPIO.PWM(gpiolist[key].pin, 10)
            p.start(50.0)
            #Attention, peut créer des problèmes pour changer une fois set. A tester!!!
        elif l_value == "BlinkSlow":
            p = GPIO.PWM(gpiolist[key].pin, 1)
            p.start(50.0)
            # Attention, peut créer des problèmes pour changer une fois set. A tester!!!


def readgpios(gpiolist):
	print("read gpios")
	for key in gpiolist.keys():
		val = GPIO.input(gpiolist[key].pin)
		if val == GPIO.HIGH :
			gpiolist[key].value = "On"
		else:
			gpiolist[key].value = "Off"
			#TODO : pas toujours On ou Off, faire intersection de range et set_High
		

def close():
    print("gpios cleanup")
    GPIO.cleanup()
