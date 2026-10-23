"""Safe, user-presentable extraction errors without provider response data."""


class ExtractionError(RuntimeError):
    """A categorized extraction failure with a non-sensitive display message."""

    def __init__(self, code: str, user_message: str):
        super().__init__(user_message)
        self.code = code
        self.user_message = user_message


class ImageValidationError(ExtractionError):
    """Invalid, unsupported, or oversized image input."""


class ProviderConfigurationError(ExtractionError):
    """Required provider configuration is unavailable or invalid."""
