# COMPSCI 760 Statistical analysis Q4

**Q4. Does the Direct minus Cascade gap depend on accent?**

Direct performs better than both cascade systems in every accent, although the size of the advantage varies. Overall, Direct scores 7.0 chrF++ points higher than Cascade-600M (95% CI [6.5, 7.6]) and 5.0 points higher than Cascade-3.3B (95% CI [4.4, 5.7]), using speaker-clustered intervals (`intervals_long.csv`). The per-accent intervals exclude zero for both comparisons in all seven accents.

Against Cascade-600M, the gap is largest for Hong Kong, Malaysian, Filipino, and India and South Asia speakers (7.6 to 8.4) and smallest for Southern African and England English speakers (5.5 and 5.4). Against Cascade-3.3B, it is largest for Hong Kong (7.0), Malaysian (5.7), and India and South Asia speakers (5.4), and smallest for Southern African speakers (3.5). The matched-pairs rank-biserial correlations are positive in every accent (0.53–0.93 against Cascade-600M and 0.39–0.91 against Cascade-3.3B), indicating that the paired score differences consistently favour Direct within each accent.

The size of the gap varies by accent, but the effect is small. Kruskal–Wallis tests on speaker-mean gaps give H(6) = 21.4, p = 0.0015, epsilon-squared = 0.014 for Direct vs Cascade-600M, and H(6) = 17.2, p = 0.009, epsilon-squared = 0.011 for Direct vs Cascade-3.3B (`tests.csv`, Kruskal–Wallis rows, speaker level). The clip-level tests yield similar results (p = 0.0015 and p = 0.018).

After Holm correction, only 2 of the 21 accent pairs show significant differences for Direct vs Cascade-600M, and only 1 of 21 for Direct vs Cascade-3.3B at the speaker level. The pairwise effects are small, with Cliff's delta magnitudes ranging from 0.23 to 0.30. The clearest difference for Direct vs Cascade-600M is between England English and Malaysian English (adjusted p = 0.005).

The gaps tend to be larger for Hong Kong, Malaysian, Filipino, and India and South Asia speakers, and smaller for England English and Southern African speakers. This is consistent with the Q3 results: Direct's accent means vary relatively little, so most of the variation in the Direct-minus-Cascade gap comes from the cascade systems.

We should still be cautious because the per-accent intervals are not adjusted for multiple comparisons, and the Hong Kong English estimate is based on only 41 speakers. More importantly, the systems differ in model family, size, and training data, so the observed differences cannot be attributed to accent handling alone.

Two results warrant particular caution: the speaker-level p = 0.041 for Cascade-600M in Q3, which is close to the conventional 0.05 threshold, and the fact that only 2 of 21 pairwise comparisons are significant in Q4 for Direct vs Cascade-600M, with only 1 of 21 significant for Direct vs Cascade-3.3B.