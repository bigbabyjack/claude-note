from .llm import ClaudeConfig, ask_claude
from .note import Note, read_note


def summarize_prompt(notes: list[Note]) -> str:
    notes_str = "\n".join(f"- {read_note(note)}" for note in notes)
    prompt = (
        f"Given the following notes:\n{notes_str}\n\nSummarize them in a few sentences."
    )
    return prompt


async def summarize(notes: list[Note], config: ClaudeConfig) -> str:
    if not notes:
        return "No notes to summarize."

    summary = await ask_claude(
        summarize_prompt(notes),
        config,
    )
    return summary
