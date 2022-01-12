from setuptools import setup

setup(
    name='genetic_search',
    version='0.1.0',
    description='Hyperparameter search via genetic algorithm',
    long_description='''This is a tool for optimising sklearn-compatible models' hyperparameters.
It uses genetic algorithm so, it is much faster than GridSearchCV and gives
more consistent results than RandomizedSearchCV.\n\n
The class GeneticSearchCV is extended of the sklearn's class BaseSearchCV, so
it has the same functionality as sklearn's searches.''',
    url='https://github.com/kok42/genetic-search',
    author='Menshenin Andrew',
    author_email='menshenin-2001@mail.ru',
    license='The Universal Permissive License (UPL)',
    packages=['genetic_search'],
    install_requires=['sklearn',
                      'numpy',
                      'deap',
                      'matplotlib'],
)
