from django.shortcuts import render, redirect
from .models import Story
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import os
import random

def generate_placeholder_image(story_id, title):
    colors = [(135, 206, 235), (255, 182, 193), (144, 238, 144)]  # Sky blue, pink, light green
    image_paths = []
    for i, color in enumerate(colors, 1):
        img = Image.new('RGB', (300, 200), color=color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("comic.ttf", 20)
        except:
            font = ImageFont.load_default()
        draw.text((10, 90), f"{title} - Page {i}", font=font, fill=(255, 255, 255))
        image_path = f"media/story_images/{story_id}_page{i}.jpg"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        img.save(image_path)
        image_paths.append(f"story_images/{story_id}_page{i}.jpg")
    return image_paths[0]

def generate_story():
    stories = [
        {
            "title": "The Happy Little Turtle",
            "content": (
                "Once upon a time, there was a happy little turtle named Timmy. "
                "Timmy loved to explore the forest with his friends, the bouncy bunny and the chirpy bird. "
                "One sunny day, they found a shiny treasure chest under a big oak tree. "
                "Inside, they discovered a map to a magical garden full of colorful flowers and yummy treats. "
                "They danced and played all day, happy to be together."
            )
        },
        {
            "title": "The Singing Cloud",
            "content": (
                "High above the hills, there was a fluffy cloud named Clara who loved to sing. "
                "Every morning, she floated over the village, humming a sweet tune that made the flowers bloom. "
                "One day, a little sparrow joined her song, and together they made the sun smile. "
                "The children below clapped and danced to their happy melody."
            )
        },
        {
            "title": "The Lost Star",
            "content": (
                "In a twinkly night sky, a tiny star named Stella fell to the ground. "
                "A curious fox found her glowing in the grass and promised to help her home. "
                "With the help of a wise owl and a speedy squirrel, they climbed the tallest tree. "
                "Stella jumped back into the sky, shining brighter than ever to say thank you."
            )
        }
    ]
    return random.choice(stories)["title"], random.choice(stories)["content"]

def create_story(request):
    if request.method == 'POST':
        title, content = generate_story()
        story = Story.objects.create(title=title, content=content)
        
        audio_path = f"media/audio/{story.id}.mp3"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        engine = pyttsx3.init()
        engine.setProperty('rate', 110)
        engine.setProperty('volume', 0.9)
        voices = [
            'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0',
            'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
        ]
        engine.setProperty('voice', random.choice(voices))
        engine.save_to_file(story.content, audio_path)
        engine.runAndWait()
        
        image_path = generate_placeholder_image(story.id, story.title)
        story.image = image_path  # Store first image in model
        story.save()
        
        return redirect('story_detail', story_id=story.id)
    return render(request, 'stories/create_story.html')

def story_list(request):
    show_favorites = request.GET.get('favorites', 'false') == 'true'
    stories = Story.objects.filter(is_favorite=True) if show_favorites else Story.objects.all()
    story_count = Story.objects.count()
    return render(request, 'stories/story_list.html', {
        'stories': stories,
        'story_count': story_count,
        'show_favorites': show_favorites
    })

def random_story(request):
    stories = Story.objects.all()
    if stories.exists():
        story = random.choice(stories)
        return redirect('story_detail', story_id=story.id)
    return redirect('story_list')

def story_detail(request, story_id):
    story = Story.objects.get(id=story_id)
    audio_path = f"media/audio/{story_id}.mp3"
    if not os.path.exists(audio_path):
        engine = pyttsx3.init()
        engine.setProperty('rate', 110)
        engine.setProperty('volume', 0.9)
        voices = [
            'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0',
            'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
        ]
        engine.setProperty('voice', random.choice(voices))
        engine.save_to_file(story.content, audio_path)
        engine.runAndWait()
    context = {
        'story': story,
        'audio_url': f"/media/audio/{story_id}.mp3",
    }
    return render(request, 'stories/story_detail.html', context)

def toggle_favorite(request, story_id):
    story = Story.objects.get(id=story_id)
    story.is_favorite = not story.is_favorite
    story.save()
    return redirect('story_detail', story_id=story_id)