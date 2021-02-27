from transactions_assessment.loaders import DataLoader
import pandas as pd


class TransactionLoader(DataLoader):
    def preprocess_data(self):
        loaded_data = self.read_lines()
        df = pd.DataFrame(loaded_data)
        return df

    def get_sample(self):
        pass
