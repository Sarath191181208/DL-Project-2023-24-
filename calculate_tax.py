def tax_india_2019(income: float) -> float:
    if income < 2_50_000:
        return 0
    elif income < 5_00_000:
        return income * 0.05
    elif income < 10_00_000:
        return income * 0.2
    
    return income * 0.3