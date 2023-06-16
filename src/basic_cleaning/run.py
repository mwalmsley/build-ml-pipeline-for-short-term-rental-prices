#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import os
import argparse
import logging
import wandb

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    input_filename = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(input_filename)

    # drop rows with mis-aligned header
    idx = df['price']

    # Drop outliers
    logging.info(f'Dropping price outliers outside {args.min_price} and {args.max_price}')
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    output_filename = "clean_sample.csv"
    df.to_csv(output_filename, index=False)

    output_artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    output_artifact.add_file(output_filename)

    logger.info("Logging artifact")
    run.log_artifact(output_artifact)

    # tmp directory so not needed
    # os.remove(input_filename)
    # os.remove(output_filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help='wandb artifact of data to be cleaned',
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help='wandb artifact of cleaned data',
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='type of output data e.g. csv',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='Housing prices with minor quality fixes',
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help='Remove houses with prices below min_price',
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help='Remove houses with prices above max_price',
        required=True
    )


    args = parser.parse_args()

    go(args)
