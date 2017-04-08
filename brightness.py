#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, timedelta
import time
import pytweening
import argparse

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

class AcpiBrightnessControl(object):
    default_dir = '/sys/class/backlight/intel_backlight'
    
    
    def __init__(self, dir=None):
        self.dir = dir or self.default_dir

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

    def animate(self, new_brightness, duration=0.25, easing_func=pytweening.easeOutCubic):
        """Adjusts backlight brightness to new_brightness with an animation
        
        Default animation is easeOutCubic over 0.25s duration
        """
        anim_range = timed_range(self.brightness, new_brightness, duration, easing_func)
        for i in anim_range:
            self.brightness = i
            # avoid busy waiting on time in the generator
            time.sleep(0.001)


def main():
    parser = argparse.ArgumentParser(description='Change and animate backlight brightness via acpi')
    parser.add_argument(
        'action',
        default='show',
        choices=['show', 'max', 'set', 'inc', 'dec'],
        metavar='action',
        help='The action that executes. One of "show", "max", "set", '
             '"inc", or "dec"'
    )
    parser.add_argument(
        'operand',
        nargs='?',
        type=int,
        help='The operand the action executes on.'
    )
    parser.add_argument(
        '--duration',
        '-d',
        type=int,
        default=0.25,
        help='The duration for the action to take effect over. Only taken '
             'into account on set, inc, and dec operations.'
    )
    parser.add_argument(
        '--easing-function',
        '-e',
        default='easeOutCubic',
        help='The easing function used for animations. This program uses '
             'PyTweening so use the function names from PyTweening e.g. '
             '"easeOutCubic" or "easeInOutQuad".'
    )
    args = parser.parse_args()

    with AcpiBrightnessControl() as control:

        if args.action == 'show':
            print(control.brightness)
        elif args.action == 'max':
            print(control.max)

        else:
            ## we will be animating so figure out params and call the function

            # all of these require an operand!
            if not args.operand:
                print(
                    'The {} action requires an operand!'.format(args.action),
                    file=sys.stderr
                )
                parser.print_usage(file=sys.stderr)
                sys.exit(1)


            # dynamically find the easing function or default
            easing_func = pytweening.easeOutCubic
            if hasattr(pytweening, args.easing_function):
                easing_func = getattr(pytweening, args.easing_function)
            else:
                print('No easing function {} found in PyTweening. '
                      'Defaulting to easeOutCubic.'.format(args.easing_function))

            new_brightness = control.brightness
            if args.action == 'set': 
                new_brightness = args.operand
            elif args.action == 'inc':
                new_brightness += args.operand
            elif args.action == 'dec':
                new_brightness -= args.operand

            control.animate(
                new_brightness,
                duration=args.duration,
                easing_func=easing_func
            )

if __name__ == "__main__":
    main()
