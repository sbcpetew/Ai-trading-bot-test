import numpy as np
import pandas as pd


def generate_dummy_data(num_bars: int = 1000) -> pd.DataFrame:
    """Generate dummy OHLCV data for testing."""
    rng = np.random.default_rng()
    prices = np.cumsum(rng.normal(0, 1, size=num_bars)) + 100
    df = pd.DataFrame(
        {
            "open": prices,
            "high": prices + rng.uniform(0, 1, size=num_bars),
            "low": prices - rng.uniform(0, 1, size=num_bars),
            "close": prices + rng.normal(0, 0.5, size=num_bars),
            "volume": rng.integers(1, 1000, size=num_bars),
        }
    )
    return df


if __name__ == "__main__":
    df = generate_dummy_data()
    print(df.head())
