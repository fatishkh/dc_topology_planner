"""
Input validation utilities.

This module provides functions to validate user inputs before processing.
"""

from typing import Optional


def validate_racks(racks: int) -> tuple[bool, Optional[str]]:
    """
    Validate number of racks.
    
    Args:
        racks: Number of racks to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if racks is None:
        return False, "Number of racks is required"
    
    try:
        racks_int = int(racks)
        if racks_int <= 0:
            return False, "Number of racks must be positive"
        if racks_int > 10000:
            return False, "Number of racks seems unreasonably high (> 10,000)"
        return True, None
    except (ValueError, TypeError):
        return False, "Number of racks must be a valid integer"


def validate_servers(servers: int) -> tuple[bool, Optional[str]]:
    """
    Validate number of servers.
    
    Args:
        servers: Number of servers to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if servers is None:
        return False, "Number of servers is required"
    
    try:
        servers_int = int(servers)
        if servers_int <= 0:
            return False, "Number of servers must be positive"
        if servers_int > 1000000:
            return False, "Number of servers seems unreasonably high (> 1,000,000)"
        return True, None
    except (ValueError, TypeError):
        return False, "Number of servers must be a valid integer"


def validate_budget(budget: float) -> tuple[bool, Optional[str]]:
    """
    Validate budget amount.
    
    Args:
        budget: Budget in USD to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if budget is None:
        return False, "Budget is required"
    
    try:
        budget_float = float(budget)
        if budget_float < 0:
            return False, "Budget cannot be negative"
        if budget_float > 1000000000:  # 1 billion USD
            return False, "Budget seems unreasonably high (> $1B)"
        return True, None
    except (ValueError, TypeError):
        return False, "Budget must be a valid number"


def validate_power(power: float) -> tuple[bool, Optional[str]]:
    """
    Validate power limit.
    
    Args:
        power: Power limit in kW to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if power is None:
        return False, "Power limit is required"
    
    try:
        power_float = float(power)
        if power_float <= 0:
            return False, "Power limit must be positive"
        if power_float > 100000:  # 100 MW
            return False, "Power limit seems unreasonably high (> 100 MW)"
        return True, None
    except (ValueError, TypeError):
        return False, "Power limit must be a valid number"


def validate_all_inputs(racks: int, servers: int, budget: float, power: float) -> tuple[bool, Optional[str]]:
    """
    Validate all inputs at once.
    
    Args:
        racks: Number of racks
        servers: Number of servers
        budget: Budget in USD
        power: Power limit in kW
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validations = [
        validate_racks(racks),
        validate_servers(servers),
        validate_budget(budget),
        validate_power(power)
    ]
    
    for is_valid, error_msg in validations:
        if not is_valid:
            return False, error_msg
    
    return True, None
