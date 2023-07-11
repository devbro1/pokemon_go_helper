from screen_controller import ScreenController
import time

def main():
    screen_reader = ScreenController()
    sleep_duration = 0.3
    for i in range(1500,2350):
        screen_reader.pressFight(1)
        time.sleep(sleep_duration)
        screen_reader.pressFight(2)
        time.sleep(sleep_duration)
        screen_reader.pressFight(3)
        time.sleep(sleep_duration)

main()
