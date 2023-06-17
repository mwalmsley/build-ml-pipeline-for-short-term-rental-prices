# Udacity MLOps Engineer course project - Build an ML Pipeline for Short-Term Rental Prices in NYC

This repo contains my solution to a udacity course project. I use mlflow and wandb to make an automated reproducible pipeline for predicting airbnb prices in NYC. I wrap this pipeline with hydra for easy configuration and hparam searches.

## Submission details

WandB public workspace: https://wandb.ai/jbca-ice/nyc_airbnb
GitHub repo: https://github.com/mwalmsley/build-ml-pipeline-for-short-term-rental-prices

## Installation errors

protobuf and numpy both cause errors when running any pipeline step, as they have been upgraded (and are not pinned) while the mlflow version is pinned.

The following needs to be added to every conda.yml

   protobuf==3.20
   numpy==1.19.0

To fix this on the remote components (`data_split`) I'm adding them directly to `/src`. I still use `wandb_utils.log_artifact` from the remote repo.

## Command used

HParam search

   #modeling.max_tfidf_features to 10, 15 and 30, and the modeling.random_forest.max_features to 0.1, 0.33, 0.5, 0.75, 1.
   mlflow run . \
   -P steps=train_random_forest \
   -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1 -m"

Deploy on new data

   mlflow run https://github.com/mwalmsley/build-ml-pipeline-for-short-term-rental-prices.git -v v1.0.0 -P hydra_options="etl.sample='sample2.csv'"

and with lat/long fix

   mlflow run https://github.com/mwalmsley/build-ml-pipeline-for-short-term-rental-prices.git -v v1.0.1 -P hydra_options="etl.sample='sample2.csv'"
