import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, betabinom
from calc import fit_beta_binom

FONTSIZE = 32
FONTSIZE_SMALL = 22
FONTSIZE_AXIS = 22


def plot_diffs(files, n, show=False, printStats=False):
    differences = []

    for i, file in enumerate(files):
        diff = np.array([int(diff) for diff in open(file, "r").read()[:-1].split(",")])
        if i != 2:
            diff *= 2
        differences.append(diff)

    # Create the plot and histogram
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(16, 18), sharex=True)
    freqs = []

    for i, diffs in enumerate(differences):
        axis = axes[i]
        axis2 = axis.twinx()
        
        min_diff = 0
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        max_diff = 20

        max_y_axis = 4499

        x_axis = np.arange(min_diff, max_diff + 3, 2)

        freqs, _, _ = axis.hist(diffs, bins=x_axis, align='left', color='orange', alpha=0.9, edgecolor='black', linewidth=1)

        # Add vertical lines for the max difference
        axis.axvline(x=max_diff, color='red', linestyle='--', linewidth=2, label="Max. possible difference")

        # Plot a curve to match the distribution of the differences
        if i == 2:
            x_axis_fit = np.linspace(min_diff, max_diff + 1, 1000)
            pdf_fitted = norm.pdf(x_axis_fit, mean_diff, std_diff)
            axis2.plot(x_axis_fit, pdf_fitted, color='black', linestyle='-', linewidth=2, label="Normal dist")
        # Fit a beta binomial distribution to the data
        else:
            a, b = fit_beta_binom(x_axis, np.append(freqs, [0]), max_diff)

            mean_diff = betabinom.mean(max_diff, a, b, loc=0)
            std_diff = betabinom.std(max_diff, a, b, loc=0)

            pmf_fitted = betabinom.pmf(x_axis, max_diff, a, b, loc=0)
            axis2.plot(x_axis, pmf_fitted, color='black', linestyle='-', linewidth=2) #, label=fr"Beta binom:{chr(10)} $\alpha$={a:.2f}{chr(10)} $\beta$={b:.2f}")


        # Annotate the plot with a title
        x_coord = -1.68
        y_mod = 0.905
        if i == 0:
            text = "Differences between schedules"
            loc = (x_coord, max_y_axis * y_mod)
        elif i == 1:
            text = "Without home/away assignments"
            loc = (x_coord, max_y_axis * y_mod)
        else:
            text = "Only home/away assignments"
            loc = (x_coord, max_y_axis * y_mod)
        axis.annotate(text,
                        xy=(0, 0),
                        xytext=loc,
                        ha='left',
                        fontweight='bold',
                        bbox=dict(facecolor='#D3D3D3', edgecolor='black', boxstyle='round,pad=0.3'),
                        fontsize=FONTSIZE_SMALL)
        
        # Annotate the max difference
        if i == 0:
            height = max_y_axis * 0.8
        elif i == 1:
            height = max_y_axis * 0.55
        else:
            height = max_y_axis * 0.2
        axis.annotate("Maximum\ndifference",
                        xy=(max_diff, 0),
                        xytext=(max_diff - 0.4, height),
                        ha='left',
                        fontstyle='italic',
                        fontsize=FONTSIZE_SMALL)

        # Add vertical lines for the mean difference and annotate it
        axis.axvline(x=mean_diff, color='green', linestyle='--', linewidth=2)
        axis.annotate(rf"$\mu$: {mean_diff:.2f}",
                        xy=(mean_diff, 0),
                        xytext=(mean_diff, np.max(freqs) * 0.2),
                        ha='center',
                        bbox=dict(facecolor='#4DFE90', edgecolor='black', boxstyle='round,pad=0.2'),
                        fontsize=FONTSIZE_SMALL)
        
        # Annotate the beta binomial distribution with the alpha and beta values
        if i != 2:
            axis.annotate(rf"$\alpha$: {a:.2f}{chr(10)}$\beta$: {b:.2f}",
                      xy=(mean_diff, 0),
                      xytext=(14, np.max(freqs) * 0.55) if i == 0 else (12, np.max(freqs) * 0.75),
                      ha='right',
                      fontweight='bold',
                      fontsize=FONTSIZE_SMALL)

        # Code to only show every other x value
        # Checks to make sure the last value is the max difference
        x_values = x_axis[::2]

        # Set the labels and title
        axis.set_xticks(x_values)
        axis.grid(alpha=0.5)
        axis.tick_params(axis='both', which='major', labelsize=FONTSIZE_AXIS)
        axis2.tick_params(axis='both', which='major', labelsize=FONTSIZE_AXIS)
        axis2.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f"{val:.2f}"))

        # Makes sure both y-axes starts at 0
        axis.set_ylim(bottom=0, top=max_y_axis)
        axis2.set_ylim(bottom=0)

        if printStats:
            print(f"i: {i}\tMean: {mean_diff}  \tStd: {std_diff}")

    fig.supxlabel("Differences", fontsize=FONTSIZE)
    fig.text(-0.01, 0.5, "Frequency", va='center', ha='center', rotation=90, fontsize=FONTSIZE)  # Left side label
    fig.text(1.01, 0.5, "Probability density", va='center', ha='center', rotation=270, fontsize=FONTSIZE)  # Right side label

    plt.xticks(np.arange(0, 21, 2))
    plt.tight_layout()
    plt.savefig(f"Plots/LBA_n=4.png", bbox_inches='tight')
    
        
    if show:
        plt.show()


if __name__ == "__main__":
    files = ["./Differences/Diff All-4.csv", "./Differences/Diff Reduced All-4.csv", "./Differences/Diff Teamless All-4.csv"]
    n = 4

    plot_diffs(files, n, show=True, printStats=False)