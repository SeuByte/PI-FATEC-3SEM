from decimal import Decimal, ROUND_HALF_UP

# 1. Simulando o dado cru: O MongoDB te devolve um float.
# Imagine que o preço real era 10.33, mas na memória virou essa dízima.
valor_venda_banco = 10.33333333333333 
quantidade_comprada = 3

print("--- O JEITO ERRADO (Matemática com Float) ---")
subtotal_bugado = valor_venda_banco * quantidade_comprada
print(f"Resultado Float: {subtotal_bugado}") 
# Resultado vai ser 30.99999999999999 (O cliente perdeu 1 centavo)

print("\n--- O JEITO CERTO (O Cofre do Carrinho) ---")
# Transforma o float para texto, depois para Decimal arredondado
preco_seguro = Decimal(str(valor_venda_banco)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
qtd_segura = Decimal(str(quantidade_comprada))

subtotal_exato = preco_seguro * qtd_segura
print(f"Preço Unitário (Decimal): {preco_seguro}")
print(f"Subtotal Perfeito (Decimal): {subtotal_exato}")
# Resultado será 31.00 exatos.

print("\n--- A SAÍDA DO SERIALIZER (A Vitrine) ---")
# Aqui é o que você vai retornar no return { ... } do seu Serializer
json_resposta = {
    "preco_unitario": str(preco_seguro),
    "subtotal": str(subtotal_exato)
}
print(f"O que o Frontend recebe: {json_resposta}")