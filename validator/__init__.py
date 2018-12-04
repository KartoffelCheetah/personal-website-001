def min_length(min_length, t):
    def validate(s):
        if type(s)==t and len(s) >= min_length:
            return s
        raise ValueError(
            "String must be at least %i characters long"
            % min_length)
    return validate

def max_length(max_length, t):
    def validate(s):
        if type(s)==t and len(s) <= max_length:
            return s
        raise ValueError(
            "String cannot be longer than %i characters"
            % max_length)
    return validate

def length(min_length, max_length, t):
    def validate(s):
        if type(s)==t and len(s) >= min_length and len(s) <= max_length:
            return s
        raise ValueError(
            "Length of String must be between %i and %i characters"
            % (min_length, max_length))
    return validate
