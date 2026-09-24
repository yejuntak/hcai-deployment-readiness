# Citation audit: HCAI Deployment Readiness Protocol

Audit date: September 8, 2026 (America/Chicago). Source reviewed: v0.1-rc.2. Corrections prepared for v0.1-rc.3.

## Findings

All twelve cited works were located in primary publication, author, institutional, or standards sources. No fabricated work was identified. Three bibliographic issues require correction: the first author's initial in [7], the mixed preprint/conference identity in [8], and the omitted subtitle in [10]. The claims made in the protocol are generally supported at the stated conceptual level. None of these sources validates this protocol, its thresholds, or its effectiveness.

This was an AI-assisted bibliographic and claim-support audit, not independent peer review. Full relevant source sections were inspected where available. For [10] and [11], the claim check relies on the institutional/publisher abstract rather than a complete reading of the subscription article. A URL failing in one retrieval tool was not treated as proof that the work did not exist. Crossref rate limits prevented some secondary metadata requests; primary sources were used instead.

## 1. NIST AI RMF 1.0

Reference: National Institute of Standards and Technology. Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1, January 2023.

Primary source: https://doi.org/10.6028/NIST.AI.100-1

Verified the report title, number, date and DOI on the PDF. MAP 1.6, printed p. 26, concerns eliciting system requirements. MEASURE 1.3, 2.1 and 2.3, p. 29, concern independent assessment, measurement documentation and assessment under relevant conditions. MEASURE 2.13, p. 30, concerns evaluation of TEVV metrics and processes. These support the conceptual mapping in section 7. They do not prescribe the protocol's all-items handoff gate. NIST institutional attribution is acceptable here; Crossref separately credits Elham Tabassi. No correction required.

## 2. NIST TEVV-Athlon initial public draft

Reference: Phillips, P. J., et al. The TEVV-Athlon Framework for Evaluating AI Systems. NIST AI 200-2 ipd, August 2026.

Primary PDF: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.200-2.ipd.pdf

DOI: https://doi.org/10.6028/NIST.AI.200-2.ipd

The title page lists P. Jonathon Phillips, Theodore Jensen, Patrick Hall, Razvan Amironesei, Yee-Yin Choong, Craig Greenberg and Kristen K. Greene. Section 2.4, printed p. 7, describes synthesis of evaluation evidence for organizational decisions. Appendix E, Table 7, p. 28, covers objectives, baselines, procedures and variables/conditions. Both pinpoint references are correct. The source is an initial public draft, not a finalized standard. It does not verify Tak's email transmission, receipt or adoption; those are separate provenance claims. No correction required.

## 3. Nielsen's usability heuristics

Primary source: https://www.nngroup.com/articles/ten-usability-heuristics/

Verified Jakob Nielsen, the title, publication date April 24, 1994, and last-reviewed date January 30, 2024. Heuristics 1, 3, 5 and 9 directly cover system status, user control, error prevention and recovery. These are general design heuristics; they do not establish the novelty or effectiveness of the new protocol. The existing undated web citation identifies the work correctly. No factual correction required.

## 4. Guidelines for Human-AI Interaction

Primary author-hosted paper: https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf

DOI verified on the paper's first page: https://doi.org/10.1145/3290605.3300233

Verified Saleema Amershi as first author and CHI 2019. The abstract describes 18 guidelines and a study with 49 design practitioners examining 20 products. This supports the protocol's statement that the guidelines were evaluated with practitioners. That evaluation is evidence about those guidelines, not about Tak's protocol. Add the verified DOI for citation convenience; no underlying factual error found.

## 5. People + AI Guidebook: Errors + Graceful Failure

Primary source: https://pair.withgoogle.com/chapter/errors-failing/

Verified the Google PAIR chapter title and content. The low-confidence section discusses uncertainty constraints, while the return-control section discusses transitions to manual control and the information users need. This supports the protocol's treatment of failures, uncertainty and fallback paths. The source also recognizes that manual override may not be appropriate in every context; the protocol's applicability-based scope does not assert universal override. No correction required.

## 6. The ML Test Score

Primary source: https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/

Verified Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib and D. Sculley; Proceedings of IEEE Big Data, 2017; and the complete title. The abstract describes 28 tests and monitoring needs for production ML systems. The protocol accurately cites this as a production-readiness rubric and distinguishes its own interface-specification assessment. No correction required.

