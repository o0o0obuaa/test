"""
Common utils.

@author: chunk
chunkplus@gmail.com
2014 Dec
"""
__author__ = 'hadoop'

import os, sys
import time
import StringIO
import ConfigParser

import numpy as np

package_dir_imager = os.path.dirname(os.path.abspath(__file__))


class Timer():
    def __init__(self):
        self.__newtime = time.time()
        self.__oldtime = self.__newtime

    def mark(self):
        self.__oldtime = self.__newtime
        self.__newtime = time.time()
        return self.__newtime - self.__oldtime

    def report(self):
        print "%-24s%fs" % ("time elapsed:", self.mark())


def ttimer():
    newtime = time.time()
    while True:
        oldtime = newtime
        newtime = time.time()
        yield newtime - oldtime


def ctimer():
    newtime = time.clock()
    while True:
        oldtime = newtime
        newtime = time.clock()
        yield newtime - oldtime


def ski2cv(img):
    if img.ndim >= 3 and img.shape[2] >= 3:
        img[:, :, [0, 2]] = img[:, :, [2, 0]]
        return img


def get_env_variable(var_name, default=False):
    """
    Get the environment variable or return exception
    :param var_name: Environment Variable to lookup

    Ref - http://stackoverflow.com/questions/21538859/pycharm-set-environment-variable-for-run-manage-py-task
    (c) rh0dium
    2015 Jan
    """
    try:
        return os.environ[var_name]
    except KeyError:
        import StringIO
        import ConfigParser

        res_envfile = os.path.join(package_dir_imager, 'res', '.env')
        env_file = os.environ.get('PROJECT_ENV_FILE', res_envfile)
        try:
            config = StringIO.StringIO()
            config.write("[DATA]\n")
            config.write(open(env_file).read())
            config.seek(0, os.SEEK_SET)
            cp = ConfigParser.ConfigParser()
            cp.readfp(config)
            value = dict(cp.items('DATA'))[var_name.lower()]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name, value)
            return value
        except (KeyError, IOError):
            if default is not False:
                return default
            from django.core.exceptions import ImproperlyConfigured

            error_msg = "Either set the env variable '{var}' or place it in your " \
                        "{env_file} file as '{var} = VALUE'"
            raise ImproperlyConfigured(error_msg.format(var=var_name, env_file=env_file))

            # Make this unique, and don't share it with anybody.
            # e.g. SECRET_KEY = get_env_variable('SECRET_KEY')


def load_env(default=False):
    res_envfile = os.path.join(package_dir_imager, 'res', '.env')
    env_file = os.environ.get('PROJECT_ENV_FILE', res_envfile)
    try:
        config = StringIO.StringIO()
        config.write("[DATA]\n")
        config.write(open(env_file).read())
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
        for var_name, value in dict(cp.items('DATA')).items():
            # print var_name,value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name.upper(), value)
    except (KeyError, IOError):
        if default is not False:
            return default
        from django.core.exceptions import ImproperlyConfigured

        error_msg = "Either set the env variable '{var}' or place it in your " \
                    "{env_file} file as '{var} = VALUE'"
        raise ImproperlyConfigured(error_msg.format(var='load_env', env_file=env_file))


def bytes2bits(arry_bytes):
    """
    :param arry_bytes: 1-D np.unit8 array
    :return: 1-D 0/1 array
    """
    hid_data_bits = [map(int, '{0:08b}'.format(byte)) for byte in arry_bytes]
    return np.array(hid_data_bits).ravel()


def bits2bytes(arry_bits):
    """
    :param arry_bits: 1-D 0/1 array
    :return: 1-D np.unit8 array
    """
    str_bits = ''.join(map(str, arry_bits))
    arry_bytes = [int(str_bits[i:i + 8], 2) for i in range(0, len(str_bits), 8)]
    return np.array(arry_bytes, dtype=np.uint8).ravel()


def test_grammer():
    a = 'fsaf'
    b = ['dasf', 'dff']
    c = 'dgfsfdg'
    # print a + b
    print [a] + b  # ['fsaf', 'dasf', 'dff']
    print [a] + [b]  # ['fsaf', ['dasf', 'dff']]
    print [a] + [c]  # ['fsaf', 'dgfsfdg']


if __name__ == '__main__':
    timer = Timer()

    timer.mark()
    timer.report()

    timer.mark()
    time.sleep(1)
    # for i in range(1000000):
    # print i
    timer.report()

    # load_env()
    # print os.environ
    # print os.getenv('SPARK_HOME')















