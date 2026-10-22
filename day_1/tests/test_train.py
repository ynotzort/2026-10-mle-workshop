
import tempfile
from datetime import date
from pathlib import Path

from day_1.train import train


def test_regression():

    with tempfile.TemporaryDirectory() as tmpdir:
        # given
        train_date = date(2022,1,1)
        val_date = date(2022,2,1)
        out_path = Path(tmpdir) / "model.pkl"

        # when
        mse = train(train_date, val_date, out_path)

        # then
        expected_mse = 8.189
        assert abs(expected_mse - mse) < 0.1

def test_file_gets_created():
    with tempfile.TemporaryDirectory() as tmpdir:
        # given
        train_date = date(2022,1,1)
        val_date = date(2022,2,1)
        out_path = Path(tmpdir) / "model.pkl"

        assert not out_path.exists()

        # when
        train(train_date, val_date, out_path)

        # then
        assert out_path.exists()