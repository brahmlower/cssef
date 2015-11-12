from distutils.core import setup

setup(
	name = 'Cyber Security Scoring Engine Framework',
	version = '0.0.1',
	py_modules = ['cssef'],
	install_requires = ['python-daemon >= 1.6','celery >= 3.1.19', 'sqlalchemy >= 0.9.8']
)
