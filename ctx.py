import pickle

import torch
from sentence_transformers import SentenceTransformer
from include.config import env_config
from include.logger import initialize_logger


def handler():
    """
    Context handler to manage all global variables
    @return: dictionary with global variables
    """
    context = {}
    PROCESSOR_CONFIG = "config.env"
    conf = env_config(PROCESSOR_CONFIG)

    location_log_folder = conf.get('LOCATION_LOG_FOLDER')
    log_level = conf.get('LOG_LEVEL')
    llm_name = conf.get('LLM_NAME')
    location_trained_model_en = conf.get('LOCATION_TRAINED_MODEL_EN')
    location_trained_model_de = conf.get('LOCATION_TRAINED_MODEL_DE')
    db_courses = conf.get('DB_COURSES')

    # --------------------------------------------------------
    logger = initialize_logger(location_log_folder, log_level)
    logger.debug('Server started')

    # check best torch_device
    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'

    # prepare global data, we may move this to the contexter
    st_object_model = SentenceTransformer(llm_name, device=torch_device)  # model object based on LLM
    logger.debug('Loading global variables into contexter')

    context.update({"location_log_folder": location_log_folder})
    context.update({"log_level": log_level})
    context.update({"llm_name": llm_name})
    context.update({"location_trained_model_en": location_trained_model_en})
    context.update({"location_trained_model_de": location_trained_model_de})
    context.update({"db_courses": db_courses})

    context.update({"logger": logger})
    context.update({"st_object_model": st_object_model})
    context.update({"torch_device": torch_device})

    return context
