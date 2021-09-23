from decimal import Decimal
from typing import List

from .constants import AXS_BREEDING_COST, SLP_BREEDING_COST


class PriceConverter(object):
    """Converts ETH, AXS, and SLP price to USD."""

    def __init__(self, eth_rate: Decimal, axs_rate: Decimal, slp_rate: Decimal):
        self.axs_rate = axs_rate
        self.slp_rate = slp_rate
        self.eth_rate = eth_rate

    def axs_to_usd(self, amount: Decimal) -> Decimal:
        """Converts AXS to USD."""
        return self.axs_rate * amount

    def slp_to_usd(self, amount: Decimal) -> Decimal:
        """Converts SLP to USD."""
        return self.slp_rate * amount

    def eth_to_usd(self, amount: Decimal) -> Decimal:
        """Converts ETH to USD."""
        return self.eth_rate * amount


class BreedingProfitCalculator(object):
    """Calculates Axie Infinity breeding profit based on given inputs.

    Supports a scalable amount of parents in a breeding loop, wherein the
    most popular loops include the ABC and ABCD loops. ABC loops produce a single
    batch of offspring per generation, while ABCD loops produce two batches per
    generation.

    :attribute price_floor: Expected floor price of sold parents.
    :attribute price_ceiling: Expected maximum price of offspring.
    """

    def __init__(
        self,
        price_converter: PriceConverter,
        price_floor: Decimal,
        price_ceiling: Decimal,
    ):
        self.price_converter = price_converter
        self.price_floor = price_floor
        self.price_ceiling = price_ceiling

    @property
    def offspring_average_price(self) -> Decimal:
        """Estimated average price of sold axies."""
        return Decimal((self.price_floor + self.price_ceiling) / 2)

    def calculate_initial_capital(self, parent_prices: List[Decimal]) -> Decimal:
        """Convert initial capital ETH price to USD.

        :param parent_prices: ETH denominated acquisition price of all parents.
        :returns: Initial investment in USD.
        """
        return self.price_converter.eth_to_usd(sum(parent_prices))

    def calculate_breeding_cost(self, parent_breed_counts: List[int]) -> Decimal:
        """Calculate the breeding cost given all of the parents' current breed counts.

        :param parent_breed_counts: A list of all of the parents' current breed counts.
        :returns: The calculated breeding cost.
        """
        prices = [SLP_BREEDING_COST[i] for i in parent_breed_counts]
        return (
            self.price_converter.slp_to_usd(sum(prices))
            + self.price_converter.axs_to_usd(
                AXS_BREEDING_COST * len(parent_breed_counts)
            )
        ).quantize(Decimal("0.01"))

    def calculate_cumulative_breeding_cost(
        self, breed_count: int, parent_count: int, slp_farmed: Decimal = 0
    ) -> Decimal:
        """Calculates the cumulative breeding cost up to the given breed count.

        This assumes that both parents have the same breed count. This also
        assumes that the SLP and AXS costs are covered via capital. If farmed
        SLP is used, specify the amount in ``slp_farmed``.

        :param breed_count: The target breed count for both parents.
        :param parent_count: The number of parents used for breeding a generation.
        :param slp_farmed: Amount of farmed SLP to be used for paying breeding costs.
        :returns: The cumulative breeding cost.
        """
        cumulative_breeding_cost = 0

        for i in range(breed_count):
            cumulative_breeding_cost += self.calculate_breeding_cost([i] * parent_count)

        cumulative_breeding_cost -= slp_farmed

        return cumulative_breeding_cost

    def calculate_sale_price(self, offspring_sold: int) -> Decimal:
        """Calculates the price of sold axies.

        The calculation is based on the estimated average of floor price and
        ceiling price, minus marketplace fees.

        :param offspring_sold: Amount of axies sold.
        :returns: Calculated sale price in USD.
        """
        marketplace_fee = Decimal(1 - Decimal(0.0425))
        sale_price = self.offspring_average_price * offspring_sold * marketplace_fee

        return self.price_converter.eth_to_usd(sale_price).quantize(Decimal("0.01"))

    def calculate_profit(
        self,
        breeding_cost: Decimal,
        sale_price: Decimal,
        parents_sold: int = 0,
    ) -> Decimal:
        """Calculates the profit after breeding costs.

        :param breeding_cost: Amount spent to pay for breeding fees.
        :param sale_price: Amount earned from selling offspring.
        :param parents_sold: Amount of parents sold.
        :returns: Profit after fees, breeding costs, and parents sold if specified.
        """
        return (
            self.price_converter.eth_to_usd(self.price_floor * parents_sold)
            + sale_price
            - breeding_cost
        ).quantize(Decimal("0.01"))

    def calculate_roi_generations(
        self, initial_capital: Decimal, breeding_cost: Decimal, profit: Decimal
    ) -> Decimal:
        """Calculates the required generations before breaking even.

        :param initial_capital: Amount spent to acquire three parents.
        :param breeding_cost: Amount spent to pay for breeding fees.
        :param profit: Profit after fees, breeding costs, and parents sold if specified.
        :returns: Required amount of breeding generations with the same breed count
            to break even.
        """
        return ((initial_capital + breeding_cost) / profit).quantize(Decimal("0.01"))

    def calculate_roi_days(
        self,
        roi_generations: Decimal = 0,
        initial_capital: Decimal = 0,
        breeding_cost: Decimal = 0,
        profit: Decimal = 0,
    ):
        """Calculates the number of days before breaking even.

        Specify ``roi_generations`` if known. Otherwise, specify the ``initial_capital``,
        ``breeding_cost``, and ``profit``. This method will calculate the same result
        using either of the paramater groups.

        :param roi_generations: Required amount of breeding generations with the same
            breed count to break even.
        :param initial_capital: Amount spent to acquire three parents.
        :param breeding_cost: Amount spent to pay for breeding fees.
        :param profit: Profit after fees, breeding costs, and parents sold if specified.
        :returns: The number of days it will take before breaking even.
        """
        days_to_generate = 5
        return (
            (roi_generations * days_to_generate).quantize(Decimal("0.01"))
            if roi_generations > 0
            else (
                self.calculate_roi_generations(initial_capital, breeding_cost, profit)
                * days_to_generate
            ).quantize(Decimal("0.01"))
        )


