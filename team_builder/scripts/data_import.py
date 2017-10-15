import os
import django
import sys
import json


sys.path.append('../team_builder')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "team_builder.settings")
django.setup()

from accounts.models import Skill


with open('scripts/skills.json', 'r') as file:
    data = json.load(file)
    for skill in data:
        Skill.objects.create(name=skill)
