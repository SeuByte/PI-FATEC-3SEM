from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages 
from .models import Clientes, Produtos

def index(request):
    return render(request, 'index.html')

def lista_cliente(request):
    clientes = Clientes.objects()
    return render(request, 'lista_cliente.html', {'clientes': clientes})


def lista_produtos(request):
    produtos = Produtos.objects()
    return render(request, 'lista_produtos.html', {'produtos': produtos})


def login_cliente(request):
    return render(request, 'login_cliente.html')


def cadastro_cliente(request) :
    if request.method == 'POST':
        try:
            Clientes.objects.create(
                Nome=request.POST.get('nome'),
                Email=request.POST.get('email'),
                Senha=request.POST.get('senha'),
                Telefone=request.POST.get('telefone'),
                Data_nasc=request.POST.get('data_nasc'),
                CPF=request.POST.get('cpf'),
                CEP=request.POST.get('cep'),
                Endereco=request.POST.get('endereco'),
                Bairro=request.POST.get('bairro'),
                Numero=request.POST.get('numero'),
                Complemento=request.POST.get('complemento'),
                Cidade=request.POST.get('cidade'),
                Estado=request.POST.get('estado')
            )
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('index')
        except:
            messages.error(request, f"Erro ao cadastrar, verifique os dados")
            return render(request, 'cadastrar_cliente.html')
            
    return render(request, 'cadastrar_cliente.html')