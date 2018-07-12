class DoesNotExist(Exception):
    """
    Raised when a model doesn't exist in the database
    """
    pass

class UnspecifiedConnection(Exception):
    """
    Raised by the query executor if a connection object hasn't be globalised
    """
    pass

class UnsupportedAdapterField(Exception):
    """
    Raised in an adapter is passed a model field type which it doesn't support
    """

class UnsupportedAdapter(Exception):
    """
    Raised if the database in the connection doesn't have an adapter to support it
    """
    pass

class FieldValidationException(Exception):
    """
    Raised if a value passed as a field parameter fails the validation
    """
    pass

class InvalidFieldException(Exception):
    """
    Raised if you try and set or get a field that doesn't exist from a model instance
    """
    pass
