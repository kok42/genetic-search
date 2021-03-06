from sklearn.model_selection._search import BaseSearchCV
from sklearn.model_selection._search import ParameterGrid
import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

import random

import matplotlib.pyplot as plt


class GeneticSearchCV(BaseSearchCV):
    """Search over specified parameter values for an estimator via genetic algorithm.

    Important members are fit, predict.
    GeneticSearchCV implements a "fit" and a "score" method.
    It also implements "score_samples", "predict", "predict_proba",
    "decision_function", "transform" and "inverse_transform" if they are
    implemented in the estimator used.
    The parameters of the estimator used to apply these methods are optimized
    by cross-validated genetic-search over a parameter grid.
    Read more in the :ref:`User Guide <grid_search>`.
    Parameters
    ----------
    estimator : estimator object
        This is assumed to implement the scikit-learn estimator interface.
        Either estimator needs to provide a ``score`` function,
        or ``scoring`` must be passed.
    param_grid : dict or list of dictionaries
        Dictionary with parameters names (`str`) as keys and lists of
        parameter settings to try as values, or a list of such
        dictionaries, in which case the grids spanned by each dictionary
        in the list are explored. This enables searching over any sequence
        of parameter settings.
    scoring : str, callable, list, tuple or dict, default=None
        Strategy to evaluate the performance of the cross-validated model on
        the test set.
        If `scoring` represents a single score, one can use:
        - a single string (see :ref:`scoring_parameter`);
        - a callable (see :ref:`scoring`) that returns a single value.
        If `scoring` represents multiple scores, one can use:
        - a list or tuple of unique strings;
        - a callable returning a dictionary where the keys are the metric
          names and the values are the metric scores;
        - a dictionary with metric names as keys and callables a values.
        See :ref:`multimetric_grid_search` for an example.
    n_jobs : int, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
        .. versionchanged:: v0.20
           `n_jobs` default changed from 1 to None
    refit : bool, str, or callable, default=True
        Refit an estimator using the best found parameters on the whole
        dataset.
        For multiple metric evaluation, this needs to be a `str` denoting the
        scorer that would be used to find the best parameters for refitting
        the estimator at the end.
        Where there are considerations other than maximum score in
        choosing a best estimator, ``refit`` can be set to a function which
        returns the selected ``best_index_`` given ``cv_results_``. In that
        case, the ``best_estimator_`` and ``best_params_`` will be set
        according to the returned ``best_index_`` while the ``best_score_``
        attribute will not be available.
        The refitted estimator is made available at the ``best_estimator_``
        attribute and permits using ``predict`` directly on this
        ``GridSearchCV`` instance.
        Also for multiple metric evaluation, the attributes ``best_index_``,
        ``best_score_`` and ``best_params_`` will only be available if
        ``refit`` is set and all of them will be determined w.r.t this specific
        scorer.
        See ``scoring`` parameter to know more about multiple metric
        evaluation.
        .. versionchanged:: 0.20
            Support for callable added.
    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
        - None, to use the default 5-fold cross validation,
        - integer, to specify the number of folds in a `(Stratified)KFold`,
        - :term:`CV splitter`,
        - An iterable yielding (train, test) splits as arrays of indices.
        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass, :class:`StratifiedKFold` is used. In all
        other cases, :class:`KFold` is used. These splitters are instantiated
        with `shuffle=False` so the splits will be the same across calls.
        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validation strategies that can be used here.
        .. versionchanged:: 0.22
            ``cv`` default value if None changed from 3-fold to 5-fold.
    verbose : int
        Controls the verbosity: the higher, the more messages.
        - >1 : the computation time for each fold and parameter candidate is
          displayed;
        - >2 : the score is also displayed;
        - >3 : the fold and candidate parameter indexes are also displayed
          together with the starting time of the computation.
    pre_dispatch : int, or str, default='2*n_jobs'
        Controls the number of jobs that get dispatched during parallel
        execution. Reducing this number can be useful to avoid an
        explosion of memory consumption when more jobs get dispatched
        than CPUs can process. This parameter can be:
            - None, in which case all the jobs are immediately
              created and spawned. Use this for lightweight and
              fast-running jobs, to avoid delays due to on-demand
              spawning of the jobs
            - An int, giving the exact number of total jobs that are
              spawned
            - A str, giving an expression as a function of n_jobs,
              as in '2*n_jobs'
    error_score : 'raise' or numeric, default=np.nan
        Value to assign to the score if an error occurs in estimator fitting.
        If set to 'raise', the error is raised. If a numeric value is given,
        FitFailedWarning is raised. This parameter does not affect the refit
        step, which will always raise the error.
    return_train_score : bool, default=False
        If ``False``, the ``cv_results_`` attribute will not include training
        scores.
        Computing training scores is used to get insights on how different
        parameter settings impact the overfitting/underfitting trade-off.
        However computing the scores on the training set can be computationally
        expensive and is not strictly required to select the parameters that
        yield the best generalization performance.
        .. versionadded:: 0.19
        .. versionchanged:: 0.21
            Default value was changed from ``True`` to ``False``
    population_size : int, dedault=50
        Size of population used in genetic algorithm.
        Larger sizes lead to more calculations as well as to more accurate
        parameters.
    max_generations : int, default=50,
        Amount of generations used in genetic algorithm.
        Larger sizes lead to more calculations as well as to more accurate
        parameters.
    tournament_size : int, default=None,
        Sise of tournament used in genetic algorithm.
        If None tournament_size is set to 20% of population size.
    crossover_prob : float, default=0.9,
        The probability of crossover happening for an individual.
        Crossover in this genetic algorithm is a uniform crossover. Gens
        of one individual are randomly swaps with corrsepondent gens
    gen_crossover_prob : float, default=0.3,
       The propapility for each gen to be swapped.
    mutation_prob : float, default=0.1,
       The probability of mutation happening for an individual.
       Mutation in this genetic algorithm is a random choise of correspondent
       value from the param grid.
    gen_mutation_prob=1.0/8,
        The propapility for each gen to mutate.
    do_plot : boolean, default=False,
        Whether to plot the dependence of max, mean and min fittess of
        generation.
    genetic_verbose : boolean, default=False,
        Whether to log what is happening during the evolution of genetic algorithm or not

    Attributes
    ----------
    cv_results_ : dict of numpy (masked) ndarrays
        A dict with keys as column headers and values as columns, that can be
        imported into a pandas ``DataFrame``.
        For instance the below given table
        +------------+-----------+------------+-----------------+---+---------+
        |param_kernel|param_gamma|param_degree|split0_test_score|...|rank_t...|
        +============+===========+============+=================+===+=========+
        |  'poly'    |     --    |      2     |       0.80      |...|    2    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'poly'    |     --    |      3     |       0.70      |...|    4    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.1   |     --     |       0.80      |...|    3    |
        +------------+-----------+------------+-----------------+---+---------+
        |  'rbf'     |     0.2   |     --     |       0.93      |...|    1    |
        +------------+-----------+------------+-----------------+---+---------+
        will be represented by a ``cv_results_`` dict of::
            {
            'param_kernel': masked_array(data = ['poly', 'poly', 'rbf', 'rbf'],
                                         mask = [False False False False]...)
            'param_gamma': masked_array(data = [-- -- 0.1 0.2],
                                        mask = [ True  True False False]...),
            'param_degree': masked_array(data = [2.0 3.0 -- --],
                                         mask = [False False  True  True]...),
            'split0_test_score'  : [0.80, 0.70, 0.80, 0.93],
            'split1_test_score'  : [0.82, 0.50, 0.70, 0.78],
            'mean_test_score'    : [0.81, 0.60, 0.75, 0.85],
            'std_test_score'     : [0.01, 0.10, 0.05, 0.08],
            'rank_test_score'    : [2, 4, 3, 1],
            'split0_train_score' : [0.80, 0.92, 0.70, 0.93],
            'split1_train_score' : [0.82, 0.55, 0.70, 0.87],
            'mean_train_score'   : [0.81, 0.74, 0.70, 0.90],
            'std_train_score'    : [0.01, 0.19, 0.00, 0.03],
            'mean_fit_time'      : [0.73, 0.63, 0.43, 0.49],
            'std_fit_time'       : [0.01, 0.02, 0.01, 0.01],
            'mean_score_time'    : [0.01, 0.06, 0.04, 0.04],
            'std_score_time'     : [0.00, 0.00, 0.00, 0.01],
            'params'             : [{'kernel': 'poly', 'degree': 2}, ...],
            }
        NOTE
        The key ``'params'`` is used to store a list of parameter
        settings dicts for all the parameter candidates.
        The ``mean_fit_time``, ``std_fit_time``, ``mean_score_time`` and
        ``std_score_time`` are all in seconds.
        For multi-metric evaluation, the scores for all the scorers are
        available in the ``cv_results_`` dict at the keys ending with that
        scorer's name (``'_<scorer_name>'``) instead of ``'_score'`` shown
        above. ('split0_test_precision', 'mean_train_precision' etc.)
    best_estimator_ : estimator
        Estimator that was chosen by the search, i.e. estimator
        which gave highest score (or smallest loss if specified)
        on the left out data. Not available if ``refit=False``.
        See ``refit`` parameter for more information on allowed values.
    best_score_ : float
        Mean cross-validated score of the best_estimator
        For multi-metric evaluation, this is present only if ``refit`` is
        specified.
        This attribute is not available if ``refit`` is a function.
    best_params_ : dict
        Parameter setting that gave the best results on the hold out data.
        For multi-metric evaluation, this is present only if ``refit`` is
        specified.
    best_index_ : int
        The index (of the ``cv_results_`` arrays) which corresponds to the best
        candidate parameter setting.
        The dict at ``search.cv_results_['params'][search.best_index_]`` gives
        the parameter setting for the best model, that gives the highest
        mean score (``search.best_score_``).
        For multi-metric evaluation, this is present only if ``refit`` is
        specified.
    scorer_ : function or a dict
        Scorer function used on the held out data to choose the best
        parameters for the model.
        For multi-metric evaluation, this attribute holds the validated
        ``scoring`` dict which maps the scorer key to the scorer callable.
    n_splits_ : int
        The number of cross-validation splits (folds/iterations).
    refit_time_ : float
        Seconds used for refitting the best model on the whole dataset.
        This is present only if ``refit`` is not False.
        .. versionadded:: 0.20
    multimetric_ : bool
        Whether or not the scorers compute several metrics.
    classes_ : ndarray of shape (n_classes,)
        The classes labels. This is present only if ``refit`` is specified and
        the underlying estimator is a classifier.
    n_features_in_ : int
        Number of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `n_features_in_` when fit.
        .. versionadded:: 0.24
    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Only defined if
        `best_estimator_` is defined (see the documentation for the `refit`
        parameter for more details) and that `best_estimator_` exposes
        `feature_names_in_` when fit.
        .. versionadded:: 1.0

    Examples
    --------
    >>> from sklearn import svm, datasets
    >>> from genetic_search.model_selection import GeneticSearchCV
    >>> iris = datasets.load_iris()
    >>> parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    >>> svc = svm.SVC()
    >>> clf = GeneticSearchCV(svc, parameters)
    >>> clf.fit(iris.data, iris.target)
    GridSearchCV(estimator=SVC(),
                 param_grid={'C': [1, 10], 'kernel': ('linear', 'rbf')})
    >>> sorted(clf.cv_results_.keys())
    ['mean_fit_time', 'mean_score_time', 'mean_test_score',...
     'param_C', 'param_kernel', 'params',...
     'rank_test_score', 'split0_test_score',...
     'split2_test_score', ...
     'std_fit_time', 'std_score_time', 'std_test_score']
    """

    _required_parameters = ["estimator", "param_grid"]

    def __init__(self,
                 estimator,
                 param_grid,
                 *,
                 scoring=None,
                 n_jobs=None,
                 refit=True,
                 cv=None,
                 verbose=0,
                 pre_dispatch="2*n_jobs",
                 error_score=np.nan,
                 return_train_score=False,
                 population_size=10,
                 max_generations=10,
                 tournament_size=None,
                 gen_crossover_prob=0.3,
                 gen_mutation_prob=1.0 / 8,
                 crossover_prob=0.9,
                 mutation_prob=0.1,
                 do_plot=False,
                 genetic_verbose=False):
        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score, )
        self.param_grid = param_grid
        self.population_size = population_size
        self.max_generations = max_generations
        if tournament_size is None:
            self.tournament_size = int(0.2 * self.population_size)
        else:
            self.tournament_size = tournament_size
        self.gen_crossover_prob = gen_crossover_prob
        self.gen_mutation_prob = gen_mutation_prob
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.do_plot = do_plot
        self.genetic_verbose = genetic_verbose

    def decode_genome(self, params):
        """Makes a param dict from genome."""
        decoded = self.param_grid.copy()
        i = 0
        for key in decoded:
            try:
                if params[i] == int(params[i]):
                    params[i] = int(params[i])
            except:
                pass
            decoded[key] = params[i]
            i += 1
        return decoded

    def create_genome(self, icls):
        """Chooses random params from the param_grid to create a genome."""
        genome = list()
        for key in self.param_grid:
            genome.append(random.choice(self.param_grid[key]))
        return icls(genome)

    @staticmethod
    def crossover(ind1, ind2, p):
        """Executes the uniform crossover process."""
        for i in range(len(ind1)):
            if random.random() < p:
                temp = ind1[i]
                ind1[i] = ind2[i]
                ind2[i] = temp
        return ind1, ind2

    def mutate(self, genome, p):
        """Executes random choice mutation."""
        if random.random() < p:
            i = 0
            for key in self.param_grid:
                genome[i] = random.choice(self.param_grid[key])
                i += 1
        return genome,

    def fitness(self, params, evaluate_candidates):
        """Wrapper function to connect functionality of genetic algorithm
            and BaseSearchCV together."""
        self.count += 1
        return evaluate_candidates([self.decode_genome(params)])['mean_test_score'][self.count],

    def _run_search(self, evaluate_candidates):
        """Executes the search using genetic algorithm."""
        self.count = -1
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register('evaluate', self.fitness, evaluate_candidates=evaluate_candidates)
        toolbox.register('individualCreator', self.create_genome, creator.Individual)
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)
        population = toolbox.populationCreator(n=self.population_size)

        toolbox.register("select", tools.selTournament, tournsize=self.tournament_size)
        toolbox.register("mate", self.crossover, p=self.gen_crossover_prob)
        toolbox.register("mutate", self.mutate, p=self.gen_mutation_prob)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", np.max)
        stats.register("avg", np.mean)
        stats.register("min", np.min)

        population, logbook = algorithms.eaSimple(population, toolbox,
                                                  cxpb=self.crossover_prob,
                                                  mutpb=self.mutation_prob,
                                                  ngen=self.max_generations,
                                                  stats=stats,
                                                  verbose=self.genetic_verbose)
        if self.do_plot:
            maxFitnessValues, meanFitnessValues, minFitnessValues = logbook.select("max", "avg", "min")
            plt.plot(maxFitnessValues, color='red')
            plt.plot(meanFitnessValues, color='green')
            plt.plot(minFitnessValues, color='blue')
            plt.legend(['max', 'mean', 'min'])
            plt.xlabel('Generation')
            plt.ylabel('Fittnes')
            plt.title('Dependence of fitness from generation')
            plt.show()
