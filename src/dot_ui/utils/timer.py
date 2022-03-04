import time

class Timer:
    timers = {}
    autoprint = False

    def start(name):
        Timer.timers[name] = {'start': time.perf_counter()}
    
    def stop(name, print=None):
        Timer.timers[name]['stop'] = time.perf_counter()
        if (Timer.autoprint and print is None) or (print == True):
            Timer.print(name)
    
    def time(name):
        return Timer.timers[name]['stop'] - Timer.timers[name]['start']

    def print(name):
        print(f"{name} timed at {Timer.time(name)} seconds")