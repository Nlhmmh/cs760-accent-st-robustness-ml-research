# COMPSCI 760 Statistical analysis Q3

**Q3. How much does accent move each system?**

Accent has a relatively small effect on chrF++ for all three systems. The between-accent spread is 1.7 [1.4, 5.1] for Direct, 2.7 [2.0, 4.7] for Cascade-600M, and 3.2 [2.0, 5.7] for Cascade-3.3B (`accent_means_ci.csv`). These spreads are smaller than the 5–7-point differences between the overall system means.

For Direct, the accent means range from 27.2 for Southern African to 28.9 for Filipino. Cascade-600M ranges from 19.8 for India and South Asia to 22.5 for England English, while Cascade-3.3B ranges from 21.3 for Hong Kong English to 24.5 for Filipino. The bootstrap intervals for the spreads are somewhat right-skewed, which is expected because the maximum-minus-minimum statistic can be biased upward when calculated from noisy means.

At the speaker level, accent is associated with Cascade-600M scores (H(6) = 13.2, p = 0.041, epsilon-squared = 0.0083; `tests.csv`, Kruskal–Wallis rows, speaker level), but there is no clear evidence of an accent effect for Cascade-3.3B (p = 0.17) or Direct (p = 0.18). The clip-level tests detect accent effects for both cascades (p = 0.006), but likely overstate the evidence because they treat repeated clips from the same speaker as independent. Overall, the effect sizes are small, with epsilon-squared no larger than 0.0083.

We also cannot conclude that accent affects one system more than another. The intervals for the differences in spread all include zero; for example, the difference between Direct and Cascade-600M is -1.0 [-2.3, 2.3].

The accent orderings also differ across systems. The two cascades show similar orderings (Spearman rho = 0.82), while Direct does not follow the same pattern as either cascade (rho = -0.18 against Cascade-600M and -0.07 against Cascade-3.3B; `tests.csv`, `accent_order_spearman` rows). These correlations are calculated across only seven accent means, and no confidence intervals were computed for them, so they should be interpreted cautiously. For example, Hong Kong English is the second-highest accent for Direct (28.3), but the lowest or close to the lowest for the cascades. The accents also have different numbers of independent speakers, ranging from 41 for Hong Kong English and 61 for Malaysian to 72 for Filipino and 527 for US English, so the uncertainty around the accent means is not the same across accents.

Overall, accent appears to have only a small effect on chrF++, and the pattern differs for Direct and the two cascades. However, these are associations rather than causal effects, since the systems differ in model family, size, and training data.