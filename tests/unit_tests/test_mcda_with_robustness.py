import pandas as pd
import numpy as np
import unittest

from mcda.mcda_with_robustness import MCDAWithRobustness
from mcda.configuration.config import Config


class TestMCDA_with_robustness(unittest.TestCase):

    @staticmethod
    def get_test_config():
        return {
            "input_matrix_path": "/path/to/input_matrix.csv",
            "polarity_for_each_indicator": ["-", "-", "+"],
            "sensitivity": {
                "sensitivity_on": "yes",
                "normalization": "minmax",
                "aggregation": "weighted_sum"},
            "robustness": {
                "robustness_on": "yes",
                "on_single_weights": "no",
                "on_all_weights": "no",
                "given_weights": [0.5, 0.5, 0.5],
                "on_indicators": "yes"},
            "monte_carlo_sampling": {
                "monte_carlo_runs": 10000,
                "num_cores": 1,
                "marginal_distribution_for_each_indicator": ['exact', 'uniform', 'normal']},
            "output_path": "/path/to/output"
        }

    @staticmethod
    def get_input_matrix() -> pd.DataFrame:
        data = {'ind1': [0, 1, 2, 3], 'std1': [0, 0, 0, 0], 'ind2': [4, 5, 6, 7], 'std2': [0.1, 0.1, 0.1, 0.1],
                'ind3': [8, 9, 10, 11], 'std3': [0.1, 0.1, 0.1, 0.1]}
        df = pd.DataFrame(data=data)

        return df

    @staticmethod
    def get_input_list() -> list[pd.DataFrame]:
        data = {'0': [0, 1, 2, 3], '1': [4, 5, 6, 7], '2': [8, 9, 10, 11], '3': [12, 13, 14, 15], '4': [16, 17, 18, 19]}
        df = pd.DataFrame(data=data)
        out_list = [df, df, df]

        return out_list

    @staticmethod
    def get_expected_out_list() -> list[pd.DataFrame]:
        data1 = {'0': [0, 1, 2, 3], '1': [0, 1, 2, 3], '2': [0, 1, 2, 3]}
        data2 = {'0': [4, 5, 6, 7], '1': [4, 5, 6, 7], '2': [4, 5, 6, 7]}
        data3 = {'0': [8, 9, 10, 11], '1': [8, 9, 10, 11], '2': [8, 9, 10, 11]}
        data4 = {'0': [12, 13, 14, 15], '1': [12, 13, 14, 15], '2': [12, 13, 14, 15]}
        data5 = {'0': [16, 17, 18, 19], '1': [16, 17, 18, 19], '2': [16, 17, 18, 19]}
        data = [data1, data2, data3, data4, data5]
        out_list = []
        for i in range(0, 5):
            df_name = pd.DataFrame(data=data[i])
            out_list.append(df_name)

        return out_list

    @staticmethod
    def get_list_random_input_matrices() -> list[pd.DataFrame]:
        np.random.seed(42)
        data1 = pd.DataFrame(
            data={'0': [0, 1, 2, 3], '1': [0, 1, 2, 3], '2': [0, 1, 2, 3], '3': [0, 1, 2, 3], '4': [0, 1, 2, 3],
                  '5': [0, 1, 2, 3], '6': [0, 1, 2, 3], '7': [0, 1, 2, 3], '8': [0, 1, 2, 3], '9': [0, 1, 2, 3]})
        data2 = np.random.uniform(low=5.5 - 0.1, high=5.5 + 0.1, size=(4, 10))
        data2 = pd.DataFrame(data2)
        data3 = np.random.normal(loc=9.5, scale=0.1, size=(4, 10))
        data3 = pd.DataFrame(data3)
        out_list = [data1, data2, data3]

        input_matrix = TestMCDA_with_robustness.get_input_matrix()
        config = TestMCDA_with_robustness.get_test_config()
        config = Config(config)
        MCDA_w_uncert = MCDAWithRobustness(config, input_matrix)
        output_list = MCDA_w_uncert.convert_list(out_list)

        return output_list

    def test_repeat_series_to_create_df(self):
        # Given
        input_matrix = self.get_input_matrix()
        input_series = input_matrix.iloc[:, 0]
        config = TestMCDA_with_robustness.get_test_config()
        config = Config(config)
        num_runs = 10
        exp_matrix = pd.DataFrame(
            data={'0': [0, 1, 2, 3], '1': [0, 1, 2, 3], '2': [0, 1, 2, 3], '3': [0, 1, 2, 3], '4': [0, 1, 2, 3],
                  '5': [0, 1, 2, 3], '6': [0, 1, 2, 3], '7': [0, 1, 2, 3], '8': [0, 1, 2, 3], '9': [0, 1, 2, 3]})

        # When
        MCDA_w_uncert = MCDAWithRobustness(config, input_matrix)
        output_matrix = MCDA_w_uncert.repeat_series_to_create_df(input_series, num_runs)

        # Then
        assert isinstance(output_matrix, pd.DataFrame)
        assert exp_matrix.values.all() == output_matrix.values.all()
        assert exp_matrix.values.shape == output_matrix.shape

    def test_convert_list(self):
        # Given
        input_matrix = self.get_input_matrix()
        config = TestMCDA_with_robustness.get_test_config()
        input_list = TestMCDA_with_robustness.get_input_list()
        expected_output_list = TestMCDA_with_robustness.get_expected_out_list()

        # When
        config = Config(config)
        MCDA_w_uncert = MCDAWithRobustness(config, input_matrix)
        output_list = MCDA_w_uncert.convert_list(input_list)

        # Then
        assert isinstance(output_list, list)
        assert len(output_list) == 5
        for df1, df2 in zip(output_list, expected_output_list):
            assert df1.shape == (4, 3)
            assert df1.values.all() == df2.values.all()

    def test_create_n_randomly_sampled_matrices(self):
        # Given
        input_matrix = self.get_input_matrix()
        config = TestMCDA_with_robustness.get_test_config()

        # When
        config = Config(config)
        MCDA_w_uncert = MCDAWithRobustness(config, input_matrix)
        n_random_matrices = MCDA_w_uncert.create_n_randomly_sampled_matrices()
        exp_n_random_matrices = TestMCDA_with_robustness.get_list_random_input_matrices()

        # Then
        assert isinstance(n_random_matrices, list)
        assert len(n_random_matrices) == config.monte_carlo_sampling["monte_carlo_runs"]
        for df1, df2 in zip(n_random_matrices, exp_n_random_matrices):
            assert df1.shape == (4, 3)
            assert df1.values.all() == df2.values.all()
