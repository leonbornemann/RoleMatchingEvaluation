# Role Matching Evaluation Scripts


Code Repository for the Submission "Role Matching in Temporal Data " to VLDB 2022. (Evaluation)

# Abstract

We present role matchings, a novel, fine-grained integrity constraint on temporal fact data, i.e., ⟨subject, predicate, object, timestamp⟩-quadruples. A role is a combination of subject and predicate and can be associated with different objects as the real world evolves and the data changes over time. A role matching is a novel constraint that states that  the associated object of two or more different roles should always match at the same timestamps. Once discovered, role matchings can serve as integrity constraints that, if  violated, can alert editors and thus allow them to correct the error. We present compatibility-based role matching (CBRM), an algorithm to discover role matchings in large datasets, based on their change histories.

We evaluate our method on datasets from the Socrata open government data portal, as well as Wikipedia infoboxes, showing that our approach can process large datasets of up to  3.5 million roles containing up to 17 million changes. Our approach consistently outperforms baselines, achieving almost 30 percentage points more F-Measure on average

# Usage

The repository contains two python3 jupyter notebooks (https://jupyter.org/), that draw plots or print out the precision/recall/f1 measures. To execute the main evaluation, you need the output data (csv files) of the [CBRM](https://github.com/leonbornemann/CompatibilityBasedRoleMatching) evaluation script (files from the original experiments as described in the paper are available [here](https://owncloud.hpi.de/s/nIkIyYY97pNovAZ)). To re-execute the tuning and general statistics, you need statistics about the edges from the [CBRM](https://github.com/leonbornemann/CompatibilityBasedRoleMatching) evaluation scripts (files from the original experiments as described in the paper are available [here](https://owncloud.hpi.de/s/j0QFeDbJS70YKG0))