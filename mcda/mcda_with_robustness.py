import sys
import copy
import logging
from mcda.utils import *
from typing import List
import pandas as pd
import numpy as np


from mcda.configuration.config import Config

formatter = '%(levelname)s: %(asctime)s - %(name)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)
logger = logging.getLogger("MCDA with sensitivity")

class MCDAWithRobustness():
    """

    Class MCDA with indicators' uncertainty

    This class allows one to run MCDA by considering the uncertainties related to the indicators.
    All indicator values are randomly sampled by different distributions.
    It's possible to have randomly sampled weights too.

    """

    def __init__(self, config: Config, input_matrix: pd.DataFrame()):
        self._config = copy.deepcopy(config)
        self._input_matrix = copy.deepcopy(input_matrix)

    @staticmethod
    def repeat_series_to_create_df(initial_series: pd.Series, num_runs:int) -> pd.DataFrame:
        """
        This is a helper function to create a (AxN) df by concatenating
        a series of values of length A for N times. This reproduces a fake random
        sampling in case an indicator has an exact marginal distribution.
        """

        data_list = [initial_series[:] for _ in range(num_runs)]
        out_df = pd.DataFrame(data_list,index=range(num_runs)).T

        return out_df

    @staticmethod
    def convert_list(data_list):
        """
        This is a helper function to convert a list of length I of (AxN) dfs
        into a list of length N of (AxI) dfs.
        """
        alternatives, num_runs = data_list[0].shape

        transposed_list = [pd.DataFrame(index=range(alternatives)) for _ in range(num_runs)]

        for i, df in enumerate(data_list):
            for n in range(num_runs):
                transposed_list[n][i] = df.iloc[:,n]

        return transposed_list

    def create_n_randomly_sampled_matrices(self) -> List[pd.DataFrame]:
        """
        This function receives an input matrix of dimensions (Ax2I) whose columns represent means and standard deviations
        of each indicator. In a first step, it produces a list of length I of matrices of dimension (AxN).
        Every matrix represents the N random samples of every alternative (A), per indicator (I).
        If there are negative random samples, they are rescaled into [0-1].
        In a second step, a utility function converts this list into a list of length N of matrices of dimension (AxI).
        The output is therefore a list containing N randomly sampled input matrices. The PDFs from where random values
        are sampled depends on the indicator marginal distributions.

        A: all alternatives
        I: all indicators
        N: number of random samples
        """
        marginal_pdf = self._config.monte_carlo_sampling["marginal_distribution_for_each_indicator"]
        is_exact_pdf_mask = check_if_pdf_is_exact(marginal_pdf)

        num_runs = self._config.monte_carlo_sampling["monte_carlo_runs"] # N
        input_matrix = self._input_matrix # (AxI)

        np.random.seed(42)

        sampled_matrices = [] # list long I

        j=0
        for i, pdf_type in enumerate(is_exact_pdf_mask):
            mean_col_position = j
            if pdf_type == 0 and marginal_pdf[i] != 'poisson':  # non-exact PDF except Poisson
                std_col_position = mean_col_position + 1  # standard deviation column follows mean
                mean_col = input_matrix.columns[mean_col_position]
                std_col = input_matrix.columns[std_col_position]
                means = input_matrix[mean_col]
                stds = input_matrix[std_col]
                j += 2

            elif pdf_type == 1 or marginal_pdf][i] == 'poisson':  # exact PDF or Poisson
                mean_col = input_matrix.columns[mean_col_position]
                means = input_matrix[mean_col]
                j += 1

            distribution_type = marginal_pdf[i // 2]

            if distribution_type == 'exact':
                samples = self.repeat_series_to_create_df(means, num_runs).T
            elif distribution_type == 'normal':
                samples = np.random.normal(loc=means, scale=stds, size=(num_runs, len(means)))
            elif distribution_type == 'uniform':
                samples = np.random.uniform(low=means, high=stds, size=(num_runs, len(means)))
            elif distribution_type == 'lnorm':
                samples = np.random.lognormal(mean=means, sigma=stds, size=(num_runs, len(means)))
            elif distribution_type == 'poisson':
                samples = np.random.poisson(lam=means, size=(num_runs, len(means)))
            else:
                raise ValueError(f"Invalid marginal distribution type: {distribution_type}")

            # check if any sample is negative and rescale btw 0 and 1
            if (samples < 0).any().any():
                samples -= samples.min()
                samples /= samples.max()

            sampled_df = pd.DataFrame(samples.transpose()) # (AxN)
            sampled_matrices.append(sampled_df)

        list_random_matrix = self.convert_list(sampled_matrices)

        return list_random_matrix