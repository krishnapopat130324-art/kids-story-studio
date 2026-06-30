# story_generator.py - Kids Story Generator

import random
import ollama
from config import LLM_MODEL, AGE_GROUPS, STORY_THEMES, VALUES

class StoryGenerator:
    def __init__(self):
        self.themes = {
            "🏰 Adventure": ["magical forest", "secret treasure", "hidden castle", "mysterious island", "dragon's cave", "ancient ruins", "enchanted valley"],
            "🐾 Animals": ["puppy", "kitten", "elephant", "dolphin", "lion", "tiger", "panda", "penguin", "butterfly", "rabbit"],
            "🚀 Space": ["astronaut", "alien", "rocket", "moon", "planet", "stars", "spaceship", "galaxy", "comet"],
            "🦄 Fantasy": ["unicorn", "dragon", "fairy", "mermaid", "wizard", "magical creature", "elf", "giant", "troll"],
            "🏫 Everyday Life": ["school", "park", "birthday party", "family", "friends", "playground", "museum", "library"],
            "🌊 Underwater": ["mermaid", "ocean", "coral reef", "sea creature", "treasure", "shipwreck", "dolphin", "whale"],
            "🌳 Nature": ["forest", "garden", "river", "mountain", "flowers", "trees", "waterfall", "meadow", "sunset"],
            "🎪 Circus": ["clown", "acrobat", "magician", "animals", "tent", "performance", "tightrope", "juggler"]
        }
        
        self.values = VALUES
        self.character_names = [
            "Emma", "Leo", "Mia", "Noah", "Ava", "Liam",
            "Sophia", "Oliver", "Isabella", "Lucas", "Mila", "Ethan",
            "Harper", "James", "Ella", "Alexander", "Amelia", "Benjamin"
        ]
        
        # Story openings for variety
        self.story_openings = [
            "Once upon a time, in a world filled with wonder",
            "On a bright and beautiful morning",
            "In a land where magic was real and dreams came true",
            "Deep in the heart of a magical kingdom",
            "When the stars aligned perfectly that night",
            "On a day unlike any other",
            "In the most enchanted corner of the world",
            "Long ago, in a place where imagination ruled",
            "There once was a child who believed in magic"
        ]
        
        # Story endings for variety
        self.story_endings = [
            "And they all lived happily ever after.",
            "And that's how {name} learned the true meaning of {value}.",
            "From that day forward, {name} never forgot the lesson about {value}.",
            "And so, {name} became the kindest person in the kingdom.",
            "The end... or maybe just the beginning of more adventures!",
            "And {name} knew that {value} was the greatest magic of all.",
            "They all learned that {value} makes the world a better place."
        ]
    
    def generate_story(self, child_name, age, theme, value):
        """Generate a personalized story for a child"""
        
        # Get age group info
        age_key = self._get_age_key(age)
        age_info = AGE_GROUPS[age_key]
        
        # Get theme elements
        theme_key = theme
        main_element = random.choice(self.themes.get(theme_key, self.themes["🏰 Adventure"]))
        
        # Get random opening
        opening = random.choice(self.story_openings)
        
        # Get random ending
        ending = random.choice(self.story_endings)
        ending = ending.replace("{name}", child_name).replace("{value}", value.lower())
        
        # Build the prompt
        prompt = f"""You are a warm, kind children's story writer. Create a magical, educational story for a child.

CHILD'S NAME: {child_name}
AGE: {age} years old (use {age_info['style']} language)
THEME: {theme} (center the story around {main_element})
VALUE TO TEACH: {value}
STYLE: {age_info['style']}, warm, engaging, positive, magical
LENGTH: About {age_info['word_count']} words

STORY OPENING: "{opening}"

IMPORTANT RULES:
1. Make {child_name} the HERO of the story
2. Teach about {value} in a natural, gentle way
3. Use age-appropriate language for a {age}-year-old
4. Include {main_element} as a key part of the adventure
5. Have a happy, positive ending
6. The story should be engaging and fun!

Now write a beautiful, magical story for {child_name}:

STORY:
"""
        
        try:
            response = ollama.chat(
                model=LLM_MODEL,
                messages=[{'role': 'user', 'content': prompt}]
            )
            story = response['message']['content']
            
            # Format and add ending
            story = self._format_story(story, child_name, value, ending)
            
            return story
            
        except Exception as e:
            print(f"Error generating story: {e}")
            # Return a beautiful fallback story
            return self._fallback_story(child_name, age, theme, main_element, value, opening, ending)
    
    def _get_age_key(self, age):
        """Get age group key"""
        if age <= 5:
            return "3-5"
        elif age <= 8:
            return "6-8"
        else:
            return "9-12"
    
    def _format_story(self, story, name, value, ending):
        """Format and clean the story"""
        # Remove extra whitespace
        story = story.strip()
        
        # Remove markdown formatting
        story = story.replace('**', '').replace('*', '')
        
        # Ensure proper paragraphs (double line breaks)
        paragraphs = story.split('\n')
        cleaned_paragraphs = []
        for p in paragraphs:
            p = p.strip()
            if p:
                cleaned_paragraphs.append(p)
        
        # Add title if missing
        if not cleaned_paragraphs or (len(cleaned_paragraphs) > 0 and not cleaned_paragraphs[0].startswith(name)):
            title = f"🌟 **{name}'s {value} Adventure**"
            cleaned_paragraphs.insert(0, title)
        
        # Add ending if not already there
        last_line = cleaned_paragraphs[-1] if cleaned_paragraphs else ""
        if not any(word in last_line.lower() for word in ['end', 'ever after', 'lesson', 'learn']):
            cleaned_paragraphs.append("")
            cleaned_paragraphs.append(ending)
        
        # Join paragraphs with double newline
        return '\n\n'.join(cleaned_paragraphs)
    
    def _fallback_story(self, name, age, theme, element, value, opening, ending):
        """Beautiful fallback story when AI fails"""
        
        # Get age-appropriate language
        if age <= 5:
            simple = True
        else:
            simple = False
        
        story_parts = []
        story_parts.append(f"🌟 **{name}'s {value} Adventure**")
        story_parts.append("")
        story_parts.append(f"{opening}, there lived a wonderful {age}-year-old named {name}.")
        story_parts.append("")
        
        if simple:
            story_parts.append(f"{name} loved to explore and learn new things. One day, while playing in the garden, {name} found a magical {element}!")
        else:
            story_parts.append(f"{name} was a curious child who believed that magic existed everywhere. One extraordinary day, while exploring the {element}, {name} discovered something truly magical.")
        
        story_parts.append("")
        story_parts.append(f"The {element} sparkled with rainbow colors and spoke in a gentle voice. 'Hello, {name}! I've been waiting for someone brave and kind like you.'")
        story_parts.append("")
        story_parts.append(f"{name} was amazed! 'What are you?' {name} asked.")
        story_parts.append("")
        story_parts.append(f"'I am the Guardian of {value},' said the {element}. 'And I need your help to spread {value} throughout the land.'")
        story_parts.append("")
        
        if simple:
            story_parts.append(f"{name} smiled. 'I want to help! What can I do?'")
            story_parts.append("")
            story_parts.append(f"'Just be yourself,' said the Guardian. 'Show others what it means to be {value}. When you are {value}, you make the world a better place.'")
            story_parts.append("")
            story_parts.append(f"So {name} went on a journey, being kind and showing {value} to everyone they met. The people were inspired by {name}'s example!")
        else:
            story_parts.append(f"{name} thought carefully. 'What does it mean to spread {value}?'")
            story_parts.append("")
            story_parts.append(f"'It means being {value} even when it's hard,' explained the Guardian. 'It means choosing {value} in every situation, no matter what.'")
            story_parts.append("")
            story_parts.append(f"{name} nodded, understanding. 'I will try my best!'")
            story_parts.append("")
            story_parts.append(f"And so {name} traveled far and wide, showing everyone what it truly means to be {value}. Through small acts of {value} and big ones, {name} changed the world around them.")
        
        story_parts.append("")
        story_parts.append(ending)
        story_parts.append("")
        story_parts.append(f"✨ *Remember, {name}: Being {value} is the greatest superpower of all!* ✨")
        
        return '\n'.join(story_parts)