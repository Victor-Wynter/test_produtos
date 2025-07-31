from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produto
from .serializers import ProdutoSerializer

# Create your views here.

def index(request):
    """
    View para a página inicial que lista produtos.
    """
    return render(request, 'produtos/index.html')

def cadastro(request):
    """
    View para a página de cadastro de produtos.
    """
    return render(request, 'produtos/cadastro.html')

@api_view(['GET', 'POST'])
def produtos_api(request):
    """
    API para listar e criar produtos.
    GET: Lista todos os produtos
    POST: Cria um novo produto
    """
    if request.method == 'GET':
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def produtos_risco_api(request):
    """
    API para listar produtos com risco (THC > 0.3% e categoria específica).
    """
    produtos = Produto.objects.filter(
        thc_percentual__gt=0.3,
        categoria_terapeutica__in=['neurologia', 'pediatria']
    )
    
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data)
