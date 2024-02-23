# Study 1 - Opinion Mining: Replication Package

The repository shares a replication package for the first experiment conducted in the study: J. Dąbrowski et al.,
"Mining and Searching App Reviews for Requirements Engineering: Evaluation and Replication Studies", Information Systems, 2023.

## About

### Goal

The goal of the experiment was to evaluate and compare approaches for mining user opinions. We here provide the replication package for the first experiment and the description of how to run it.


For any information, please contact the main contributor: Jacek Dąbrowski (jacek.dabrowski.16@alumni.ucl.ac.uk)

or

[Create new issue](https://github.com/jsdabrowski/IS-22/issues/new) for further information.

## Repository Structure

The repository contains the following directories:

- ``` Dataset/ ``` : Collected app reviews and the ground truth
- ``` Documents/ ``` : Annotation guideline, preprint of the paper and a template in which  outputs from tools will be generated.
- ``` Scripts/ ``` : Scripts with evaluation methods for feature extraction and feature-specific sentiment analysis.
- ``` Tools/ ``` : Re-implemented GuMa tool, and references to SAFE and ReUS tools

## How to Run the Experiment

```
The general procedure for running the first experiment consists of the following steps:
1: Download Ground_truth.xls
2: Download Experiment_template.xls
3: Make sure app reviews and annotated features from Ground_truth.xls are copied to Experiment_template.xls
4: Download a tool for feature extraction and/or feature-specific sentiment analysis that you want to evaluate
5: Make sure the tool is configured to generate outputs to Experiment_template.xls
6: Run the tool
7: Run evaluation_method_features.py script comparing the tool output with the ground truth
8: Refresh cells in Experiment_template.xls to compute effectiveness metrics
9: Run evaluation_method_sentiment.py script to compute the sentiment
```

## Citation

If you intend to use this work, please cite us:

```
@article{DBLP:journals/is/DabrowskiLPS23,
  author       = {Jacek Dabrowski and
                  Emmanuel Letier and
                  Anna Perini and
                  Angelo Susi},
  title        = {Mining and searching app reviews for requirements engineering: Evaluation
                  and replication studies},
  journal      = {Inf. Syst.},
  volume       = {114},
  pages        = {102181},
  year         = {2023},
  url          = {https://doi.org/10.1016/j.is.2023.102181},
  doi          = {10.1016/J.IS.2023.102181},
  timestamp    = {Sat, 13 May 2023 01:06:45 +0200},
  biburl       = {https://dblp.org/rec/journals/is/DabrowskiLPS23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

or

```
@InProceedings{10.1007/978-3-030-49435-3_25,
  author    = {Dąbrowski, Jacek and Letier, Emmanuel and Perini, Anna and Susi, Angelo},
  title     = {Mining User Opinions to Support Requirement Engineering: An Empirical Study},
  booktitle = {Advanced Information Systems Engineering},
  year      = {2020},
  editor    = {Dustdar, Schahram and Yu, Eric and Salinesi, Camille and Rieu, Dominique and Pant, Vik},
  pages     = {401--416},
  address   = {Cham},
  publisher = {Springer International Publishing},
  isbn      = {978-3-030-49435-3},
}

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
