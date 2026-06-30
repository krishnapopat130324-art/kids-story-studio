# config.py - Kids Story Studio (LIGHT BROWN THEME)

LLM_MODEL = "llama3.2"
DATA_DIR = "data/"
STORIES_DIR = "stories/"

# Kids Story Settings
AGE_GROUPS = {
    "3-5": {"word_count": 100, "style": "simple", "emoji": "👶"},
    "6-8": {"word_count": 200, "style": "medium", "emoji": "🧒"},
    "9-12": {"word_count": 350, "style": "advanced", "emoji": "🧑"}
}

STORY_THEMES = [
    "🏰 Adventure",
    "🐾 Animals", 
    "🚀 Space",
    "🦄 Fantasy",
    "🏫 Everyday Life",
    "🌊 Underwater",
    "🌳 Nature",
    "🎪 Circus"
]

VALUES = [
    "Kindness", "Honesty", "Courage", "Patience", 
    "Friendship", "Sharing", "Respect", "Responsibility",
    "Forgiveness", "Gratitude", "Empathy", "Confidence"
]

CHARACTER_NAMES = [
    "Emma", "Leo", "Mia", "Noah", "Ava", "Liam",
    "Sophia", "Oliver", "Isabella", "Lucas", "Mila", "Ethan",
    "Harper", "James", "Ella", "Alexander", "Amelia", "Benjamin"
]