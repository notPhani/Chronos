# ==========================================
# HYBRID UTILITY MODEL
# ==========================================
#
# u_i(x) =
# α_i * Bell(x)
# +
# (1 - α_i) * Chi2(x)
#
# Then aggregate using:
# geometric mean
#
# ==========================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ==========================================
# CONFIG
# ==========================================
dims = 15
timesteps = 120

mu = np.ones(dims) * 70
sigma = np.ones(dims) * 15

epsilon = 1e-6

# ==========================================
# ALPHA VECTOR
# ==========================================
#
# α_i near 1
# -> equilibrium-sensitive
#
# α_i near 0
# -> maximize-sensitive
#

alpha = np.array([

    # P01 Electoral Strength
    0.3,

    # P02 Legislative Performance
    0.4,

    # P03 Constituency Development
    0.5,

    # P04 Public Accessibility
    0.8,

    # P05 Communication
    0.8,

    # P06 Party Standing
    0.5,

    # P07 Media Coverage
    0.9,

    # P08 Digital Influence
    0.95,

    # P09 Financial Muscle
    0.3,

    # P10 Alliance Intel
    0.5,

    # P11 Caste Equation
    0.7,

    # P12 Anti-Incumbency
    1.0,

    # P13 Grassroots Network
    0.2,

    # P14 Ideology Consistency
    0.9,

    # P15 Scandal Index
    1.0

])

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
for t in range(timesteps):

    s = np.random.normal(95, 4, dims)

    s = np.clip(s, 0, 100)

    extremist_high_signals.append(s)

extremist_high_signals = np.array(extremist_high_signals)

# ==========================================
# EXTREMIST LOW PARTY
# ==========================================
for t in range(timesteps):

    s = np.random.normal(15, 4, dims)

    s = np.clip(s, 0, 100)

    extremist_low_signals.append(s)

extremist_low_signals = np.array(extremist_low_signals)

# ==========================================
# PARTY DATA
# ==========================================
party_data = {
    "Consistent": consistent_signals,
    "Inconsistent": inconsistent_signals,
    "Extremist High": extremist_high_signals,
    "Extremist Low": extremist_low_signals
}

# ==========================================
# BELL UTILITY
# ==========================================
def bell_utility(x, mu, sigma):

    return np.exp(
        -((x - mu) ** 2) /
        (2 * sigma ** 2)
    )

# ==========================================
# CHI2 UTILITY
# ==========================================
#
# only penalize below-target
#
def chi2_utility(x, mu, sigma):

    penalties = np.maximum(0, mu - x)

    return 1 / (
        1 +
        (penalties ** 2) /
        (sigma ** 2)
    )

# ==========================================
# HYBRID UTILITY
# ==========================================
def hybrid_utility(x):

    bell = bell_utility(
        x,
        mu,
        sigma
    )

    chi2 = chi2_utility(
        x,
        mu,
        sigma
    )

    utility = (
        alpha * bell
        +
        (1 - alpha) * chi2
    )

    return utility

# ==========================================
# GEOMETRIC AGGREGATION
# ==========================================
def geometric_nri(x):

    utility = hybrid_utility(x)

    floored = np.maximum(
        utility,
        epsilon
    )

    nri = np.exp(
        np.mean(
            np.log(floored)
        )
    )

    return nri * 100

# ==========================================
# COMPUTE RESULTS
# ==========================================
results = {}

for party_name, signals in party_data.items():

    scores = []

    for t in range(timesteps):

        s = signals[t]

        score = geometric_nri(s)

        scores.append(score)

    results[party_name] = scores

# ==========================================
# PLOT TEMPORAL TRAJECTORIES
# ==========================================
plt.figure(figsize=(14, 7))

for party_name in results:

    plt.plot(
        results[party_name],
        label=party_name
    )

plt.title(
    "Hybrid Utility + Geometric Aggregation NRI"
)

plt.xlabel("Time")
plt.ylabel("NRI Score")

plt.legend()

plt.grid(
    linestyle='--',
    alpha=0.3
)

plt.tight_layout()
plt.show()

# ==========================================
# BAR GRAPH
# ==========================================
party_names = list(results.keys())

means = [
    np.mean(results[p])
    for p in party_names
]

plt.figure(figsize=(10, 6))

bars = plt.bar(
    party_names,
    means
)

plt.title(
    "Average Hybrid-Geometric NRI"
)

plt.ylabel("Average Score")

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.3
)

plt.tight_layout()
plt.show()

# ==========================================
# PRINT AVERAGES
# ==========================================
print("\n==============================")
print("HYBRID GEOMETRIC NRI")
print("==============================")

for party_name in results:

    print(
        f"{party_name}:",
        round(np.mean(results[party_name]), 2)
    )