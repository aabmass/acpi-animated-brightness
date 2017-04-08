acpibacklight
=============

|PyPI version|

A python library and script for changing brightness on Linux via acpi.
Allows for easing animations too!

.. code:: bash

    pip install acpibacklight

You can use the script ``acpi-ease-backlight`` to adjust the backlight
with easing via acpi on your device. See ``acpi-ease-backlight --help``
for options.

CLI Usage
---------

After installing via pip, use the script ``acpi-ease-backlight``. Here
is how you might use it:

.. code:: bash

    $ acpi-ease-backlight -h        # see help
    ...

    $ acpi-ease-backlight show      # show the current backlight value
    4000

    $ acpi-ease-backlight max       # show the your display's max backlight value
    4882

    $ acpi-ease-backlight set 2000  # set the backlight to 2000, over the default
                                    # duration of 0.25 seconds and using the default
                                    # easing function 'easeOutCubic'

    $ acpi-ease-backlight -d 1 -e easeInOutQuad set 3000
                                    # set the backlight to 3000 over duration of
                                    # 1 second, using the easing function 'easeInOutQuad'

    $ acpi-ease-backlight -d 0.5 dec 1000
                                    # decrease the current backlight value by
                                    # 1000 over a duration of 0.5 seconds

Library Usage
-------------

Use the class ``acpibacklight.AcpiBacklightControl`` for changing the
backlight level in various ways. ``AcpiBacklightControl`` is designed to
use python *with* statements similarly to file objects and python's
``open`` builtin:

.. code:: python

    with AcpiBacklightControl() as ctrl:
        # set the brightness without animating
        ctrl.brightness = 2000

        # get max brightness on this device
        new_brightness = ctrl.max

        # You can also use the animate function on the AcpiBacklightControl.
        # See the docstring for kwargs
        ctrl.animate(new_brightness, duration=0.75)

Alternatively, you can construct, then open, then close the
``AcpiBacklightControl``:

.. code:: python

    ctrl = AcpiBacklightControl()
    ctrl.open()
    ctrl.animate(ctrl.brightness - 1000)
    ctrl.close()

You can pass an easing function to be used in ``animate()`` by the
``easing_func`` keyword arg. This package uses
`PyTweening <https://github.com/asweigart/pytweening>`__ for its default
animation and the CLI, so you can easily pass one of those:

.. code:: python

    import pytweening
    ctrl.animate(2345, easing_func=pytweening.easeInOutBounce)

Finally, if you want to create and pass your own easing function, it
should take one paramater (time) between 0 and 1, and return a value
between 0 and 1. For instance, a linear easing function would look like:

.. code:: python

    def linear_easing(t):
      # t is always in the range [0, 1]
      return t

    # ...
    ctrl.animate(1234, easing_func=linear_easing)

.. |PyPI version| image:: https://badge.fury.io/py/acpibacklight.svg
   :target: https://badge.fury.io/py/acpibacklight
