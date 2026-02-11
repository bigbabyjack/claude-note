from .llm import ClaudeConfig, ask_claude
from .note import Note, read_note


def categorize_prompt(notes: list[Note], categories: list[str]) -> str:
    notes_str = "\n".join(f"- {read_note(note)}" for note in notes)
    categories_str = "\n".join(f"- {cat}" for cat in categories)
    prompt = (
        f"Given the following notes:\n{notes_str}\n\n"
        f"Categorize them into one of the following categories:\n{categories_str}\n\n"
        "Return only the category name."
    )
    return prompt


async def categorize(
    notes: list[Note], categories: list[str], config: ClaudeConfig
) -> str:
    if not categories:
        return "Uncategorized"
    if len(categories) == 1:
        return categories[0]
    category = await ask_claude(
        categorize_prompt(notes, categories),
        config,
    )
    return category
