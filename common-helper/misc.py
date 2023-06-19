import os
import subprocess
import tldextract
import calendar
import logging
from hashlib import sha256
from datetime import datetime


logger = logging.getLogger('utils.misc')


def timestamp_to_utcdatetime(ts):
    try:
        return datetime.utcfromtimestamp(float(ts))
    except:
        return None


def timestamp_to_datetime(ts):
    try:
        return datetime.fromtimestamp(ts)
    except:
        return None


def utcdatetime_to_timestamp(dt):
    return calendar.timegm(dt.utctimetuple())


def timestamp_to_string(ts, fmt=None):
    dt = timestamp_to_datetime(ts)

    if dt is None:
        return None

    if fmt is None:
        fmt = '%Y%m%d%H%M%S'

    return dt.strftime(fmt)


def timestring_to_timestamp(ts, fmt=None):
    if not fmt:
        fmt = '%Y%m%d%H%M%S'

    dt = datetime.strptime(ts, fmt)

    return int(datetime.timestamp(dt))


def cmd(s, **kwargs):
    logger.info("executing command: %s", s)
    subprocess.check_call(s, **kwargs)


def cmd2(s):
    logger.info("executing command: %s", s)
    os.system(s)


def get_sld(domain):
    sld = tldextract.extract(domain).registered_domain
    return sld


def sha256sum(string):
    return sha256(string.encode('utf-8')).hexdigest().upper()


def is_int(string):
    try:
        int(string)
        return True
    except:
        return None


def get_file_row_count(_file_path):
    count = 0
    with open(_file_path, 'r') as fd:
        for _ in fd:
            count += 1

    return count


def split_file(_file_path, count):
    _row_count = get_file_row_count(_file_path)
    _l = int(_row_count / count)

    _dir = os.path.dirname(_file_path)
    _base = os.path.basename(_file_path)

    string = 'cd %s && split -l%s %s %s.' % (_dir, _l, _base, _base)
    cmd2(string)

    _files = []
    for _file in os.listdir(_dir):
        _p = os.path.join(_dir, _file)
        if _p == _file_path:
            continue

        if not _file.startswith(_base):
            continue

        _files.append(_p)

    return _files


def mkdir(_path):
    logger.info('mkdir %s', _path)
    os.makedirs(_path, exist_ok=True)


def clear_path(_path):
    cmd(['rm', '-rf', _path])


def rename_file(from_file, to_file):
    logger.info('renaming %s -> %s', from_file, to_file)
    os.rename(from_file, to_file)


def move_file(from_file, to_directory):
    cmd(['mv', from_file, to_directory])


def copy_file(from_file, to_directory):
    cmd(['cp', from_file, to_directory])


def tar_directory(_directory, _target):
    cmd(['tar', '-zcvf', _target, '-C', _directory, '.'])


def untar_package(_package, _directory):
    cmd(['tar', 'zxvf', _package, '-C', _directory])
