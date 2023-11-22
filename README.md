# CBGTPy: An extensible cortico-basal ganglia-thalamic framework for modeling biological decisions
Matthew Clapp Jyotika Bahuguna Cristina Giossi, Jonathan E. Rubin, Timothy Verstynen, Catalina Vich

ABSTRACT: Here we introduce CBGTPy, a virtual environment for designing and testing goal-directed agents with internal dynamics that are modeled off of the cortico-basal-ganglia-thalamic (CBGT) pathways in the mammalian brain, including a physiologically-realistic implementation of dopamine-driven synaptic plasticity. CBGTPy enables researchers to investigate the internal dynamics of the CBGT system during a variety of tasks, allowing for the formation of testable predictions about animal behavior and neural activity. The framework has been designed around the principle of flexibility, such that many experimental parameters in a decision-making paradigm can be easily defined and modified. Here we demonstrate the capabilities of CBGTPy across a range of single and multi-choice tasks, highlighting the ease of set up and the biologically realistic behavior that it produces. We show that CBGTPy is extensible enough to apply to a wide range of experimental protocols and to allow for the implementation of model extensions with minimal developmental effort. 

# Below are the instructions to create a conda environment and install all the dependencies required to run CBGTPy


## Install conda on your machine
	* Download from here https://docs.conda.io/projects/miniconda/en/latest/
	
 	* Change the directory to where the executable file was donwloaded
  		$ cd <directory where executable was downloaded>
  	
   	*In the directory, where the executable file (eg. Miniconda3-latest-MacOSX-x86_64.sh) is downloaded, type the following on your command line

		* Mac. 

			$bash Miniconda3-latest-MacOSX-x86_64.sh
		* Linux
			$bash Miniconda3-latest-Linux-x86_64.sh


## Create a conda environment by typing the following on the command line 
	$conda create -n cbgtpy_env python=3.8 pyyaml
## Activate the conda environment
	$source activate cbgtpy_env
## Run the installation file. 
	*You will be asked which multiprocessing library do you want to install. Although "ray" is the recommended version, it may cause problems on some machines.
 	Some basic benchmarking for the three options are stated below.
        Hence CBGTPy uses an alternative multiprocessing library  (pathos)that interfaces with default python multiprocessing APIs. Pathos is installed by default. 
	But you can choose to not install ray by typing "n" to the prompted question.
  
	$python install.py install
## Test by running:
	$ipython

	-On the ipython prompt
	$import pathos

## If there is an error, deactivate and activate the conda environment again

## Start jupyter notebooks
	$jupyter-notebook

## Only if you want to delete the conda environment !!!
	$conda remove --name cbgtpy_env --all


