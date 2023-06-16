import pandas as pd

if __name__ == '__main__':

    df = pd.read_csv('/home/walml/repos/build-ml-pipeline-for-short-term-rental-prices/src/basic_cleaning/clean_sample.csv')

    # # Drop outliers
    # idx = df['price'].between(10, 350)
    # df = df[idx].copy()
    # # Convert last_review to datetime
    # df['last_review'] = pd.to_datetime(df['last_review'])

    print(df['price'].min(), df['price'].max())

    # print(df['price'])
