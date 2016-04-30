# -*- coding: utf-8 -*-

from . import ExceptionWithFormat


class IntervalException(ExceptionWithFormat):
    """
    set interval exception.
    """


class AlarmException(ExceptionWithFormat):
    """
    Alarm exception.
    """


class PrinterException(ExceptionWithFormat):
    """
    Log printer exception.
    """


class WorkerNotFound(ExceptionWithFormat):
    """
    Worker not found.
    """


class CallingWorkerError(ExceptionWithFormat):
    """
    Error occurred during running worker.
    """


class EmptyCrawlerResponse(ExceptionWithFormat):
    """
    Scrapper responded with empty object.
    """


class CallingValidationError(ExceptionWithFormat):
    """
    Error occurred during running validation.
    """


class ValidationErrorResponse(ExceptionWithFormat):
    """
    Scrapper responded with not valid json.
    """


class SaveDataToDatabaseError(ExceptionWithFormat):
    """
    Error saving data to db
    """


class ConnectToDatabaseError(ExceptionWithFormat):
    """
    Scrapper  responded with not valid json.
    """
