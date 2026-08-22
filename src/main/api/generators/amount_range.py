from dataclasses import dataclass
import random

AMOUNT_STEP = 100

@dataclass(frozen=True)
class AmountRange:
    min: int
    max: int

    def random_value(self):
        return random.randrange(self.min, self.max + AMOUNT_STEP, AMOUNT_STEP)

    def capped_at(self, limit):
        return AmountRange(self.min, min(self.max, int(limit)))


DEPOSIT_AMOUNT_RANGE = AmountRange(1000, 9000)
TRANSFER_AMOUNT_RANGE = AmountRange(500, 10000)
CREDIT_AMOUNT_RANGE = AmountRange(5000, 15000)
