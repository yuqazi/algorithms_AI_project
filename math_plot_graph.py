import matplotlib.pyplot as plt

def plot_predictions(y_test, y_pred):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             linestyle='--')
    plt.title("Actual vs Predicted SOH")
    plt.xlabel("Actual SOH")
    plt.ylabel("Predicted SOH")
    plt.grid()
    plt.savefig("actual_vs_predicted.png")
    #plt.show()