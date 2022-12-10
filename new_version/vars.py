import os

CURRENT_WORKING_DIR     = os.getcwd()
PATH_CONFIG             = "./configuration.json"
PATH_DATA_FOLDER        = "ExperimentData/"
PLOTTER_RESOULTS_PREFIX = "Plotter_output"
ZIP_FILE_NAME           = ""#Will be added device name and time to don't override always !
# NAME_DIR_EXPERIMENT     = ""
PATH_LOCAL_DIR_WITH_PLOTER_OUTPUT   = f"{CURRENT_WORKING_DIR}/PlotterOutput"
PATH_LOCAL_DIR_WITH_EXPERIMENTS     = f"{CURRENT_WORKING_DIR}/ExperimentData"
# SSH_RETRIES_CHECK   = 3