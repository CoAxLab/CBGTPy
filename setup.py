from setuptools import setup
from Cython.Build import cythonize

setup(
    name='nchoice',
    ext_modules=cythonize("../nchoice/agent_timestep_plasticity.pyx"),
    zip_safe=False,
)

setup(
    name='stopsignal',
    ext_modules=cythonize("../stopsignal/agent_timestep_stop_signal.pyx"),
    zip_safe=False,
)