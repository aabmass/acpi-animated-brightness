#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import pytweening
from .acpibacklight import AcpiBacklightControl

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
    type=float,
    default=0.25,
    help='The duration for the action to take effect over. Only taken '
         'into account on set, inc, and dec operations.'
)
parser.add_argument(
    '--easing-function',
    '-e',
    default='easeOutCubic',
    choices=['easeInBack', 'easeInBounce', 'easeInCirc', 'easeInCubic',
        'easeInElastic', 'easeInExpo', 'easeInOutBack', 'easeInOutBounce',
        'easeInOutCirc', 'easeInOutCubic', 'easeInOutElastic',
        'easeInOutExpo', 'easeInOutQuad', 'easeInOutQuart',
        'easeInOutQuint', 'easeInOutSine', 'easeInQuad', 'easeInQuart',
        'easeInQuint', 'easeInSine', 'easeOutBack', 'easeOutBounce',
        'easeOutCirc', 'easeOutCubic', 'easeOutElastic', 'easeOutExpo',
        'easeOutQuad', 'easeOutQuart', 'easeOutQuint', 'easeOutSine',
        'linear'],
    metavar='EASING_FUNC',
    help='The easing function used for animations. This program uses '
         'PyTweening so use the function names from PyTweening e.g. '
         '"easeOutCubic" or "easeInOutQuad".'
)
args = parser.parse_args()

with AcpiBacklightControl() as control:

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
