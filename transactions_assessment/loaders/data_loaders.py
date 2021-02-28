from transactions_assessment.loaders import DataLoader
from datetime import datetime
import pandas as pd


class TransactionLoader(DataLoader):
    def preprocess_data(self) -> pd.DataFrame:
        """
        load in data from text file and convert to
        a pandas dataframe. Turn the variable transactionDateTime
        into a datetime type.
        RETURNS
        ---------
        df: pd.DataFrame
            preprocessed data frame
        """
        loaded_data: list = self.read_lines()
        df = pd.DataFrame(loaded_data)
        df['transactionDateTime'] = df.transactionDateTime.apply(
            lambda k: datetime.strptime(k.replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
        df['multi_swipe'] = self.detect_multi_swipe(300, df)
        return df

    def detect_multi_swipe(self, time_window: int, df: pd.DataFrame) -> list:
        """
        Decide if any give transaction is
        part of a series of multi-swipes by
        comparing the times of transaction
        DateTime, and the amount of purchase.

        PARAMS
        --------
        values: pd.Series
            datetime variable series that has
            been sorted

        time_window: int
            time in seconds to use as the cut-off
            to decide if a transaction is multi-swipe

        RETURNS
        --------
        multi_swipe_col: list
            a list of 0s and 1s representing
            whether a transaction is multi-swipe (1)
            or not (0)
        """
        df.sort_values(by=['transactionDateTime'], inplace=True)
        multi_swipe_col = [0]
        for idx, dt in enumerate(df.transactionDateTime):
            if idx == 0:
                continue
            diff = abs(df.transactionDateTime[idx] - df.transactionDateTime[idx - 1]).total_seconds()
            if diff < time_window and (df.transactionAmount[idx] == df.transactionAmount[idx - 1]) and (
                    df.accountNumber[idx - 1] == df.accountNumber[idx]) and (
                    df.transactionType[idx].lower() == 'purchase'):
                multi_swipe = 1
            else:
                multi_swipe = 0
            multi_swipe_col.append(multi_swipe)
        return multi_swipe_col

    def get_sample(self):
        pass
