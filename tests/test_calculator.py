from decimal import Decimal

from axie_breeding_calculator.calculators import ROICalculator


class TestROICalculator(object):
    calculator = ROICalculator(
        slp_rate=Decimal("0.26"),
        axs_rate=Decimal("40"),
        eth_rate=Decimal("2190"),
        price_floor=Decimal("0.2358"),
        price_ceiling=Decimal("0.73"),
    )

    def test_offspring_average_price(self):
        assert self.calculator.offspring_average_price == Decimal("0.4829")

    def test_calculate_sale_price(self):
        assert self.calculator.calculate_sale_price(3) == Decimal("3037.82")

    def test_calculate_sale_price(self):
        assert self.calculator.calculate_sale_price(3) == Decimal("3037.82")

    def test_axs_to_usd(self):
        assert self.calculator.axs_to_usd(Decimal("4.11")) == Decimal("164.40")

    def test_slp_to_usd(self):
        assert self.calculator.slp_to_usd(Decimal("4500")) == Decimal("1170")

    def test_eth_to_usd(self):
        assert self.calculator.eth_to_usd(Decimal("6.69")) == Decimal("14651.1")


class TestROICalculatorABCLoop(object):
    calculator = ROICalculator(
        slp_rate=Decimal("0.26"),
        axs_rate=Decimal("40"),
        eth_rate=Decimal("2190"),
        price_floor=Decimal("0.2358"),
        price_ceiling=Decimal("0.73"),
    )

    def test_calculate_initial_capital(self):
        assert self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        ) == Decimal("3285")

    def test_caclulate_cumulative_breeding_cost(self):
        assert self.calculator.calculate_cumulative_breeding_cost(4, 2) == Decimal(
            "1498"
        )

    def test_caclulate_cumulative_breeding_cost_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)

        assert self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        ) == Decimal("1264")

    def test_calculate_profit(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1539.82"
        )

    def test_calculate_profit_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1773.82"
        )

    def test_calculate_profit_parents_sold(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        ) == Decimal("2572.62")

    def test_calculate_profit_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        ) == Decimal("2806.62")

    def test_calculate_roi_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("3.11")

    def test_calculate_roi_generations_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("2.56")

    def test_calculate_roi_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.86")

    def test_calculate_roi_generations_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("1.62")

    def test_calculate_roi_days(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("15.55")

    def test_calculate_roi_days_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("12.80")

    def test_calculate_roi_days_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("9.30")

    def test_calculate_roi_days_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 2, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )
        roi_generations = self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        )

        assert self.calculator.calculate_roi_days(
            roi_generations=roi_generations
        ) == Decimal("8.10")

    def test_calculate_roi_days_unknown_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("15.55")

    def test_calculate_roi_days_unknown_generations_parents_sold(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 2)
        sale_price = self.calculator.calculate_sale_price(3)
        profit = self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=2
        )

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("9.30")


class TestROICalculatorABCDLoop(object):
    calculator = ROICalculator(
        slp_rate=Decimal("0.26"),
        axs_rate=Decimal("40"),
        eth_rate=Decimal("2190"),
        price_floor=Decimal("0.2358"),
        price_ceiling=Decimal("0.73"),
    )

    def test_calculate_initial_capital(self):
        assert self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        ) == Decimal("4380")

    def test_caclulate_cumulative_breeding_cost(self):
        assert self.calculator.calculate_cumulative_breeding_cost(4, 4) == Decimal(
            "2996"
        )

    def test_caclulate_cumulative_breeding_cost_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)

        assert self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        ) == Decimal("2762")

    def test_calculate_profit(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1054.42"
        )

    def test_calculate_profit_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(breeding_cost, sale_price) == Decimal(
            "1288.42"
        )

    def test_calculate_profit_parents_sold(self):
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        ) == Decimal("3120.03")

    def test_calculate_profit_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(
            4, 4, slp_farmed
        )
        sale_price = self.calculator.calculate_sale_price(4)

        assert self.calculator.calculate_profit(
            breeding_cost, sale_price, parents_sold=4
        ) == Decimal("3354.03")

    def test_calculate_roi_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_generations(
            initial_capital, breeding_cost, profit
        ) == Decimal("7.00")

    def test_calculate_roi_generations_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
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
        ) == Decimal("5.54")

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
        ) == Decimal("2.36")

    def test_calculate_roi_generations_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
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
        ) == Decimal("2.13")

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
        ) == Decimal("35")

    def test_calculate_roi_days_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
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
        ) == Decimal("27.70")

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
        ) == Decimal("11.80")

    def test_calculate_roi_days_parents_sold_slp_farmed(self):
        slp_farmed = self.calculator.slp_to_usd(900)
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
        ) == Decimal("10.65")

    def test_calculate_roi_days_unknown_generations(self):
        initial_capital = self.calculator.calculate_initial_capital(
            [Decimal("0.5"), Decimal("0.5"), Decimal("0.5"), Decimal("0.5")]
        )
        breeding_cost = self.calculator.calculate_cumulative_breeding_cost(4, 4)
        sale_price = self.calculator.calculate_sale_price(4)
        profit = self.calculator.calculate_profit(breeding_cost, sale_price)

        assert self.calculator.calculate_roi_days(
            initial_capital=initial_capital, breeding_cost=breeding_cost, profit=profit
        ) == Decimal("35.00")

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
        ) == Decimal("11.80")