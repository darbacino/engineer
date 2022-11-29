import os

CURRENT_WORKING_DIR = os.getcwd()
PATH_CONFIG         = "./configuration.json"
# SSH_RETRIES_CHECK   = 3
PATH_DATA_FOLDER = "ExperimentData/"
PATH_LOCAL_DIR_WITH_EXPERIMENTS = f"{CURRENT_WORKING_DIR}/ExperimentData"
ZIP_FILE_NAME = "exp_data_"#Will be added device name and time to don't override always !
PATH_TO_ZIP = ""
PATH_LOCAL_DIR_WITH_PLOTER_OUTPUT = f"{CURRENT_WORKING_DIR}/PlotterOutput"
PLOTTER_RESOULTS_PREFIX = "Plotter_output"