import time, sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix


BUTTON1 = 8

level = 0
prevLevel = 0
timer_running = False
start_time = 0
board = CustomTelemetrix()

RED = 4
GREEN = 5
BUZZER = 3

def ButtonChanged(data):
    global level, timer_running, start_time
    level = data[2]
    if level == 0:
        if timer_running:
            timer_running = False  
        else:
            timer_running = True
            start_time = time.time()
            timer_count()

def setup():
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTON1, callback=ButtonChanged)
    board.set_pin_mode_digital_output(RED)
    board.set_pin_mode_digital_output(GREEN)
    board.set_pin_mode_analog_output(BUZZER)

def timer_count():
    global timer_running, start_time
    baking_time_seconds = 0.1 * 60  # 15 minutes in seconds
    while baking_time_seconds > -1 and timer_running:
        board.digital_write(RED, 1)
        time.sleep(1)
        board.displayShow(int(baking_time_seconds))
        print(baking_time_seconds)
        baking_time_seconds -= 1
    board.digital_write(RED, 0)
    board.digital_write(GREEN, 1)
    buzzer()
    board.digital_write(GREEN, 0)

def buzzer():
    i = 0
    while i < 4:
        board.analog_write(BUZZER, 1)
        time.sleep(0.3)
        board.analog_write(BUZZER, 0)
        time.sleep(0.3)
        i += 1

def loop():
    global prevLevel
    if prevLevel != level:
        print(level)
        prevLevel = level

def main():
    setup()
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            board.displayOff()
            print("\nShutdown...")
            sys.exit()

if __name__ == "__main__":
    main()
