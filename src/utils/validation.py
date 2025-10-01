def validate_order_inputs(symbol: str, side: str, quantity: float):
    """
    Performs basic validation on common order parameters.
    Raises ValueError if validation fails.
    """
    if not symbol or len(symbol) < 6:
        raise ValueError("Invalid or missing symbol. It should be like 'BTCUSDT'.")
    
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Invalid side. Must be 'BUY' or 'SELL'.")
        
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError("Invalid quantity. It must be a positive number.")
        
    return True