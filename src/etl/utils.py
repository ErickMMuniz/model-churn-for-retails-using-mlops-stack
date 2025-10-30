def from_str_to_type(type_name: str):
    """
    Converts a string representation of a type to its actual type.

    Args:
        type_name (str): The name of the type as a string (e.g., 'int', 'float').

    Returns:
        type: The actual Python type or a string for pandas datetime.

    Note: This function is primarily designed for use with `pd.Series` types.
    """
    match type_name:
        case "int":
            return int
        case "float":
            return float
        case "str":
            return str
        case "bool":
            return bool
        case "datetime":
            return "datetime64[ns]"
        case _:
            return "object"
