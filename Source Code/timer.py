import asyncio
import time

class Timer:
    """
    Class for setting timers to trigger event after a given time period. Timer automatically re-starts after triggering event

    Methods:
    start - start the timer
    reset - resets the timer setting the start_ticks to current time
    stop - stops the timer

    Attributes:
    timer_seconds (int) - number of seconds to wait before triggering the event
    timer_event (asyncio.Event) - event to trigger when the timer period has elapsed
    check_period (int) - number of seconds to wait in-between each check of elapsed time
    """

    def __init__(self, timer_event, timer_seconds, check_period):
        """
        Initialize the timer

        timer_event (asyncio.Event) - event to trigger when the timer period has elapsed
        timer_seconds (int) - number of seconds to wait before triggering event
        check_period (int) - number of seconds to wait in-between each check of elapsed time
        """
        self.timer_event = timer_event
        self.timer_seconds = timer_seconds
        self.check_period = check_period
        self._running = False
    
    @property
    def timer_seconds(self):
        return self._timer_seconds
    
    @timer_seconds.setter
    def timer_seconds(self, value):
        self._timer_seconds = value
        self._timer_ms = value * 1000
    
    async def _run(self):
        """
        Internal method to wait and trigger event
        """
        while self._running:
            # Determine if desired time has elapsed
            if time.ticks_diff(time.ticks_ms(),self._start_ticks) >= self._timer_ms:
                # Set the event and reset the timer
                self.timer_event.set()
                self._start_ticks = time.ticks_ms()
            
            # Sleep until next checkpoint
            await asyncio.sleep(self.check_period)
    
    def start(self):
        """
        Start the timer
        """
        # Set start ticks
        self._start_ticks = time.ticks_ms()

        # Start the run task
        self._running = True
        asyncio.create_task(self._run())
    
    def reset(self):
        """
        Reset the start timer
        """
        self._start_ticks = time.ticks_ms()
    
    def stop(self):
        """
        Stop the timer
        """
        self._running = False