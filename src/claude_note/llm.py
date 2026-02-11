"""LLM integration using the Claude CLI."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ClaudeConfig:
    model: Literal["haiku", "sonnet", "opus"] = "sonnet"
    timeout: int = 30

    @property
    def cmd(self) -> list[str]:
        return ["claude", "--model", self.model, "-p"]


async def ask_claude(prompt: str, config: ClaudeConfig) -> str:
    """Ask a question to Claude using the CLI."""
    cmd: list[str] = config.cmd
    cmd.append(prompt)

    process = None
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=config.timeout,
        )

        if process.returncode != 0:
            error_msg = f"Claude CLI failed: {stderr.decode().strip()}"
            raise RuntimeError(error_msg)

        return stdout.decode().strip()

    except TimeoutError as e:
        if process:
            process.kill()
            await process.wait()
        raise TimeoutError(f"Claude CLI timed out after {config.timeout}s") from e
