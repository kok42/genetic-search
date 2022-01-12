# Genetic search 

This is a tool for optimising sklearn-compatible models' hyperparameters.
It uses genetic algorithm so, it is much faster than GridSearchCV and gives
more consistent results than RandomizedSearchCV.

The class GeneticSearchCV is extended of the sklearn's class BaseSearchCV, so
it has the same functionality as sklearn's searches.

You are free to use, modify and copy the code.

GeneticSearchCV has all parameters of sklearn's GridsearchCV. See sklearn 
documentation to learn more

#### Example
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

#### Additional parameter documentation
- population_size : int, dedault=10  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Size of population used in genetic algorithm.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Larger sizes lead to more calculations as well as to more accurate parameters.

- max_generations : int, default=10,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Amount of generations used in genetic algorithm.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Larger sizes lead to more calculations as well as to more accurate parameters.
- tournament_size : int, default=None,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Sise of tournament used in genetic algorithm.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; If None tournament_size is set to 20% of population size.  
- crossover_prob : float, default=0.9,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The probability of crossover happening for an individual.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Crossover in this genetic algorithm is a uniform crossover. Gens  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; of one individual are randomly swaps with corrsepondent gens  
- gen_crossover_prob : float, default=0.3,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The propapility for each gen to be swapped.  
- mutation_prob : float, default=0.1,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The probability of mutation happening for an individual.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Mutation in this genetic algorithm is a random choise of correspondent  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; value from the param grid.  
- gen_mutation_prob=1.0/8,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The propapility for each gen to mutate.  
- do_plot : boolean, default=False,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Whether to plot the dependence of max, mean and min fittess of  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; generation.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Whether to log what is happening during the evolution of genetic   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; algorithm or not
