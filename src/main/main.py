import json
import os
import logging
import typer
from typing import List
from pydantic import BaseModel

app = typer.Typer()
DB_FILE = "notes_db.json"

# Logging: The "Black Box" Recorder
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",  # This saves logs to a file named app.log
    filemode="a"  # "a" means append (don't overwrite old logs)
)


class Note(BaseModel):
    id: int
    title: str
    content: str


def load_notes() -> List[dict]:
    """Helper: Reads the JSON file and returns a list of notes."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_notes(notes: List[dict]):
    """Helper: Saves the list of notes to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(notes, f, indent=4)


@app.command()
def add(title: str, content: str):
    """The 'Core Action': Adds a new note to storage."""
    # Log the start of the action
    logging.info(f"App started: Adding note '{title}'")

    try:
        notes = load_notes()
        new_id = len(notes) + 1
        new_note = Note(id=new_id, title=title, content=content)

        notes.append(new_note.model_dump())
        save_notes(notes)

        # Log the success
        logging.info(f"Note #{new_id} saved successfully")
        typer.echo(f"✨ Success! Note #{new_id} added.")

    except Exception as e:
        # Log the error if it fails
        logging.error(f"Could not save note! Error: {e}")
        typer.echo("❌ An error occurred while saving the note.")


if __name__ == "_main_":
    app()