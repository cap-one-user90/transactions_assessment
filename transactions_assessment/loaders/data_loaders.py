from transactions_assessment.loaders import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
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
        df['multi_swipe'] = detect_multi_swipe(300, df)
        return df


class ModelDataLoader(DataLoader):
    def preprocess_data(self) -> tuple:
        """
        Preprocess data for fitting with
        a model

        RETURNS
        --------
        x_train: pd.DataFrame
            training set of predictors
        y_train: pd.Series
            training set of responses
        x_test: pd.DataFrame
            testing set of predictors
        y_test: pd.Series
            test set of responses
        """
        loaded_data: list = self.read_lines()
        df = pd.DataFrame(loaded_data)
        df['transactionDateTime'] = df.transactionDateTime.apply(
            lambda k: datetime.strptime(k.replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
        df = df.sort_values('transactionDateTime').reset_index()
        df['multi_swipe'] = detect_multi_swipe(300, df)
        labels = df.isFraud.astype(int)
        df.drop('isFraud', axis=1, inplace=True)
        df = self.encode_cats(df)
        df.drop(['echoBuffer', 'merchantCity', 'merchantState', 'merchantZip', 'posOnPremises', 'recurringAuthInd',
                 'transactionDateTime'], axis=1, inplace=True)
        x_train, y_train, x_test, y_test = train_test_split(df, labels, test_size=0.2)

        return x_train, y_train, x_test, y_test

    def encode_cats(self, df: pd.DataFrame):
        """
        encode categorical variables
        """
        label_encoder = LabelEncoder()
        cat_cols = ['accountNumber', 'customerId', 'merchantName', 'merchantCategoryCode',
                    'currentExpDate', 'accountOpenDate', 'dateOfLastAddressChange', 'cardCVV', 'enteredCVV',
                    'cardLast4Digits']
        for col in cat_cols:
            df[col] = label_encoder.fit_transform(df[col])
        processed_df = pd.get_dummies(df, columns=['merchantCountryCode', 'posEntryMode', 'posConditionCode',
                                                   'transactionType', 'acqCountry'], drop_first=True)
        return processed_df


def detect_multi_swipe(time_window: int, df: pd.DataFrame) -> list:
    """
    Decide if any give transaction is
    part of a series of multi-swipes by
    comparing the times of transaction
    DateTime, and the amount of purchase.

    PARAMS
    --------
    df: pd.DataFrame
        unprocessed pandas dataframe with
        column transactionDate

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
