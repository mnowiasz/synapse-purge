from setuptools import setup

setup (
    name='synapse-purge',
    version='0.0.1',
    packages='synapsepurge',
    url='https://github.com/mnowiasz/synapse-purge',
    license='MIT',
    author='Mark Nowiasz',
    author_email='buckaroo+synapsepurge@midworld.de',
    description='purge old room events from your homeserver',
    install_requires = [
        'matrix-nio>=0.6.0',
        'psycog2'
    ],
    entry_points={
        'console_scripts': ['purge=synapsepurge:purge'],
    }
)