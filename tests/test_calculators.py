from decimal import Decimal

from axie_money.calculators import (
    BreedingProfitCalculator,
    PriceConverter,
    ScholarshipProfitCalculator,
)


class TestPriceConverter(object):
    converter = PriceConverter(
        slp_rate=Decimal("0.08"), axs_rate=Decimal("67"), eth_rate=Decimal("3140")
    )

    def test_axs_to_usd(self):
        assert self.converter.axs_to_usd(Decimal("4.11")) == Decimal("275.37")

    def test_slp_to_usd(self):
        assert self.converter.slp_to_usd(Decimal("4500")) == Decimal("360")

    def test_eth_to_usd(self):
        assert self.converter.eth_to_usd(Decimal("6.69")) == Decimal("21006.6")


class TestBreedingProfitCalculator(object):
    calculator = BreedingProfitCalculator(
        price_converter=PriceConverter(
            slp_rate=Decimal("0.08"), axs_rate=Decimal("67"), eth_rate=Decimal("3140")
        ),
        price_floor=Decimal("0.173"),
        price_ceiling=Decimal("0.69"),
    )

    def test_offspring_average_price(self):
        assert self.calculator.offspring_average_price == Decimal("0.4315")

    def test_calculate_sale_price(self):
        assert self.calculator.calculate_sale_price(2) == Decimal("2594.65")

    def test_calculate_breeding_cost(self):
        assert self.calculator.calculate_breeding_cost([0, 0]) == Decimal("115")


class TestBreedingProfitCalculatorABCLoop(object):
    calculator = BreedingProfitCalculator(
        price_converter=PriceConverter(
            slp_rate=Decimal("0.08"), axs_rate=Decimal("67"), eth_rate=Decimal("3140")
        ),
        price_floor=Decimal("0.173"),
        price_ceiling=Decimal("0.69"),
    )

    def test_calculate_initial_capital(self):
        assert self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        ) == Decimal("4710")

    def test_calculate_cumulative_breeding_cost(self):
        assert self.calculator.calculate_cumulative_breeding_cost(4, 2) == Decimal(
            "700"
        )

    def test_calculate_cumulative_breeding_cost_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)

        assert self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        ) == Decimal("628")

    def test_calculate_profit(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1894.65"
        )

    def test_calculate_profit_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1966.65"
        )

    def test_calculate_profit_parents_sold(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        ) == Decimal("2981.09")

    def test_calculate_profit_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        ) == Decimal("3053.09")

    def test_calculate_roi_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("2.86")

    def test_calculate_roi_generations_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("2.71")

    def test_calculate_roi_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.81")

    def test_calculate_roi_generations_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.75")

    def test_calculate_roi_days(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("14.3")

    def test_calculate_roi_days_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("13.55")

    def test_calculate_roi_days_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("9.05")

    def test_calculate_roi_days_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("8.75")

    def test_calculate_roi_days_unknown_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("14.3")

    def test_calculate_roi_days_unknown_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(2)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("9.05")


class TestBreedingProfitCalculatorABCDLoop(object):
    calculator = BreedingProfitCalculator(
        price_converter=PriceConverter(
            slp_rate=Decimal("0.08"), axs_rate=Decimal("67"), eth_rate=Decimal("3140")
        ),
        price_floor=Decimal("0.173"),
        price_ceiling=Decimal("0.69"),
    )

    def test_calculate_initial_capital(self):
        assert self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        ) == Decimal("6280")

    def test_calculate_cumulative_breeding_cost(self):
        assert self.calculator.calculate_cumulative_breeding_cost(4, 4) == Decimal(
            "1400"
        )

    def test_calculate_cumulative_breeding_cost_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)

        assert self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        ) == Decimal("1360")

    def test_calculate_profit(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "3789.31"
        )

    def test_calculate_profit_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "3829.31"
        )

    def test_calculate_profit_parents_sold(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        ) == Decimal("5962.19")

    def test_calculate_profit_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        ) == Decimal("6002.19")

    def test_calculate_roi_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("2.03")

    def test_calculate_roi_generations_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("2.0")

    def test_calculate_roi_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.29")

    def test_calculate_roi_generations_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.27")

    def test_calculate_roi_days(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("10.15")

    def test_calculate_roi_days_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("10")

    def test_calculate_roi_days_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("6.45")

    def test_calculate_roi_days_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.price_converter.slp_to_usd(500)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("6.35")

    def test_calculate_roi_days_unknown_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("10.15")

    def test_calculate_roi_days_unknown_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        )

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("6.45")


class TestScholarshipProfitCalculator(object):
    calculator = ScholarshipProfitCalculator(
        price_converter=PriceConverter(
            slp_rate=Decimal("0.08"), axs_rate=Decimal("67"), eth_rate=Decimal("3140")
        ),
        min_slp=Decimal("100"),
        max_slp=Decimal("150"),
        percentage=Decimal("0.5"),
    )

    def test_potential_average_slp(self):
        assert self.calculator.potential_average_slp == Decimal("125")

    def test_calculate_initial_capital(self):
        assert self.calculator.calculate_initial_capital(
            [Decimal("0.18"), Decimal("0.22"), Decimal("0.169")]
        ) == Decimal("1786.66")

    def test_calculate_actual_average_slp_per_day(self):
        assert self.calculator.calculate_actual_average_slp_per_day(
            current_slp=2000, days=15
        ) == Decimal("133.33")

    def test_calculate_roi_periods_potential(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.18"), Decimal("0.22"), Decimal("0.169")]
        )
        potential_average = self.calculator.potential_average_slp
        days = 30

        assert self.calculator.calculate_roi_periods(
            initial_capital, potential_average, days
        ) == Decimal("11.91")

    def test_calculate_roi_periods_actual(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.18"), Decimal("0.22"), Decimal("0.169")]
        )
        days = 30
        actual_average = self.calculator.calculate_actual_average_slp_per_day(
            6000, days
        )

        assert self.calculator.calculate_roi_periods(
            initial_capital, actual_average, days
        ) == Decimal("7.44")
