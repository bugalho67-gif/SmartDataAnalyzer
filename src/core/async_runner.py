"""Execução segura de corrotinas em contextos síncronos."""

import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

ResultT = TypeVar("ResultT")


class AsyncRunner:
    """Executa uma corrotina em um novo event loop."""

    @staticmethod
    def run(coroutine: Coroutine[Any, Any, ResultT]) -> ResultT:
        """Executa a corrotina e devolve seu resultado."""
        return asyncio.run(coroutine)


def run_async(coroutine: Coroutine[Any, Any, ResultT]) -> ResultT:
    """Atalho funcional para :meth:`AsyncRunner.run`."""
    return AsyncRunner.run(coroutine)
