import signal

def signal_handler(func):
    def handler(signum, frame):
        try:
            print("Caught signal " + str(signum))
            import sys
            func()
        except OSError as e:
            if e.errno != errno.EAGAIN:
                print('Signal handler write error')
                os._exit(1)
    signal.signal(signal.SIGINT, handler)