## 7. HINT

Primary paper: https://www.microsoft.com/en-us/research/wp-content/uploads/2022/05/HINT-IUI-22.pdf

Primary publication record: https://www.microsoft.com/en-us/research/publication/hint-integration-testing-for-ai-based-features-with-humans-in-the-loop/

DOI verified on the paper: https://doi.org/10.1145/3490099.3511141

The first author is Quanze Chen, followed by Tobias Schnabel, Besmira Nushi and Saleema Amershi. The venue is IUI 2022. Correct Chen, C. to Chen, Q. The source describes crowd-based testing of AI experiences and practitioner evaluation before deployment, supporting the protocol's summary. Add the verified DOI. This correction concerns attribution; the research cited is real and relevant.

## 8. From Accuracy to Readiness

Version actually inspected: https://arxiv.org/abs/2603.18895v1

Full text inspected: https://arxiv.org/html/2603.18895v1

Verified author Min Hun Lee and submission date March 19, 2026. The inspected preprint title is From Accuracy to Readiness: Metrics and Benchmarks for Human-AI Decision-Making. Its taxonomy covers outcomes, reliance, safety and learning/readiness, including calibration and harm. It supports the protocol's conceptual summary.

The related ACM record, DOI 10.1145/3772363.3798377, has the longer title ending in An Initial Exploration. The old reference combined the preprint title/link with a conference label. Cite the inspected arXiv v1 explicitly rather than implying that the conference version was the text examined. This is version disambiguation, not evidence that the work is nonexistent.

## 9. How to measure metacognition

Primary source: https://doi.org/10.3389/fnhum.2014.00443

Verified Stephen M. Fleming and Hakwan C. Lau; Frontiers in Human Neuroscience, volume 8, article 443; July 15, 2014. The abstract and measurement discussion distinguish bias, sensitivity and efficiency, and discuss calibration/discrimination. This supports caution about what an expected-recall discrepancy measures. It does not validate the protocol's specific session-level subtraction formula. The current protocol explicitly avoids that stronger claim. No correction required.

## 10. Prototype fidelity and aesthetics

Institutional source: https://susi.usi.ch/global/documents/302252

DOI: https://doi.org/10.1016/j.apergo.2008.06.006

Verified Jürgen Sauer and Andreas Sonderegger; 2009; Applied Ergonomics, volume 40, pp. 670-677. The full title includes Effects on user behaviour, subjective evaluation and emotion, which was omitted from the old reference. Restore it and add the DOI. The DOI's 2008 component does not change the 2009 publication year. The institutional abstract reports a 60-participant study and conditional effects of prototype fidelity/aesthetics. This supports the cautious statement about effects under particular conditions, not an AI-specific or universal causal claim.

## 11. Does the Fidelity of Software Prototypes Affect the Perception of Usability?

Publisher source: https://journals.sagepub.com/doi/10.1177/154193129203600429

Verified Michael E. Wiklund, Christopher Thurrott and Joseph S. Dumas; October 1992; Proceedings of the Human Factors and Ergonomics Society Annual Meeting, volume 36, issue 4. The publisher abstract reports no bias in perceived usability within the aesthetic range studied. This supports the protocol's mention of null findings. It does not show that fidelity never matters. The existing DOI, authors, title and year are correct. Add the venue and volume/issue for completeness without inventing an unchecked page range.

## 12. The Evaluator Effect

Author manuscript: https://mortenhertzum.dk/publ/IJHCI2001.pdf

Publisher record: https://www.tandfonline.com/doi/abs/10.1207/S15327590IJHC1304_05

Verified Morten Hertzum and Niels Ebbe Jacobsen; International Journal of Human-Computer Interaction, 13(4), 421-443, 2001. The author manuscript reviews eleven studies and describes disagreement in problem detection and severity. The existing DOI is correct. Search results also surfaced a different 2003 record/DOI; it must not replace the DOI for the cited 2001 article. The protocol's claim about evaluator disagreement is supported. The prescribed validation workflow remains the protocol author's methodological proposal.

## Release checks

Preserve the twelve reference numbers and their claim links. Change bibliographic entries only, apart from release identity and correction notes. Preserve the formulas, worked-example data, limitations and AI-assistance disclosure. Retain rc.2 as historical evidence; distribute corrected files under rc.3. This audit does not convert a proposed method into a validated method.
