from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner


class TestDequeFilling:

    # TODO: create a test with a mocked version of the API to reduce test runtime
    def test_deque_filling(self):
        result = MetricsCalculationRunner._fetch_interval_of_blocks(start=0, end=51)
        assert list(map(lambda x: x["height"], result)) == list([x for x in range(0, 52)])
