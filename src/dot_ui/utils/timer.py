import time

class Timer:
    timers = {}
    autoprint = False

    def start(name):
        Timer.timers[name] = {'start': time.perf_counter()}
    
    def stop(name, print=None):
        try:
            Timer.timers[name]['stop'] = time.perf_counter()
            if (Timer.autoprint and print is None) or (print == True):
                Timer.print(name)
        except KeyError:
            print(f"Timer \"{name}\" has not been started")
    
    def time(name):
        try:
            return Timer.timers[name]['stop'] - Timer.timers[name]['start']
        except KeyError:
            if not name in Timer.timers:
                print(f"Timer \"{name}\" has not been started")
            else:
                print(f"Timer \"{name}\" has not been stopped")

    def print(name):
        print(f"{name} timed at {Timer.time(name)} seconds")