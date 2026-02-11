#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Créer les catégories par défaut
python manage.py shell -c "
from biens.models import Category
for name in ['Appartement', 'Maison', 'Villa', 'Studio', 'Bureau', 'Terrain']:
    Category.objects.get_or_create(name=name)
print('Categories OK')
"
