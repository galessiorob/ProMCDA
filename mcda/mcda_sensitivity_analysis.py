#! /usr/bin/env python3

import logging
import sys

from mcda.configuration.config import Config
from mcda.utils import *

formatter = '%(levelname)s: %(asctime)s - %(name)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)
logger = logging.getLogger("mcda_sensitivity_analysis")

def main(input_config: dict):
    logger.info("Loading the configuration file")
    config = Config(input_config)

    logger.info("Read input matrix at {}".format(config.input_matrix_path))
    input_matrix = read_input_matrix(config.input_matrix_path)

    logger.info("Marginal distributions: {}".format(config.marginal_distribution_for_each_indicator))
    marginal_pdf = config.marginal_distribution_for_each_indicator

    if all(element == 'exact' for element in marginal_pdf):
       # every column of the input matrix represents an indicator
        no_indicators = input_matrix.shape[1]-1
        logger.info("Number of alternatives: {}".format(input_matrix.shape[0]))
        logger.info("Number of indicators: {}".format(no_indicators))
    else:
        # non-exact indicators in the input matrix are associated to a column representing its mean
        # and a second column representing its std
        no_non_exact = len(marginal_pdf) - marginal_pdf.count('exact')
        no_indicators = input_matrix.shape[1]-1-no_non_exact
        logger.info("Number of alternatives: {}".format(input_matrix.shape[0]))
        logger.info("Number of indicators: {}".format(no_indicators))

    logger.info("Number of Monte Carlo runs: {}".format(config.monte_carlo_runs))
    mc_runs = config.monte_carlo_runs

    logger.info("Polarities: {}".format(config.polarity_for_each_indicator))
    polar = config.polarity_for_each_indicator

    logger.info("Weights: {}".format(config.weight_for_each_indicator))
    weight = config.weight_for_each_indicator

    cores = config.no_cores

    if no_indicators != len(polar):
        logger.error('Error Message', stack_info=True)
        raise ValueError('The no. of polarities does not correspond to the no. of indicators')
    if no_indicators != len(weight):
        logger.error('Error Message', stack_info=True)
        raise ValueError('The no. of weights does not correspond to the no. of indicators')

    # here the magic happens

#    logger.info("Saving results in {}".format(config.output_file_path))
#    save_result(res, config.output_file_path)

if __name__ == '__main__':
    config_path = parse_args()
    input_config = get_config(config_path)
    main(input_config=input_config)
