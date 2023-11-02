from fhict_cb_01.custom_telemetrix import CustomTelemetrix
import time, sys

board = CustomTelemetrix()

RED = 4
GREEN = 5
BUZZER = 3

def setup():
    board.displayOn()
    board.set_pin_mode_digital_output(RED)
    board.set_pin_mode_digital_output(GREEN)
    board.set_pin_mode_analog_output(BUZZER)

def timer_count():
    global baking_time
    baking_time = float(input("Baking time: "))
    baking_time_seconds = baking_time * 60
    while baking_time_seconds > -1:
        board.digital_write(RED, 1)
        time.sleep(1)
        board.displayShow(int(baking_time_seconds))
        print(baking_time_seconds)
        baking_time_seconds -= 1  
    board.digital_write(RED, 0)
    board.digital_write(GREEN, 1)
    buzzer()

def buzzer():
    i = 0
    while i < 4:
        board.analog_write(BUZZER, 1)
        time.sleep(0.3)
        board.analog_write(BUZZER, 0)
        time.sleep(0.3)
        i += 1

def main():
    while True:
        try:
            setup()
            timer_count()
        except KeyboardInterrupt:
            board.displayOff()
            board.digital_write(GREEN, 0)
            print("\n Shutdown...")
            sys.exit()

main()