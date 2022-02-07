# Study 2 - Searching Feature-Specific Reviews: Replication Package

The repository shares a replication package for the second experiment conducted in the study: J. Dąbrowski et al.,
"Mining and Searching App Reviews for Requirements Engineering: Evaluation and Replication Studies", [Update Once Paper Accepted], 2022.

## About

### Goal

The goal of the experiment was to evaluate and compare approaches for finding feature-specific app reviews. We here provide the replication package for the second experiment and the description of how to run it.


For any information, please contact the main contributor: Jacek Dąbrowski (j.dabrowski@cs.ucl.ac.uk)

or

[Create new issue](https://github.com/jsdabrowski/IS-21/issues/new) for further information.

## Repository Structure

The repository contains the following directories:

- ``` Dataset/ ``` : Collected app reviews and the ground truth (queried features and annotated app reviews).
- ``` Documents/ ``` : Annotation guideline, preprint of the paper and a template in which  outputs from tools will be generated.
- ``` Tools/ ``` : Re-implemented MARAM and our Lucene-based tool, and references to SAFE.

## How to Run the Experiment

```
The general procedure for running the first experiment consists of the following steps:
1: Download a sample of collected reviews and a list of queries.
2: Download a tool for finding feature-related app reviews.
3: Make sure the tool is configured to query a desired feature and generate outputs to an intended localisation.
4: Run the tool.
```

## Citation

If you intend to use this work, please cite us:

```
<Update Once Paper Accepted>
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
