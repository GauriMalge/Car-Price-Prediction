import seaborn as sns
import matplotlib.pyplot as plt




def generate_plots(df):
    """Generates figures and returns them for Gradio formatting instead of using plt.show()."""
    # Plot 1: Histogram of Horsepower
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x="horsepower", bins=3, ax=ax1)
    ax1.set_title("Distribution of Horsepower")
    plt.close(fig1)

    # Plot 2: Barplot of Binned Horsepower vs Price
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="binned_horsepower", y="price", ax=ax2)
    ax2.set_title("Binned Horsepower vs Price")
    plt.close(fig2)

    # Plot 3: Lineplot of Price vs City-L/100km
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.lineplot(x=df["city-L/100km"], y=df["price"], marker="*", ax=ax3)
    ax3.set_title("Price vs City-L/100km")
    ax3.set_xlabel("City-L/100km")
    ax3.set_ylabel("Price")
    plt.close(fig3)

    # Plot 4: Histogram of body-style
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x="body-style", ax=ax4)
    ax4.set_title("Distribution of Body Styles")
    plt.close(fig4)

    # Plot 5: Barplot of body-style vs price segmented by fuel-type
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="body-style", y="price", hue="fuel-type", palette="Set2", ax=ax5)
    ax5.set_title("Body Style vs Price by Fuel Type")
    plt.close(fig5)

    return fig1, fig2, fig3, fig4, fig5
