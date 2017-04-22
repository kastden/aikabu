#!/usr/bin/env python3


class AikabuException(Exception):
    pass


class SessionTimeoutException(AikabuException):
    pass


class MaintenanceWindowException(AikabuException):
    pass


class InvalidResponseCodeException(AikabuException):
    pass
