"""
This script acts as a bridge for calling the ProMCDA process. It imports the main function from promcda_core.py
and provides a wrapper function run_promcda that accepts the input_config_settings dictionary and passes it to the main function.
Whether the run_promcda function is called from a CLI interface or an API endpoint, it expects the input_config_settings
parameter to be passed directly.
"""

import sys
import logging
from mcda.promcda_core import main
from mcda.configuration.config import Config
from mcda.utils.utils_for_main import parse_args, get_config

log = logging.getLogger(__name__)

FORMATTER: str = '%(levelname)s: %(asctime)s - %(name)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMATTER)
logger = logging.getLogger("ProMCDA")


def run_promcda(input_config_settings: dict):
    """
    Run the ProMCDA process with the provided input configuration.

    :param input_config_settings: dict: Configuration parameters for the ProMCDA process.
    :return: None
    """
    config = Config(input_config_settings)
    main(config)

    print("ProMCDA process is running...")


if __name__ == '__main__':
    config_path = parse_args()
    input_config = get_config(config_path)
    main(input_config=input_config)
