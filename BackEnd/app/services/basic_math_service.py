from app.schemas.bassic_math import SumRequest, SumResponse


def sum_math(a: float, b: float) -> float:
    return SumResponse(result=a + b).result

