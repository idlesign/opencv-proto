from ocvproto.toolbox import to_rgb, Canvas, Text


def test_to_rgb():

    assert to_rgb((0, 0, 0)) == (0, 0, 0)
    assert to_rgb('black') == (0, 0, 0)
    assert to_rgb(0) == (0, 0, 0)


def test_canvas():
    canvas = Canvas(color='red')
    assert canvas.height == 480


def test_text():
    canvas = Canvas()

    text = Text()
    text.put_on(canvas)
    text.put_on_demo(canvas)

