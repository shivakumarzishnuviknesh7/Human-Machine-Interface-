"""
This file shows how to configure your project.
All global variables here are used throughout the project, so they can be shared across modules.
The config.env file stores all these variables, which are run at the beginning of the program.
"""
import configparser


# ----------------------------------------------------------------
#                   Configuration file
# ----------------------------------------------------------------

# @todo add logger instead of print
def env_config(config_file):
    import os
    from dotenv import load_dotenv

    load_dotenv(config_file)
    config_dict = {}

    # General Config
    try:
        location_log_folder = os.getenv('LOCATION_LOG_FOLDER')
        log_level = os.getenv('LOG_LEVEL')
        llm_name = os.getenv('LLM_NAME')
        location_trained_model_en = os.getenv('LOCATION_TRAINED_MODEL_EN')
        location_trained_model_de = os.getenv('LOCATION_TRAINED_MODEL_DE')
        db_courses = os.getenv('DB_COURSES')

        config_dict.update([('LOCATION_LOG_FOLDER', location_log_folder)])
        config_dict.update([('LOG_LEVEL', log_level)])
        config_dict.update([('LLM_NAME', llm_name)])
        config_dict.update([('LOCATION_TRAINED_MODEL_EN', location_trained_model_en)])
        config_dict.update([('LOCATION_TRAINED_MODEL_DE', location_trained_model_de)])
        config_dict.update([('DB_COURSES', db_courses)])

    except Exception as error:
        print("please check configuration file: %s", error)
        return -1

    return config_dict
