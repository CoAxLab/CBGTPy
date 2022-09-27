from setuptools import setup
from Cython.Build import cythonize

setup(
    name='plasticity',
    ext_modules=cythonize("agent_timestep_plasticity.pyx"),
    zip_safe=False,
)

setup(
    name='stop signal',
    ext_modules=cythonize("agent_timestep_stop_signal.pyx"),
    zip_safe=False,
)