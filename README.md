# CBGTPy: An extensible cortico-basal ganglia-thalamic framework for modeling biological decisions
Matthew Clapp Jyotika Bahuguna Cristina Giossi, Jonathan E. Rubin, Timothy Verstynen, Catalina Vich

ABSTRACT: Here we introduce CBGTPy, a virtual environment for designing and testing goal-directed agents with internal dynamics that are modeled off of the cortico-basal-ganglia-thalamic (CBGT) pathways in the mammalian brain, including a physiologically-realistic implementation of dopamine-driven synaptic plasticity. CBGTPy enables researchers to investigate the internal dynamics of the CBGT system during a variety of tasks, allowing for the formation of testable predictions about animal behavior and neural activity. The framework has been designed around the principle of flexibility, such that many experimental parameters in a decision-making paradigm can be easily defined and modified. Here we demonstrate the capabilities of CBGTPy across a range of single and multi-choice tasks, highlighting the ease of set up and the biologically realistic behavior that it produces. We show that CBGTPy is extensible enough to apply to a wide range of experimental protocols and to allow for the implementation of model extensions with minimal developmental effort. 

# Below are the instructions to create a conda environment, install all the dependencies required to run CBGTPy and run notebooks.

## Dependencies.
   * Python 3.8+ (This only needs attention if the user is using Python version < 3, e.g. 2.7. In case, Python version > 3 is been used, the installation script will install the correct version of Python and other dependencies)
   * gcc (already installed in Linux by default, but not in Mac)
   * Xcode (Mac users)
   * CLT  (Mac users)

Xcode and CLT (for Mac users) can be installed by running this on the command line:
   
   	$ xcode-select --install
   
gcc (for Mac users) can be installed by running this on commad line:

     	$ brew install gcc


## Install conda on your machine.
* Download from here https://docs.conda.io/projects/miniconda/en/latest/
	
* Change the directory to where the executable file was downloaded:

  		$ cd <directory where executable was downloaded>
  	
* In the directory, where the executable file (eg. Miniconda3-latest-MacOSX-x86_64.sh) is downloaded, type the following on your command line:

	* Mac
 
			$ bash Miniconda3-latest-MacOSX-x86_64.sh
 	* Linux
  
   			$ bash Miniconda3-latest-Linux-x86_64.sh


## Download CBGTPy-main folder.
	
 	$  git clone https://github.com/CoAxLab/CBGTPy.git

 * Change the directory:

		$ cd CBGTPy
  	

## Create a conda environment by typing the following on the command line. Choose an environment name, e.g. cbgtpy_env.
	$ conda create -n <env name> python=3.8 pyyaml
	
E.g., if the <env name> is "cbgtpy_env", then use:
 
	$ conda create -n cbgtpy_env python=3.8 pyyaml
 
## Activate the conda environment.
	$ conda activate cbgtpy_env
 or 
  	
   	$ source activate cbgtpy_env
   
## Run the installation file. 

You will be asked which multiprocessing library you want to install. Although "ray" is the recommended version, it may cause problems on some machines.
Hence CBGTPy is designed to use the default Python multiprocessing APIs, that need a third-party library (pathos). Pathos is installed by default. 
You can choose to install ray by typing "y" to the prompted question. If "n" is typed, ray will not be installed. 
Some basic benchmarking for the three options - (a) no multiprocessing (b) with pathos (c) with ray - are stated below.
	
* For 5 simulations, 3 trials each on an Apple M1 machine with OS Ventura 13.2.1:
 (a) none: 664s; (b) pathos: 331s; (c) ray:  266s.
  	
* For 5 simulations, 3 trials each on a 11th Gen Intel Core(TM) i7-11800H with Windows 10:
 (a) none: 525s; (b) pathos: 386s; (c) ray: 232s.

		$ python install.py <env name>

	* For the environment name cbgtpy_env:

  			$ python install.py cbgtpy_env
 
## Test by running:
	$ ipython

* On the ipython prompt:

 		$ import pathos

## If there is an error, deactivate and activate the conda environment again.

## If you plan to use "ray", start the ray server as described below. If not, skip this step.
* On the shell prompt:

		$ ray start --head --port=6379 --redis-password="cbgt2"
  
* The above line should be sufficient to start the ray server. In case is not, it would give back the machine IP. The machine IP could be used in the following command:

  		$ ray start --address='< machine ip>:6379' --redis-password='cbgt2'
    
  For e.g. for IP 192.168.1.167:

  		$ ray start --address='192.168.1.167:6379' --redis-password='cbgt2'



## From the shell prompt, start jupyter notebooks. There are three example notebooks provided which can be executed from the jupyter notebook environment.
* network_simulation-n-choice.ipynb (Runs a n-choice task)
* network_simulation-stop-signal.ipynb (Runs a stop-signal task)
* network_simulation-n-choice-optostim.ipynb (Shows an example of optogenetic stimulation during a n-choice task)
 
		$ jupyter-notebook 
 	
  	or
  		
        	$ jupyter notebook

## If the libraries pathos and ray are not still visible (gives an error saying they are not found) in the jupyter notebook, then execute these commands at the beginning of the notebook.
	
        import sys
	import yaml
	with open('environment.yml') as f:
	    doc = yaml.safe_load(f)
	    
	sys.path.append(doc['prefix']+"/lib/python3.8/site-packages/")

## Only if you want to delete the conda environment !!!
	$ conda remove --name cbgtpy_env --all





