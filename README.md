# Axie Money

## Breeding Profit Calculator

Calculate the time it takes prior to break even from breeding axies. Currently supports
ABC and ABCD loops. Crypto prices are pulled from known services, or can be
specified by the user.

### Usage 

```python
from decimal import Decimal
from axie_money.calculators import BreedingProfitCalculator, PriceConverter

price_converter=PriceConverter(
	slp_rate=Decimal("0.26"), axs_rate=Decimal("40"), eth_rate=Decimal("2190")
)
calculator = BreedingProfitCalculator(
	price_converter=price_converter,
	price_floor=Decimal("0.2358"),
	price_ceiling=Decimal("0.73"),
)
initial_capital = calculator.calculate_initial_capital(
	parent_prices=[
		Decimal("0.5"),
		Decimal("0.5"),
		Decimal("0.5")
	]
)
breeding_cost = calculator.calculate_cumulative_breeding_cost(
	breed_count=4,
	parent_count=2
)
sale_price = calculator.calculate_sale_price(offspring_sold=2)
profit = calculator.calculate_profit(breeding_cost, sale_price)
roi_generations = calculator.calculate_roi_generations(
	initial_capital, breeding_cost, profit
)
calculator.calculate_roi_days(
	roi_generations=roi_generations
)
```

## Scholarship Profit Calculator

Calculate the time it takes prior to break even from a scholarship.

### Usage

```python
from decimal import Decimal
from axie_money.calculators import ScholarshipProfitCalculator, PriceConverter

price_converter=PriceConverter(
	slp_rate=Decimal("0.26"), axs_rate=Decimal("40"), eth_rate=Decimal("2190")
)
calculator = ScholarshipProfitCalculator(
	price_converter=price_converter,
	min_slp=Decimal("100"),
	max_slp=Decimal("150"),
	percentage=Decimal("0.5")
)
initial_capital = calculator.calculate_initial_capital(
	[Decimal("0.18"), Decimal("0.22"), Decimal("0.169")]
)
days = 30
actual_average = calculator.calculate_actual_average_slp_per_day(
	4000, days
)
calculator.calculate_roi_days(
	initial_capital, actual_average, days
)
```