from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# utility function to plot the decision surface
def plot_surface(est, x_1, x_2, ax=None, threshold=0.0, contourf=False):
    """Plots the decision surface of ``est`` on features ``x1`` and ``x2``. """
    xx1, xx2 = np.meshgrid(np.linspace(x_1.min(), x_1.max(), 100),
                           np.linspace(x_2.min(), x_2.max(), 100))
    # plot the hyperplane by evaluating the parameters on the grid
    X_pred = np.c_[xx1.ravel(), xx2.ravel()]  # convert 2d grid into seq of points
    if hasattr(est, 'predict_proba'):  # check if ``est`` supports probabilities
        # take probability of positive class
        pred = est.predict_proba(X_pred)[:, 1]
    else:
        pred = est.predict(X_pred)
    Z = pred.reshape((100, 100))  # reshape seq to grid
    if ax is None:
        ax = plt.gca()
    # plot line via contour plot
    
    '''if contourf:
        ax.contourf(xx1, xx2, Z, levels=np.linspace(0, 1.0, 25), cmap=plt.cm.RdBu, alpha=0.6)'''
    ax.contour(xx1, xx2, Z, levels=[threshold], colors='black')
    diff1 = (x_1.max() - x_1.min()) / 10
    diff2 = (x_2.max() - x_2.min()) / 10

    ax.set_xlim((x_1.min() - diff1, x_1.max() + diff1))
    ax.set_ylim((x_2.min() - diff2, x_2.max() + diff2))




def plot_dataset(X_train, y_train, X_test=None, y_test=None, est=None):
    fig, ax = plt.subplots(1, 1)
    
    # plot review lighter than training
    cm_bright = ListedColormap(['#FF0000', '#0000FF'])
    # Plot the training points
    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright)
    if X_test is not None and y_test is not None: 
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6)
    # and testing points
    # plot limits
    ax.set_xlim(X_train[:, 0].min(), X_train[:, 0].max())
    ax.set_ylim(X_train[:, 1].min(), X_train[:, 1].max())
    # no ticks
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_ylabel('$x_1$')
    ax.set_xlabel('$x_0$')
    if est is not None:
        est.fit(X_train, y_train)
        plot_surface(est, X_train[:, 0], X_train[:, 1], ax=ax, threshold=0.5, contourf=True)
        if y_test is not None and X_test is not None:
            err = (y_test != est.predict(X_test)).mean()
            ax.text(0.88, 0.02, '%.2f' % err, transform=ax.transAxes)
            


''' Datasets is a dictionary of dictionary's. Each element in datasets is a 'name' and a 
    dictionary of 'X_train', 'X_test', 'y_train', and 'y_test' '''
def plot_datasets(datasets, est=None): 
    """Plotsthe decision surface of ``est`` on each of the three datasets. """
    fig, axes = plt.subplots(1, 3, figsize=(10, 4))
    for (name, ds), ax in zip(datasets.iteritems(), axes):
        X_train = ds['X_train']
        y_train = ds['y_train']
        X_test = ds['X_test']
        y_test = ds['y_test']
        
        # plot review lighter than training
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        # Plot the training points
        ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright)
        # and testing points
        ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6)
        # plot limits
        ax.set_xlim(X_train[:, 0].min(), X_train[:, 0].max())
        ax.set_ylim(X_train[:, 1].min(), X_train[:, 1].max())
        # no ticks
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_ylabel('$x_1$')
        ax.set_xlabel('$x_0$')
        ax.set_title(name)
        if est is not None:
            est.fit(X_train, y_train)
            plot_surface(est, X_train[:, 0], X_train[:, 1], ax=ax, threshold=0.5, contourf=True)
            err = (y_test != est.predict(X_test)).mean()
            ax.text(0.88, 0.02, '%.2f' % err, transform=ax.transAxes)
            
    fig.subplots_adjust(left=.02, right=.98)
