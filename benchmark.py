import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ==========================================
# CONFIG
# ==========================================
dims = 15
timesteps = 120

# ideal political baseline
mu = np.ones(dims) * 70

# utility spread
sigma = np.ones(dims) * 15

# weighted sum weights
weights = np.ones(dims) / dims

# ==========================================
# STORAGE
# ==========================================
consistent_signals = []
inconsistent_signals = []
extremist_high_signals = []
extremist_low_signals = []

# ==========================================
# CONSISTENT PARTY
# ==========================================
#
# stays near baseline ±5-10
#
for t in range(timesteps):

    shared_trend = np.sin(t / 18) * 1.5

    s = (
        mu
        + shared_trend
        + np.random.normal(0, 4, dims)
    )

    s = np.clip(s, 0, 100)

    consistent_signals.append(s)

consistent_signals = np.array(consistent_signals)

# ==========================================
# INCONSISTENT PARTY
# ==========================================
#
# unstable structure
#
for t in range(timesteps):

    s = []

    for i in range(dims):

        if np.random.rand() > 0.5:
            val = np.random.normal(85, 10)
        else:
            val = np.random.normal(45, 10)

        s.append(val)

    s = np.array(s)

    s = np.clip(s, 0, 100)

    inconsistent_signals.append(s)

inconsistent_signals = np.array(inconsistent_signals)

# ==========================================
# EXTREMIST HIGH PARTY
# ==========================================
#
# everything near 90-100
#
for t in range(timesteps):

    s = np.random.normal(95, 4, dims)

    s = np.clip(s, 0, 100)

    extremist_high_signals.append(s)

extremist_high_signals = np.array(extremist_high_signals)

# ==========================================
# EXTREMIST LOW PARTY
# ==========================================
#
# everything near 10-20
#
for t in range(timesteps):

    s = np.random.normal(15, 4, dims)

    s = np.clip(s, 0, 100)

    extremist_low_signals.append(s)

extremist_low_signals = np.array(extremist_low_signals)

# ==========================================
# METRIC FUNCTIONS
# ==========================================

# ------------------------------------------
# Weighted Sum
# ------------------------------------------
def weighted_sum(x):

    return np.dot(weights, x)

# ------------------------------------------
# Mahalanobis
# ------------------------------------------
cov = np.cov(consistent_signals.T)

cov += np.eye(dims) * 1e-3

sigma_inv = np.linalg.inv(cov)

def mahal_score(x):

    r = x - mu

    d = np.sqrt(
        r.T @ sigma_inv @ r
    )

    tau = 25

    score = 100 / (1 + d / tau)

    return score

# ------------------------------------------
# Modified Chi-Squared
# ------------------------------------------
#
# only penalize BELOW target
#
def modded_chi2_score(x):

    penalties = np.maximum(0, mu - x)

    chi2 = np.sum(
        (penalties ** 2) / (sigma ** 2)
    )

    tau = 15

    score = 100 / (1 + chi2 / tau)

    return score

# ------------------------------------------
# Bell Curve Utility
# ------------------------------------------
def bell_curve_score(x):

    utility = np.exp(
        -((x - mu) ** 2) /
        (2 * sigma ** 2)
    )

    score = 100 * np.mean(utility)

    return score

# ==========================================
# COMPUTE ALL METRICS
# ==========================================

party_data = {
    "Consistent": consistent_signals,
    "Inconsistent": inconsistent_signals,
    "Extremist High": extremist_high_signals,
    "Extremist Low": extremist_low_signals
}

results = {}

for name, signals in party_data.items():

    ws = []
    mahal = []
    chi2 = []
    bell = []

    for t in range(timesteps):

        s = signals[t]

        ws.append(
            weighted_sum(s)
        )

        mahal.append(
            mahal_score(s)
        )

        chi2.append(
            modded_chi2_score(s)
        )

        bell.append(
            bell_curve_score(s)
        )

    results[name] = {
        "weighted": ws,
        "mahal": mahal,
        "chi2": chi2,
        "bell": bell
    }

# ==========================================
# PLOTTING
# ==========================================

fig, axs = plt.subplots(
    4,
    1,
    figsize=(16, 18)
)

metric_names = [
    ("weighted", "Weighted Sum"),
    ("mahal", "Mahalanobis"),
    ("chi2", "Modified Chi-Squared"),
    ("bell", "Bell Curve Utility")
]

for ax, (metric_key, title) in zip(axs, metric_names):

    for party_name in results:

        ax.plot(
            results[party_name][metric_key],
            label=party_name
        )

    ax.set_title(title)
    ax.set_ylabel("Score")
    ax.legend()

axs[-1].set_xlabel("Time")

plt.tight_layout()
plt.show()

# ==========================================
# PRINT AVERAGES
# ==========================================

print("\n==============================")
print("AVERAGE SCORES")
print("==============================")

for party_name in results:

    print(f"\n--- {party_name} ---")

    print(
        "Weighted Sum:",
        round(np.mean(results[party_name]["weighted"]), 2)
    )

    print(
        "Mahalanobis:",
        round(np.mean(results[party_name]["mahal"]), 2)
    )

    print(
        "Modified Chi2:",
        round(np.mean(results[party_name]["chi2"]), 2)
    )

    print(
        "Bell Curve:",
        round(np.mean(results[party_name]["bell"]), 2)
    )
# ==========================================
# BAR GRAPH VISUALIZATION
# ==========================================

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# COMPUTE AVERAGES
# ==========================================

party_names = list(results.keys())

weighted_means = [
    np.mean(results[p]["weighted"])
    for p in party_names
]

mahal_means = [
    np.mean(results[p]["mahal"])
    for p in party_names
]

chi2_means = [
    np.mean(results[p]["chi2"])
    for p in party_names
]

bell_means = [
    np.mean(results[p]["bell"])
    for p in party_names
]

# ==========================================
# BAR POSITIONS
# ==========================================

x = np.arange(len(party_names))

width = 0.2

# ==========================================
# PLOT
# ==========================================

plt.figure(figsize=(14, 7))

plt.bar(
    x - 1.5 * width,
    weighted_means,
    width,
    label="Weighted Sum"
)

plt.bar(
    x - 0.5 * width,
    mahal_means,
    width,
    label="Mahalanobis"
)

plt.bar(
    x + 0.5 * width,
    chi2_means,
    width,
    label="Modified Chi²"
)

plt.bar(
    x + 1.5 * width,
    bell_means,
    width,
    label="Bell Curve Utility"
)

# ==========================================
# LABELS
# ==========================================

plt.xticks(x, party_names)

plt.ylabel("Average Score")

plt.title(
    "Comparison of Reputation Metrics Across Political Archetypes"
)

plt.legend()

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.3
)

plt.tight_layout()

plt.show()