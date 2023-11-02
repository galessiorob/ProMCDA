<div style="text-align: left;margin-bottom: 0.01px;">
<img src="logo/total_logo.jpg" alt="logo" width="400" height="100">
</div>

<!-- [![status](https://joss.theoj.org/papers/4214c6e588774490458e34630e8052c1/status.svg)](https://joss.theoj.org/papers/4214c6e588774490458e34630e8052c1) -->
<!-- [![PyPi version](https://img.shields.io/pypi/v/promcda?color=blue)](https://pypi.org/project/promcda) -->
![tests](https://github.com/pysersic/pysersic/actions/workflows/pytest.yml/badge.svg)
![License](https://img.shields.io/badge/license-EPL%202.0-blue)

# Probabilistic Multi Criteria Decision Analysis

A tool to estimate scores of alternatives and their uncertainties based on the Multi Criteria Decision Analysis (MCDA) approach.

A MCDA approach is a systematic framework for making decisions in situations where multiple criteria or objectives need to be 
considered. It can be applied in various domains and contexts. Here are some possible usages of an MCDA approach:

- **Environmental impact assessment**: assess the environmental consequences of various projects or policies by considering 
  multiple environmental criteria.
- **Project selection**: choose the most suitable project from a set of alternatives by considering multiple criteria such 
  as cost, risk, and strategic alignment.
- **Healthcare decision-making**: decide on the allocation of healthcare resources, such as funding for medical treatments 
  or the purchase of medical equipment, while considering criteria like cost-effectiveness, patient outcomes, 
  and ethical considerations. It applies to other decision-making problems too.
- **Investment portfolio optimization**: construct an investment portfolio that balances criteria like risk, return, 
  and diversification.
- **Personnel recruitment**: evaluate job candidates based on criteria like qualifications, experience, and cultural fit.
- **Location analysis**: choose the optimal location for a new facility or business by considering factors like cost, 
  accessibility, and market potential.
- **Public policy evaluation**: assess the impact of proposed policies on various criteria, such as economic growth, 
  social welfare, and environmental sustainability.
- **Product development**: prioritize features or attributes of a new product by considering criteria like cost, market demand, 
  and technical feasibility.
- **Disaster risk management**: identify high-risk areas and prioritize disaster preparedness and mitigation measures based 
  on criteria like vulnerability, exposure, and potential impact.
- **Energy planning**: make decisions about energy resource allocation and investments in renewable energy sources, 
  taking into account criteria like cost, environmental impact, and reliability.
- **Transportation planning**: optimize transportation routes, modes, and infrastructure investments while considering 
  criteria like cost, time efficiency, and environmental impact.
- **Water resource management**: optimize water allocation for various uses, including agriculture, industry, 
  and municipal supply, while considering criteria like sustainability and equity.
- **Urban planning**: decide on urban development projects and land-use planning based on criteria such as social equity, 
  environmental impact, and economic development.

These are just a few examples of how MCDA can be applied across a wide range of fields to support decision-making processes 
that involve multiple, often conflicting, criteria. The specific application of MCDA will depend on the context 
and the goals of the decision-maker.

In MCDA context an *alternative* is one possible course of action available; 
an *indicator* is a parameter that describes the alternatives.
The variability of the MCDA scores are caused by:

- the sensitivity of the algorithm to the different pairs of norm/agg functions (--> sensitivity analysis);
- the randomness that can be associated to the weights (--> robustness analysis);
- the uncertainty associated with the indicators (--> robustness analysis).

Here we define:
- the **sensitivity analysis** as the one aimed at capturing the output score stability to the different initial modes;
- the **robustness analysis** as the one aimed at capturing the effect of any changes in the inputs (their uncertainties) on the output scores.

The tool can be also used as a simple (i.e. deterministic) MCDA ranking tool with no robustness/sensitivity analysis (see below for instructions).

### Input information needed in the configuration file
The configuration file collects all the input information to run ```ProMCDA```.
The following input information should be all contained in the `configuration.json` file.

***Path to the input matrix***, a table where rows represent the alternatives and columns represent the indicators.
Be sure that the column containing the names of the alternatives is set as index column, e.g. by:
```bash
input_matrix = input_matrix.set_index('Alternatives').
```
Be also sure that there are no duplicates among the rows. If the values of one or more indicators are all the same, 
the indicators are dropped from the input matrix.
Examples of input matrix:

- *input matrix without uncertainties* for the indicators (see an example here: `tests/resources/input_matrix_without_uncert.csv`)
- *input matrix with uncertainties* for the indicators (see an example here: `tests/resources/input_matrix_with_uncert.csv`)

The input matrix with uncertainties has for each indicator a column with the mean values and a column with the standard deviation; 
if the marginal distribution relative to the indicator is 'exact', then the standard deviation column contains only 0.

***List of polarities*** for each indicator, "+" (the higher the value of the indicator the better for the evaluation) 
or "-" (the lower the value of the indicator the better).

The configuration file can trigger a run with or without ***sensitivity analysis***; this is set in the `sensitivity_on` parameter (*yes* or *no*); 
if *no* is selected, then the pair normalization/aggregation should be given in `normalization` and `aggregation`.

Similarly, a run with or without uncertainty on the indicators or on the weights (i.e. with ***robustness analysis***) 
can be triggered by setting the `robustness_on` parameter to *yes* or *no*. If `robustness_on` is set to *yes*, then 
the uncertainties might be on the indicators (`on_indicators`) or on the weights (`on_single_weights` or `on_all_weights`). 
In the first case (`on_single_weights=yes`) one weight at time is randomly sampled from a uniform distribution; 
in the second case (`on_all_weights=yes`) all weights are simultaneously sampled from a normal distribution. 
If there is no uncertainty associated to the weights, then the user should provide a ***list of weights*** for the indicators. 
The sum of the weights should always be equal to 1 or the values will be normalised. 
Depending on the different options, the other information are disregard. Sensitivity and robustness analysis can be run
together. If robustness analysis is selected, it can run either on the weights or on the indicators, but not on both simultaneously.

If robustness analysis is selected, a last block of information is needed:
the ***Number of Monte Carlo runs***, "N" (default is 0, then no robustness is considered; N should be a sufficient big number, 
e.g., larger or equal than 1000). The ***number of cores*** used for the parallelization; and a 
***List of marginal distributions*** for each indicator; the available distributions are: 
  - exact, **"exact"**,
  - uniform distribution, **"uniform"**
  - normal distribution, **"norm"**
  - lognormal distribution, **"lnorm"**
  - Poisson distribution, **"poisson"**

Finally, the ***Path to output file*** (e.g. `path/output_file.csv`) is given. In the output file the scores (normalised or rough) 
and the ranks relative to the alternatives can be found in form of CSV tables. If the weights are iteratively sampled, 
multiple tables are saved in PICKLE files. Plots of the scores are saved in PNG images.

### Requirements
```bash
conda create --name <choose-a-name-like-Promcda> python=3.6
source activate <choose-a-name-like-Promcda>
pip install -r requirements.txt
```

### Running the code (from root dir)
```bash
source activate <your-env>
python3 -m mcda.mcda_run -c configuration_w_robustness.json
```
where an example of configuration file can be found in `mcda/configuration_w_robustness.json` or `mcda/configuration_without_robustness.json`.

### Running the tests
```bash
python3 -m pytest -s tests/unit_tests/test_mcda_run.py -vv
```

### What does the code do: summary overview
If no robustness analysis is selected, then:
- the indicator values are normalized by mean of all the possible normalization methods (or by the selected one);
- the normalized indicators are aggregated by mean of all the possible aggregation methods (or by the selected one), 
  by considering their assigned weights;
- the resulting scores of all the combinations normalization/aggregation (or the selected ones only) are provided in form 
  of a csv table and plots in png format in the output directory.

If the weights are randomly sampled (robustness analysis of the weights), then:
- all weights or one weight at time are randomly sampled from a uniform distribution [0,1];
- the weights are normalized so that their sum is always equal to 1;
- if all weights are sampled together, MCDA calculations receive N-inputs (N being the number of `monte_carlo_runs`; 
  if the weights are sampled one at time, MCDA will receive (*n-inputs x num_weights*) inputs;
- iterations 1,2,3 of the first condition follow;
- the results of all the combinations normalization/aggregation (or the one selected) are provided in the form of mean and std over all the runs 
  (if the weights are iteratively sampled, this applies for *num_indicators-times*).

If the robustness analysis regards the indicators, then:
- for each indicator, the mean and std are extracted from the input matrix;
- for each N, and for each indicator, a value is sampled from the relative assigned marginal distribution: therefore, one of N input matrix is created;
- normalizations and aggregations are performed as in points 1,2 of the first case: a list of all the results is created in the output directory;
- mean and std of all the results are estimated across (monte_carlo_runs x pairs of combinations);  
- in this case, no randomness on the weights is allowed.


### General information and references
The aggregation functions are implemented by following [*Langhans et al.*, 2014](https://www.sciencedirect.com/science/article/abs/pii/S1470160X14002167)

The normalization functions *minmax*, *target* and *standardized* can produce negative or zero values, therefore a shift to positive values
is implemented so that they can be used also together with the aggregation functions *geometric* and *harmonic* (which require positive values). 

The code implements 4 normalization and 4 aggregation functions. However, not all combinations are 
meaningful or mathematically acceptable. For more details refer to Table 6 in 
[*Gasser et al.*, 2020](https://www.sciencedirect.com/science/article/pii/S1470160X19307241)

The standard deviation of rescaled scores with any form of randomness are not saved nor plotted because they cannot bring a statistically meaningful information.
In fact, when one calculates the standard deviation after rescaling between (0,1), the denominator used in the standard deviation formula becomes smaller. 
This results in a higher relative standard deviation compared to the mean.
However, the higher relative standard deviation is not indicating a greater spread in the data but rather a consequence of the rescaling operation and 
the chosen denominator in the standard deviation calculation.


