#import setuptools
#import pkg_resources
import os 
from subprocess import run
import yaml
 
#import conda.cli.python_api as Conda

required  = ['matplotlib','numpy','scipy','pandas', 'seaborn','cython','pathos'] 



#installed = [pkg.key for pkg in pkg_resources.working_set]

print("What packaged would you like to install for multiprocessing?")
print("The default mode (none) is single threaded mode, which may not be optimal for heavy simulations \n")

multi_pck = input("There are two options: pathos and ray. The CBGTPy has been modified to run on both packages. Pathos is installed by default. Do you want to install ray? (n/y):  ")
if multi_pck == "y":
    #required.add(multi_pck)
    required.append("ray")

os.system("conda env export --name cbgtpy_env --file environment.yml")

# Add the rest of the packages
with open('environment.yml') as f:
    doc = yaml.safe_load(f)

# Make a new dictionary, but where every key is a dictionary in order to include the pip list
doc_new = dict()
for k in doc.keys():
    if k == "dependencies":
        doc_new[k] = dict()
    else:
        doc_new[k] = []

for k in doc.keys():
    doc_new[k] = doc[k]



for r in required:
    if r== "ray":
        doc_new['dependencies'].append({'pip':[]})
        doc_new['dependencies'][-1]['pip'].append('ray')
    else:
        doc_new['dependencies'].append(r)

doc_new['dependencies'].append('ipykernel')

with open('environment.yml', 'w') as file:
        yaml.dump(doc_new,file,sort_keys=False)


prefix = doc_new['prefix']
os.system("conda env update --prefix "+prefix+" --file environment.yml  --prune")


