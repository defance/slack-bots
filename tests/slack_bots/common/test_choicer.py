import os
from unittest import mock

from slack_bots.common.choicer import RandomChoicer


def test_choicer_without_params():
    choicer = RandomChoicer('foo.txt')
    cwd = os.getcwd()
    assert choicer.file == f'{cwd}/data/foo.txt'
    assert choicer.cache_file == f'{cwd}/cache/used.foo.txt'


def test_choicer_with_complex_file_name():
    choicer = RandomChoicer('path/foo.txt')
    cwd = os.getcwd()
    assert choicer.file == f'{cwd}/data/path/foo.txt'
    assert choicer.cache_file == f'{cwd}/cache/path/used.foo.txt'


def test_choicer_selected_is_saved(mocker):
    mocker.patch('slack_bots.common.choicer.read_all_lines', side_effect=[
        ['foo'],
        [],
    ])
    write = mocker.patch('slack_bots.common.choicer.write_all_lines')
    choicer = RandomChoicer('foo.txt')
    selected = choicer.select()
    assert selected == 'foo'
    write.assert_called_with(mock.ANY, {'foo'})


def test_choicer_last_variant_saves_full_cache(mocker):
    mocker.patch('slack_bots.common.choicer.read_all_lines', side_effect=[
        ['foo', 'bar'],
        ['bar'],
    ])
    write = mocker.patch('slack_bots.common.choicer.write_all_lines')
    choicer = RandomChoicer('foo.txt')
    selected = choicer.select()
    assert selected == 'foo'
    write.assert_called_with(mock.ANY, {'foo', 'bar'})


def test_choicer_full_cache_is_refreshed(mocker):
    mocker.patch('slack_bots.common.choicer.read_all_lines', side_effect=[
        ['foo', 'bar'],
        ['foo', 'bar'],
    ])
    write = mocker.patch('slack_bots.common.choicer.write_all_lines')
    choicer = RandomChoicer('foo.txt')
    selected = choicer.select()
    call = write.call_args_list[0]
    assert mock.call(mock.ANY, {selected}) == call