class ScholarshipProfitCalculator(object):
    """Calculates Axie Infinity scholarship profit based on given inputs.

    Calculates the rate of return and breakeven of a given scholarship account.
    A scholar is expected to earn a ``min_slp`` amount of SLP per day. ``max_slp``
    is used to calculate for the scholar's average gain per day.

    :attribute min_slp: The required minimum SLP a scholar has to farm per day.
    :attribute max_slp: Theoretical maximum SLP a scholar can farm per day,
        ideally based on past performance and win rate.
    :attribute percentage: Percentage of SLP that the manager earns from the
        scholarship. Should be a number between 0-1.
    """

    def __init__(
        self,
        price_converter: PriceConverter,
        min_slp: Decimal,
        max_slp: Decimal,
        percentage: Decimal,
    ):
        self.price_converter = price_converter
        self.min_slp = min_slp
        self.max_slp = max_slp
        self.percentage = percentage

    @property
    def potential_average_slp(self) -> Decimal:
        """Estimated daily average SLP earnings."""
        return Decimal((self.min_slp + self.max_slp) / 2)

    def calculate_initial_capital(self, team_price: List[Decimal]) -> Decimal:
        """Convert initial capital ETH price to USD.

        :param team_price: ETH denominated acquisition price of the scholar's
            team of axies.
        :returns: Initial investment in USD.
        """
        return self.price_converter.eth_to_usd(sum(team_price)).quantize(
            Decimal("0.01")
        )

    def calculate_actual_average_slp_per_day(
        self, current_slp: Decimal, days: int
    ) -> Decimal:
        """Calculates the actual average SLP based on the scholar's performance.

        :param current_slp: Current unclaimable SLP the scholar has farmed.
        :param days: Number of days the scholar farmed ``current_slp``.
        :returns: Average SLP the scholar farmed per day based on actual
            performance.
        """
        return Decimal(current_slp / days).quantize(Decimal("0.01"))

    def calculate_roi_periods(
        self, initial_capital: Decimal, average_slp: Decimal, days: int
    ) -> Decimal:
        """Calculates the number of periods before breaking even.

        :param initial_capital: USD denominated acquisition price of the
            scholar's team of axies.
        :param average_slp: Actual or potential average SLP the scholar can
            farm per day.
        :param days: Number of days in a specified period, ie. 30 if you
            want to calculate the ROI based on monthly returns.
        :returns: The number of periods it will take before breaking even.
        """
        return Decimal(
            initial_capital
            / (self.price_converter.slp_to_usd(average_slp) * self.percentage * days)
        ).quantize(Decimal("0.01"))
