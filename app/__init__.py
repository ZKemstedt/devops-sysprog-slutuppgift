from pathlib import Path

# Create data folder+file if they don't exist
file = Path('collectiondata', 'boardgamecollections.yml')
file.parent.mkdir(exist_ok=True)
