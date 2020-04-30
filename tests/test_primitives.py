from ocvproto.primitives.legend import Legend
from ocvproto.toolbox import Canvas


def test_wm(tmpdir):
    legend = Legend(['a', 'b', 'c'])
    legend.put_on(Canvas())

    assert legend.labels == {'a': (119, 134, 45), 'b': (83, 102, 172), 'c': (45, 197, 210)}
