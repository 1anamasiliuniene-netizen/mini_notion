import random

PHRASES = [
    "Keep pushing forward!",
    "You are capable of amazing things",
    "Every day is a new opportunity",
    "Small steps lead to big results",
    "Small steps today lead to big results tomorrow",
    "Progress, not perfection",
    "You are capable of more than you think",
    "Consistency beats intensity",
    "Every day is a fresh start",
    "Focus on progress, not comparison",
    "Discipline creates freedom",
    "Done is better than perfect",
    "One task at a time",
    "Growth begins outside your comfort zone",
    "Your future self will thank you",
    "Keep going — you’re building momentum",
    "Success is built on daily habits",
    "Stay focused. Stay determined",
    "Turn ideas into action",
    "Hard work compounds over time",
    "Believe in your ability to improve",
    "Start where you are. Use what you have",
    "Make today count",
    "You don’t have to be perfect — just persistent",
    "Keep shining today!",
    "Make every moment count!",
    "Dream big, act bigger!",
    "Small steps lead to big results!"
]

def hero_phrase(request):
    return {
        'hero_phrase': random.choice(PHRASES)
    }