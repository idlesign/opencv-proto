import pytest

from ocvproto.toolbox import WindowManager, Window, Application, Canvas, Trackbar


@pytest.mark.skip(reason='UI backend may be unavailable')
def test_wm(tmpdir):

    with WindowManager() as wm:

        app = wm.app
        assert isinstance(app, Application)
        app.set_config(tmpdir / 'wm_conf.json')

        win = wm.window
        assert isinstance(win, Window)

        a, b = win.add_trackbar_group(2, prefix='common')
        a.set_keys('[]')
        assert isinstance(a, Trackbar)
        assert isinstance(b, Trackbar)
        assert a.name == 'common 1'
        assert b.name == 'common 2'

        c, d = win.add_trackbar_group(['x', {'default': 20}])
        assert isinstance(c, Trackbar)
        assert isinstance(d, Trackbar)
        assert c.name == 'x'
        assert d.name == '2'

        wm.bind_trackbar_keys()

        app.config_save()
        app.config_load()

        canvas = Canvas()
        wm.set_frame(canvas)
        wm.render()
