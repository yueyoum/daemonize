from distutils.core import setup

VERSION = '0.2.4'

setup(
    name = 'daemonized',
    version = VERSION,
    py_modules = ['daemonized'],
    author = 'Wang Chao',
    author_email = 'yueyoum@gmail.com',
    url = 'https://github.com/yueyoum/daemonize',
    description = 'A Module to help you daemonize your program in Unix-like system',
    long_description = open('README.md').read(),
)
