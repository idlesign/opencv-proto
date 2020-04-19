Quickstart
==========

Color Palette
~~~~~~~~~~~~~

Let's replace 37 lines of source code from `Trackbar as the Color Palette <https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_trackbar/py_trackbar.html>`_
tutorial with ``ocvproto``-based implementation:

.. code-block:: python

    from ocvproto.toolbox import WindowManager, Canvas

    with WindowManager() as wm:
        # Window manager will create a default window for us if none provided.
        # Default window is available through .window property.

        # With the help of .add_trackbar_group() we create three trackbars,
        # to adjust our color values for R, G and B. Batch apply `max` value
        # to all three trackbars.
        rgb = wm.window.add_trackbar_group(['R', 'G', 'B'], max=255)

        # If one doesn't configure their own Application object,
        # Window manager will instantiate one automatically, using default settings.
        for _ in wm.app.loop():
            # Most of the time we'll need a loop to process our frames.
            # Application object (available through .app property) offers us such a loop.

            # Lastly we create a canvas object using RGB value from trackbars,
            # and pass its' frame to .set_frame() shortcut.
            # That shortcut puts the frame into default window.
            wm.set_frame(Canvas(512, 300, color=rgb).frame)


Camera capture
~~~~~~~~~~~~~~

Now let's capture video camera stream into ``ocvproto.avi`` file, being able to adjust blur.

Let's also setup config filepath (``ocvproto.json``) - this allows us to store current trackbar values
(``s`` key) and load them (``r`` key). It is useful to restore settings between sessions.

.. code-block:: python

    from ocvproto.toolbox import WindowManager, Camera

    with WindowManager() as wm:

        # We create two trackbars to adjust blur.
        blur = wm.window.add_trackbar_group(['x', 'y'], 'Blur', default=1)

        # We instruct our application to store settings into file.
        wm.app.set_config('ocvproto.json')

        # We initiate default (first available) camera connection.
        with Camera() as cam:
            for _ in wm.app.loop():
                # Read a frame from camera, we'll work with.
                cam.read()

                # Now we blur that frame.
                cam.blur(blur)

                # And we write the frame into the file.
                # If dumping parameters were not set up before
                # .write() shortcut will use defaults
                # (e.g. `ocvproto.avi` name, XVID codec).
                cam.write()

                # Show the frame.
                wm.set_frame(cam.frame)

