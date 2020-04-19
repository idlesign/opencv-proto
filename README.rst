opencv-proto
============
https://github.com/idlesign/opencv-proto

|release| |lic|  |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/opencv-proto.svg
    :target: https://pypi.python.org/pypi/opencv-proto

.. |lic| image:: https://img.shields.io/pypi/l/opencv-proto.svg
    :target: https://pypi.python.org/pypi/opencv-proto

.. |ci| image:: https://img.shields.io/travis/idlesign/opencv-proto/master.svg
    :target: https://travis-ci.org/idlesign/opencv-proto

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/opencv-proto/master.svg
    :target: https://coveralls.io/r/idlesign/opencv-proto


**Work in progress. Stay tuned.**

Description
-----------

*Allows fast prototyping in Python for OpenCV*

Offers primitives and simplified interfaces to streamline prototypes construction in Python.

Facilitates:

* Windows construction and management
* Trackbar construction
* Configuration save/load (including trackbar values)
* Key binding (e.g. for trackbar control, configuration save/load)
* Video capturing and modification
* Work with images
* Work with text
* Frames transformation


Samples
-------

Color Palette
~~~~~~~~~~~~~

Let's replace 37 lines of source code from `Trackbar as the Color Palette <https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_trackbar/py_trackbar.html>`_
tutorial with ``ocvproto``-based implementation:

.. code-block:: python

    from ocvproto.toolbox import WindowManager, Canvas

    with WindowManager() as wm:
        rgb = wm.window.add_trackbar_group(['R', 'G', 'B'], max=255)
        for _ in wm.app.loop():
            wm.set_frame(Canvas(512, 300, color=rgb).frame)


Camera capture
~~~~~~~~~~~~~~

Now let's capture video camera stream into ``ocvproto.avi`` file, being able to adjust blur.

Let's also setup config filepath (``ocvproto.json``) - this allows us to store current trackbar values
(``s`` key) and load them (``r`` key). It is useful to restore settings between sessions.

.. code-block:: python

    from ocvproto.toolbox import WindowManager, Camera

    with WindowManager() as wm:

        blur = wm.window.add_trackbar_group(['x', 'y'], 'Blur', default=1)
        wm.app.set_config('ocvproto.json')

        with Camera() as cam:
            for _ in wm.app.loop():
                cam.read()
                cam.blur(blur)
                cam.write()
                wm.set_frame(cam.frame)


Read the documentation.

Requirements
------------
* Python 3.6+
* ``opencv-python`` (or variants)


Documentation
-------------

https://opencv-proto.readthedocs.org/
