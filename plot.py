from matplotlib import pyplot as plt

# plot function
def plot_mlscore(ml_score) :
    ml_score.sort()
    plt.plot(ml_score)
    plt.show()