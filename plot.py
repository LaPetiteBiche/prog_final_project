from matplotlib import pyplot as plt

def plot_mlscore(ml_score) :
    ml_score.sort()
    plt.plot(ml_score)
    plt.show()