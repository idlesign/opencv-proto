# Quickstart

## Color Palette

Let's replace 37 lines of source code from `Trackbar as the Color Palette`
tutorial with `ocvproto`-based implementation:

```python
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
        wm.set_frame(Canvas(512, 300, color=rgb))
```

## Camera capture

Now let's capture video camera stream into `ocvproto.avi` file, being able to adjust blur.

Let's also setup config filepath (`ocvproto.json`) — this allows us to store current trackbar values
(`s` key) and load them (`r` key). It is useful to restore settings between sessions.

We bind `z` key to take camera shots.

```python
from ocvproto.toolbox import WindowManager, Camera

with WindowManager() as wm:

    # Configure config file for trackbar values save/load.
    wm.app.set_config('ocvproto.json')

    # Register trackbars to adjust blur.
    blur = wm.window.add_trackbar_group(['x', 'y'], 'Blur', default=1)

    with Camera() as cam:
        # Bind `z` key to take camera shots.
        wm.app.bind_key('z', cam.dump_image)

        for _ in wm.app.loop():
            cam.read()
            cam.blur(blur)
            cam.dump()
            wm.set_frame(cam)
```
