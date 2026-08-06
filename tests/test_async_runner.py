"""AsyncRunner tests."""

import asyncio

import pytest

from src.core.async_runner import AsyncRunner, run_async


async def _sample_coro(value: int) -> int:
    await asyncio.sleep(0.01)
    return value * 2


def test_async_runner_basic():
    result = AsyncRunner.run(_sample_coro(21))
    assert result == 42


def test_async_runner_exception():
    async def failing():
        raise ValueError("test error")

    with pytest.raises(ValueError, match="test error"):
        AsyncRunner.run(failing())


def test_run_async_convenience():
    result = run_async(_sample_coro(10))
    assert result == 20


def test_multiple_runs():
    results = [AsyncRunner.run(_sample_coro(i)) for i in range(5)]
    assert results == [0, 2, 4, 6, 8]
