from unittest.mock import MagicMock

from ocvproto.toolbox import Application, Key


def test_application(tmpdir, monkeypatch):

    app1 = Application()  # no config test
    app1.config_load()
    app1.config_save()

    app2 = Application(config=tmpdir / 'some.json')

    log = []

    def hook_save(config):
        log.append('save')

    def hook_load(config):
        log.append('load')

    app2.hook_register('config_save', hook_save)
    app2.hook_register('config_load', hook_load)

    app2.config_save()
    app2.config_load()

    assert log == ['save', 'load']

    log.clear()

    from ocvproto.backend import cv
    monkeypatch.setattr(cv, 'waitKey', MagicMock())

    def loop_func():
        log.append('triggered')
        len_log = len(log)

        if len_log == 1:
            cv.waitKey.return_value = 115

        elif len_log == 3:
            cv.waitKey.return_value = Key.ESC

    app2.set_loop_func(loop_func)

    for _ in app2.loop():
        pass

    assert log == ['triggered', 'save', 'triggered']
