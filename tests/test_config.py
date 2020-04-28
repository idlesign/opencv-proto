from ocvproto.toolbox import Config


def test_config(tmpdir):

    fpath = tmpdir / 'some.json'

    conf = Config(fpath)
    conf.load()

    assert conf.get_data('key', 'some') == 'some'

    conf.set_data('key', 'val')
    conf.save()

    conf = Config(fpath)
    conf.load()
    assert conf.get_data('key') == 'val'
