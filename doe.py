"""This module contains functions for design of experiments analysis for HW 4 in AE 498 Data-Driven Modeling and Optimization."""

from numbers import Integral
import numpy as np
import matplotlib.pyplot as plt
# We define the signs first
# Each row has the contrast signs for A, B, then AB
# The interaction signs are the elementwise product of the A and B signs
_SIGNS = np.array([[-1, 1, -1, 1], [-1, -1, 1, 1], [1, -1, -1, 1]])

# Now we write a function to check whether input data is compatible; no effects are calculated here

def _validate(responses, n_replicates):
    """Validate a complete, balanced design without silently dropping data."""
    if isinstance(n_replicates, (bool, np.bool_)) or not isinstance(n_replicates, Integral):
        raise ValueError('n_replicates must be a positive integer.')
    if n_replicates < 1:
        raise ValueError('n_replicates must be a positive integer.')
    values = np.asarray(responses, dtype=float)
    # a 2^2 experiment has four treatments, each with the same number of boards
    if values.shape != (4, n_replicates):
        raise ValueError('responses must have shape (4, n_replicates).')
    # reject garbage values
    if not np.isfinite(values).all():
        raise ValueError('responses must contain only finite numeric values.')
    return values


def effects(responses, n_replicates):
    """Function to calculate main and interaction effects for a 2^2 factorial experiment.

    Parameters
    ----------
    responses : array_like
        Input response data (4 x n_replications dimensions), where each row is an observed response for a condition (ordered in the standard order) and each column is a replicate.
        For example, responses[0,1] = response from replicate 1 for condition (1), responses[1,1] = response from replicate 1 for condition a.
    n_replicates : int
        Number of replications in the experiment data.

    Returns
    -------
    effects : array_like
        Calculated effects (3 x 1 dimensions) for A, B, and AB.

    Notes
    -----
    Standard order of experiment conditions (order of rows in responses) = (1), a, b, ab
    """

    # YOUR CODE HERE
    # Suman's code
    values = _validate(responses, n_replicates) # checking validity of data
    # Now, we calculate all effects at once using matrix multiplication for row data and signs 
    # Then divide with 2n to get means
    return _SIGNS @ values.sum(axis=1) / (2 * n_replicates)
    

def plot_effects(responses, n_replicates):
    """Function to plot effects for a 2^2 factorial experiment.

    Parameters
    ----------
    responses : array_like
        Input response data (4 x n_replications dimensions), where each row is an observed response for a condition (ordered in the standard order) and each column is a replicate.
        For example, responses[0,1] = response from replicate 1 for condition (1), responses[1,1] = response from replicate 1 for condition a.
    n_replicates : int
        Number of replications in the experiment data.

    Returns
    -------
    out : list
        List of artists added.

    Notes
    -----
    This function structure is based on matplotlib's suggested signature function for returning a plot:
    https://matplotlib.org/3.5.0/tutorials/introductory/usage.html#the-object-oriented-interface-and-the-pyplot-interface
    """

    # YOUR CODE HERE
    # Suman's code
    means = _validate(responses, n_replicates).mean(axis=1) # check data
    ax = plt.gca()
    out = ax.plot([-1, 1], means[[0, 1]], 'o--', label='B− (low)')
    out += ax.plot([-1, 1], means[[2, 3]], 's--', label='B+ (high)')
    ax.set(xticks=[-1, 1], xticklabels=['Low, −', 'High, +'],
           xlabel='Factor A', ylabel='Mean response', title='Factorial interaction plot')
    ax.legend()
    ax.grid(alpha=0.2)
    return out


def plot_tornado(responses, n_replicates):
    """Function to make a tornado plot for a 2^2 factorial experiment.

    Parameters
    ----------
    responses : array_like
        Input response data (4 x n_replications dimensions), where each row is an observed response for a condition (ordered in the standard order) and each column is a replicate.
        For example, responses[0,1] = response from replicate 1 for condition (1), responses[1,1] = response from replicate 1 for condition a.
    n_replicates : int
        Number of replications in the experiment data.

    Returns
    -------
    out : list
        List of artists added.

    Notes
    -----
    This function structure is based on matplotlib's suggested signature function for returning a plot:
    https://matplotlib.org/3.5.0/tutorials/introductory/usage.html#the-object-oriented-interface-and-the-pyplot-interface
    """

    # YOUR CODE HERE
    # Suman's code
    values = effects(responses, n_replicates)
    order = np.argsort(-np.abs(values), kind='stable')
    ax = plt.gca()
    bars = ax.barh(np.arange(3), values[order],
                   color=['#226b91' if v >= 0 else '#c56b42' for v in values[order]])
    ax.set(yticks=np.arange(3), yticklabels=np.array(['A', 'B', 'AB'])[order],
           ylim=(2.5, -0.5), xlabel='Average effect (high − low)',
           ylabel='Factor or interaction', title='Tornado plot of effects')
    ax.axvline(0, color='0.25', linewidth=0.8)
    ax.grid(axis='x', alpha=0.2)
    return list(bars)
