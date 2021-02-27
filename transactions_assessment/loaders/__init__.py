from transactions_assessment.exceptions import NonExistError, WrongExtError, LineFormatError
from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum
import logging
import json


class Constants(Enum):
    FILE_EXT = '.txt'
    FIELDS = ['accountNumber', 'customerId', 'creditLimit', 'availableMoney', 'transactionDateTime',
              'transactionAmount','merchantName', 'acqCountry', 'merchantCountryCode', 'posEntryMode',
              'posConditionCode', 'merchantCategoryCode', 'currentExpDate', 'accountOpenDate',
              'dateOfLastAddressChange', 'cardCVV', 'enteredCVV', 'cardLast4Digits', 'transactionType', 'echoBuffer',
              'currentBalance', 'merchantCity', 'merchantState', 'merchantZip', 'cardPresent', 'posOnPremises',
              'recurringAuthInd', 'expirationDateKeyInMatch', 'isFraud']


class DataLoader(ABC):
    def __init__(self, data_file: str):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f'{__name__} entered')
        self.data_file = data_file
        self.validate_file()
        self.validate_ext()

    def validate_line(self, line: str) -> dict:
        """
        validate a line of the txt file,
        check if the line is formatted correctly,
        and if the expected keys exists

        PARAMS
        ---------
        line: str
            a single line to be processed

        RETURNS
        ----------
        validated_dict: dict
            an evaluated dictionary
        """
        try:
            record = json.loads(line)
            if Constants.FIELDS.value != list(record.keys()):
                raise LineFormatError
        except json.decoder.JSONDecodeError:
            raise LineFormatError
        return record

    def read_lines(self) -> list:
        """
        Read each line of file, if line is
        valid, append it to a list, otherwise
        log warning and continue

        RETURNS
        -----------
        data_bundle: list
            list of dictionaries, where each
            dictionary represents a line from
            the file
        """
        data_bundle = []
        counter = 0
        for line in open(self.data_file):
            counter += 1
            try:
                record: dict = self.validate_line(line)
                data_bundle.append(record)
                self.logger.debug('Adding line to bundle')
            except LineFormatError:
                self.logger.warning(f'Line number {counter} is malfomed.. not adding to bundle')
        self.logger.info(f'{data_bundle.__len__()} lines of {counter} successfully read.')
        return data_bundle

    def validate_file(self):
        """
        validate the data file to
        ensure the file exists. Raise
        NonExistError if it does not
        """
        file_path = Path.absolute(Path(self.data_file))
        file_exists = file_path.exists()
        if not file_exists:
            self.logger.error(f'The file you have supplied does not seem to exist: {file_path}')
            raise NonExistError

    def validate_ext(self):
        """
        make sure that the extension of the file
        is .txt.Raise WrongExtError if it does not
        """
        file_name = Path(self.data_file)
        if file_name.suffix != Constants.FILE_EXT.value:
            self.logger.error(f'The file you have supplied ({file_name}) does not have the expected .txt ext')
            raise WrongExtError

    @abstractmethod
    def preprocess_data(self):
        pass

    @abstractmethod
    def resample(self):
        pass
