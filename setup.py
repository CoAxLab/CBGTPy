from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import glob

cwd = os.getcwd()
cwd = os.path.dirname(cwd)

extensions_nchoice = [Extension(name="agent_timestep_plasticity", 
    sources=
    [cwd+"/nchoice/"+'agent_timestep_plasticity.pyx',
    ],
)]

extensions_stop = [Extension(name="agent_timestep_stop_signal", 
    sources=
    [cwd+"/stopsignal/"+'agent_timestep_stop_signal.pyx',
    ],
)]

setup(
    name='nchoice',
    ext_modules=cythonize(extensions_nchoice,build_dir="./"),
    zip_safe=False,
)

setup(
    name='stopsignal',
    ext_modules=cythonize(extensions_stop,build_dir="./"),
    zip_safe=False,
)

so_files = glob.glob(cwd+"/notebooks/"+"*.so")
for sf in so_files:
    print(sf)
    if "plasticity" in sf:
        os.replace(sf, cwd+"/nchoice/agent_timestep_plasticity.so")
    elif "stop_signal" in sf:
        os.replace(sf, cwd+"/stopsignal/agent_timestep_stop_signal.so")
        
pyd_files = glob.glob(cwd+"/notebooks/"+"*.pyd")
for sf in pyd_files:
    print(sf)
    if "plasticity" in sf:
        os.replace(sf, cwd+"/nchoice/agent_timestep_plasticity.pyd")
    elif "stop_signal" in sf:
        os.replace(sf, cwd+"/stopsignal/agent_timestep_stop_signal.pyd")