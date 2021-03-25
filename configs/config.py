class TinyUrl:
    NAME = "tinyurl"
    API_URL = "http://tinyurl.com/api-create.php"
    CONTENT_TYPE = "application/json"


class BitLy:
    NAME = 'bitly'
    API_URL = "https://api-ssl.bitly.com/v4/shorten"
    TOKEN = "Bearer 8ce4e9f7e73b0da7303a325b64bbb1c540e16a73"
    CONTENT_TYPE = "application/json"


class Messages:
    WRONG_PROVIDER_MSG = "Not supported Provider. Choose between bit.ly and tinyurl"
    WRONG_PARAMETER_MSG = "Invalid parameters. Provide a <url> and optionally a <provider> parameter."
    WRONG_URL_MSG = "Invalid Url. Please provide a valid url"
    SUCCESS_MSG = "Successfully Shortened the URL"


class GeneralStrs:
    UNKNOWN = "unknown"
    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-Type"