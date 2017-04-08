import os
from datetime import datetime
import time
import pytweening

def timed_range(start, stop, duration, easing_func=lambda t: t):
    """Generator function for a timed range on an easing function

    Returns a generator that eases from start to stop along the curve specified
    by the easing_func, taking a total duration of duration.
    """
    t_start = datetime.now()
    y_span = stop - start
    t = (datetime.now() - t_start).total_seconds()
    t_scaled = 1 - (duration - t) / duration
    i = easing_func(t_scaled) * y_span + start

    while t_scaled < 1:
        i = easing_func(t_scaled) * y_span + start
        t = (datetime.now() - t_start).total_seconds()
        t_scaled = 1 - (duration - t) / duration
        yield i

class AcpiBacklightControl(object):
    default_dir = '/sys/class/backlight/intel_backlight'


    def __init__(self, dir=None, time_sleep=0.01):
        """__init__

        :param dir: The directory containing the acpi files
        :param time_sleep: The time to time.wait() to prevent busy waiting
        """
        self.dir = dir or self.default_dir
        self.time_sleep = time_sleep

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        return self.close()

    def open(self):
        # first store the maximum
        max_file_path = os.path.join(self.dir, 'max_brightness')
        with open(max_file_path, 'r') as max_file:
            self._max = int(max_file.read().strip())

        # now open and keep open the brightness file
        brightness_file_path = os.path.join(self.dir, 'brightness')
        self.brightness_file = open(brightness_file_path, mode='r+')

    def close(self):
        return self.brightness_file.close()

    @property
    def max(self):
        return self._max

    @property
    def brightness(self):
        self.brightness_file.seek(0)
        return int(self.brightness_file.read().strip())

    @brightness.setter
    def brightness(self, new_brightness):
        if new_brightness > self.max:
            raise ValueError('Brightness must be in range 0 to {} for this device'.format(self.max))

        self.brightness_file.seek(0)
        new_brightness = str(int(new_brightness))
        self.brightness_file.write(new_brightness)

        # not sure if I need to flush the file or not...

    def animate(self, new_brightness, duration=0.25, easing_func=pytweening.easeOutCubic):
        """Adjusts backlight brightness to new_brightness with an animation

        Default animation is easeOutCubic over 0.25s duration
        """
        anim_range = timed_range(self.brightness, new_brightness, duration, easing_func)
        for i in anim_range:
            self.brightness = i
            # avoid busy waiting on time in the generator
            time.sleep(self.time_sleep)
