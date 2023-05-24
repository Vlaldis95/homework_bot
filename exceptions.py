class StatusError(Exception):
    """Исключение, вызываемое при неправильном статусе запроса."""

    pass


class APIError(Exception):
    """Исключение, вызываемое при сбоях в работе запросов к API."""

    pass
