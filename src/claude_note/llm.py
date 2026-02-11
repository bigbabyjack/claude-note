"""LLM integration using the Claude CLI."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ClaudeConfig:
    cmd: list[str] = field(default_factory=lambda: ["claude", "-p"])
    model: Literal["haiku", "sonnet", "opus"] = "sonnet"
    timeout: int = 120


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
