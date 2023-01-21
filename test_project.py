from project import startApp, generateHistory, openFile
import pytest

def test_startApp():
    with pytest.raises(SystemExit):
        startApp('-e')
    with pytest.raises(SystemExit):
        startApp('exe')

def test_generateHistory():
    with pytest.raises(SystemExit):
        generateHistory('yes')
    with pytest.raises(SystemExit):
        generateHistory('n')
    with pytest.raises(SystemExit):
        generateHistory('No')


def test_openFile():
    with pytest.raises(SystemExit):
        openFile('yes')
    with pytest.raises(SystemExit):
        generateHistory('n')
    with pytest.raises(SystemExit):
        generateHistory('No')