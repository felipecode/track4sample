# CARLA_AD_Challenge_track4_baseline



Clone the repository:

    git clone https://github.com/felipecode/track4sample.git 
    cd coiltraine


You need pygame:
    
    pip install pygame


The checkpoints should now be allocated already on the proper folders.

Download the [latest CARLA 0.9.x version](https://github.com/carla-simulator/carla/blob/master/Docs/download.md).
Then, after unpacking it,  define where the root folder was placed:

    export CARLA_ROOT=<path_to_carla_root>

Install the latest CARLA API:

    easy_install ${CARLA_ROOT}/PythonAPI/*-py3.5-linux-x86_64.egg

Make sure you set the PYTHONPATH PythonAPI path:

     export PYTHONPATH=${CARLA_ROOT}/PythonAPI:$PYTHONPATH
     
### Get the agent performance on the CARLA Challenge


Clone the scenario  runner repository:
    
    cd
    git clone https://github.com/carla-simulator/scenario_runner.git

Setup the scenario runner challenge repository by setting the path to your CARLA root
folder.

    cd scenario_runner
    bash setup_environment --carla-root <path_to_carla_root_folder>


Export the track4sample path to the PYTHONPATH:

    cd ~/track4sample
    export PYTHONPATH=`pwd`:$PYTHONPATH


Going back to the scenario runner folder,
execute the challenge with the conditional imitation learning baseline

    python3  srunner/challenge/challenge_evaluator.py --file --scenario=group:ChallengeBasic --agent=../track4sample/Track4SampleAgent.py 