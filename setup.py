from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("agent_timestep.pyx"),
    zip_safe=False,
)