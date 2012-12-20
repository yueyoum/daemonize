from distutils.core import setup

setup(
    name = 'daemonized',
    version = '0.2.2',
    py_modules = ['daemonized'],
    author = 'Wang Chao',
    author_email = 'yueyoum@gmail.com',
    url = 'https://github.com/yueyoum/daemonize',
    description = 'A Module to help you daemonize your program in Unix-like system',
    long_description = open('README.txt').read(),
)
