from django.db import IntegrityError
from rest_framework.decorators import api_view
from src.api.serializers.funcionario_serializer import FuncionarioSerializer
from src.api.services.funcionario_service import FuncionarioService
from src.api.utils.response import success, error




@api_view(["POST"])
def cadastrar_funcionario(request):

    serializer = FuncionarioSerializer(data=request.data)


    if serializer.is_valid():

        try:

            funcionario = (FuncionarioService.criar_funcionario(serializer.validated_data))

            return success(

                data=FuncionarioSerializer(funcionario).data,message="Funcionário cadastrado com sucesso!", status=201)

        except IntegrityError:

            return error(message="Email já cadastrado", status=400)

        except Exception as e:

            return error(message=str(e), status=500)

    return error(message=serializer.errors, status=400)



@api_view(["GET"])
def listar_funcionarios(request):


    try:

        data = (FuncionarioService.listar_funcionarios())

        return success(data=data)
        
    except Exception as e:

        return error(message=str(e), status=500)



@api_view(["GET"])
def buscar_funcionario(request, id_funcionario):

    try:

        data = (FuncionarioService.buscar_funcionario(id_funcionario))

        return success(data=data)


    except ValueError as e:

        return error(message=str(e), status=404)

    except Exception as e:

        return error(message=str(e), status=500)

@api_view(["PUT"])
def atualizar_funcionario(request, id_funcionario):

    serializer = FuncionarioSerializer(data=request.data, partial=True)



    if serializer.is_valid():


        try:

            funcionario = (
                FuncionarioService.atualizar_funcionario(
                    id_funcionario, serializer.validated_data))
            
            return success(
                data=FuncionarioSerializer(funcionario).data,
                message="Funcionário atualizado com sucesso!"
)

        except ValueError as e:

            return error(message=str(e), status=404)
            
        except IntegrityError:

            return error(message="Email já cadastrado", status=400)


        except Exception as e:

            return error(message=str(e), status=500)

    return error(message=serializer.errors, status=400)

@api_view(["DELETE"])
def deletar_funcionario(request, id_funcionario):
    
    try:

        FuncionarioService.deletar_funcionario(id_funcionario)

        return success(message="Funcionário deletado com sucesso!")

    except ValueError as e:

        return error(message=str(e), status=404)

    except Exception as e:

        return error(message=str(e), status=500)