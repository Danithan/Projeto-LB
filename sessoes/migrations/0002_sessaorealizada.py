from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessoes', '0001_initial'),
        ('criancas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SessaoRealizada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('status', models.CharField(choices=[('em_andamento', 'Em Andamento'), ('concluida', 'Concluída')], max_length=20)),
                ('observacoes', models.TextField(blank=True)),
                ('crianca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='criancas.crianca')),
                ('sessao_modelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sessoes.sessaomodelo')),
                ('terapeuta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
