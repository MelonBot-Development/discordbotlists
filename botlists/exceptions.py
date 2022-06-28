class BotListException(Exception):
    """
    Base exception class for all errors raised.  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class RequestFailureException(BotListException):
    """
    Exception raised when API requests fail.
    """
    def __init__(self, status: int, response: str):
        super().__init__("{}: {}".format(status, response))
        
class RateLimitException(BotListException):
    """
    Exception raised when API endpoint is being rate limited.
    """
    def __init__(self, json=None):
        super().__init__(
            "The request to the API endpoint was ratelimited." +
            ("\nPlease re-attempt this request after {:,} seconds.".format(json['retry_after'])
            if json and "retry_after" in json else ""
        ))
        
class EmptyResponseException(BotListException):
    """
    Exception raised when API endpoint sends an empty response.
    """
    def __init__(self):
        super().__init__(
            "No response was received from the API."
        )
        
class NotFoundException(BotListException):
    """
    Exception raised if the entity is not found.
    """
    def __init__(self):
        super().__init__(
            "The requested entity was not found."
        )
        