# pyrefly: ignore [missing-import]
from django.db import migrations, models
# pyrefly: ignore [missing-import]
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercicios', '0001_initial'),
        ('sessoes', '0002_sessaorealizada'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExercicioResultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem_execucao', models.IntegerField()),
                ('percentual_acerto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tentativas', models.IntegerField()),
                ('tempo_segundos', models.IntegerField()),
                ('pontuacao', models.IntegerField()),
                ('respondido_em', models.DateTimeField(auto_now_add=True)),
                ('exercicio_modelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exercicios.exerciciomodelo')),
                ('sessao_realizada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessoes.sessaorealizada')),
            ],
        ),
    ]
