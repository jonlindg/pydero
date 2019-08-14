
def to_dero(value):
    """Convert number in smallest unit to number in dero"""
    return value/10**12

def from_dero(value_in_dero):
    """Convert number in dero to smallest unit"""
    return int(value_in_dero*10**12)
