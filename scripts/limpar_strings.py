import os
import django
import json
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exercicios.models import ExercicioModelo

count = 0
for e in ExercicioModelo.objects.all():
    changed = False
    
    if '[PILOTO]' in e.enunciado or 'NÃO APLICAR' in e.enunciado or 'NAO APLICAR' in e.enunciado or 'NO APLICAR' in e.enunciado:
        e.enunciado = re.sub(r'\[PILOTO\]|NÃO APLICAR|NAO APLICAR|N.O APLICAR', '', e.enunciado).strip()
        e.enunciado = re.sub(r'\s-\s', ' ', e.enunciado).strip()
        changed = True
        
    config_str = json.dumps(e.configuracao)
    if '[PILOTO]' in config_str or 'NÃO APLICAR' in config_str or 'NAO APLICAR' in config_str or 'NO APLICAR' in config_str:
        config_str = re.sub(r'\[PILOTO\]|NÃO APLICAR|NAO APLICAR|N.O APLICAR', '', config_str)
        config_str = re.sub(r'\s-\s', ' ', config_str).strip()
        try:
            e.configuracao = json.loads(config_str)
            changed = True
        except:
            pass
        
    if changed:
        e.save()
        count += 1
        
print(f'Atualizados {count} exercícios.')
