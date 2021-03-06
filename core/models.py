from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from PIL import Image

# Create your models here.

class Livro(models.Model):
	NIVEL_CONSERVACAO = (
        ('ruim', 'Ruim'),
        ('razoavel', 'Razoavel'),
        ('bom', 'Bom'),
        ('excelente', 'Excelente')
    )

	foto = models.ImageField(upload_to='static/img', null=True, blank = True)
	titulo = models.CharField(max_length=45)
	autor = models.CharField(max_length=75)
	edicao = models.CharField(max_length=10)
	genero = models.ManyToManyField('Genero')
	nivel_conservacao = models.CharField(max_length=45, choices=NIVEL_CONSERVACAO)
	dono = models.ForeignKey('user.Usuario', on_delete=models.CASCADE,related_name='meus_livros')	

	def __str__(self):
		return self.titulo

	def save(self):
		super(Livro, self).save()
		if not Anuncio.objects.filter(livro=self):			
			Anuncio.objects.create(livro=self)
	
		if not self.foto:
		    return None 		

		image = Image.open(self.foto)		
		size = (250,250)
		image = image.resize(size, Image.ANTIALIAS)
		image.save(self.foto.path)


class Transacao(models.Model):
	emissor = models.ForeignKey('user.Usuario', on_delete=models.CASCADE,related_name='livros_desapegados')
	receptor = models.ForeignKey('user.Usuario', on_delete=models.CASCADE,related_name='livros_adiquiridos')
	livro = models.OneToOneField('Livro', on_delete=models.CASCADE,related_name='minha_transacao')	
	data_transacao = models.DateField(auto_now=True)

	def checar_usuario_dono(self):
		if self.livro.dono == self.receptor:			
			raise Exception('Você não pode adquirir o proprio livro')

	def checar_livro(self):
		#checar se o livro ja foi doado ou trocado
		if Transacao.objects.filter(livro=self.livro):
			raise ValidationError('Livro ja negociado')	

	def checar_usuario_receptor(self):
		#checar se o usuario recebeu 3 doações no mês se sim, raise execption		
		if Transacao.objects.filter(receptor=self.receptor).filter(data_transacao__month=
			datetime.now().month).filter(data_transacao__year=datetime.now().year).count() >= (3 + self.receptor.livros_doado_no_mes()):
			raise ValidationError('Ja recebeu mais doações de livros do que o permitido esse mês')		

	def clean(self):		
		super(Transacao, self).clean()
		self.checar_livro()
		self.checar_usuario_receptor()
		self.checar_usuario_dono()

	def save(self, **kwargs):
		self.clean()
		super(Transacao, self).save()


class Anuncio(models.Model):
	livro = models.OneToOneField('Livro', on_delete=models.CASCADE,related_name='meu_anuncio')
	data_anuncio = models.DateTimeField(auto_now=True)	
	is_ativo = models.BooleanField(default=True)

	@property
	def dono(self):
		return self.livro.dono

class Genero(models.Model):
	nome = models.CharField(max_length=25)

	def __str__(self):
		return self.nome