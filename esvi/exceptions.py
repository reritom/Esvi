class DoesNotExist(Exception):
    """
    Raised when a model doesn't exist in the database
    """
    pass

class InstanceDeletedException(Exception):
    """
    Raised if ModelInstance.save() is called on a deleted instance
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

class PrimaryKeyModificationException(Exception):
    """
    Raised if you try and change the primary key value in a model instance
    """
    pass

class UnsupportedFieldForPrimaryKey(Exception):
    """
    Raised if a field type which can't be a primary key is set as a primary key
    """
    pass

class UnsupportedQueryAction(Exception):
    """
    Raised if the query action value isn't in the supported list
    """
    pass

class InvalidForeignKeyDefinition(Exception):
    """
    Raised if the value passed in a model definition for the foregin key isn't another model definition class
    """
    pass
