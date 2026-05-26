## RF001 — Login Administrativo
O sistema deve permitir login de administradores e funcionários.

---

## RF002 — Controle de Permissões
O sistema deve possuir níveis de acesso:
- Administrador
- Funcionário
- Estoque
- Atendimento

---

## RF003 — Recuperação de Senha
O sistema deve permitir recuperação de senha via e-mail.

---

# 4.2 Cadastro de Produtos

## RF004 — Cadastro de Produtos
O sistema deve permitir cadastro de produtos contendo:
- Nome
- Descrição
- Categoria
- Marca
- Peso
- Unidade
- SKU
- Código de barras
- Valor
- Valor promocional
- Estoque
- Imagens
- Status ativo/inativo

---

## RF005 — Categorias
O sistema deve permitir cadastro de categorias.

---

## RF006 — Imagens dos Produtos
O sistema deve permitir múltiplas imagens por produto.

---

## RF007 — Produtos em Destaque
O sistema deve permitir marcar produtos como destaque.

---

## RF008 — Promoções
O sistema deve permitir cadastro de promoções e descontos.

---

# Requisitos Funcionais — Controle de Estoque

## RF009 — Controle de Estoque
O sistema deve possuir um módulo de controle de estoque integrado ao e-commerce.

---

## RF010 — Cadastro de Produtos no Estoque
O sistema deve permitir cadastro e gerenciamento dos produtos contendo os seguintes campos:

| Campo | Descrição |
|---|---|
| Referência | Código interno do produto |
| Descrição | Nome/descrição do produto |
| Estoque | Quantidade disponível |
| Unidade | Unidade de medida do produto |
| Valor venda | Valor de venda do produto |
| Cód. grupo | Código da categoria/grupo |
| Grupo | Nome da categoria do produto |
| Preço 100g | Valor proporcional por 100g |

---

## RF011 — Atualização Automática de Estoque
O sistema deve atualizar automaticamente a quantidade disponível dos produtos após:
- Venda
- Cancelamento
- Entrada de mercadoria
- Ajustes manuais

---

## RF012 — Controle de Movimentações
O sistema deve registrar histórico de:
- Entradas
- Saídas
- Perdas
- Ajustes
- Cancelamentos

---

## RF013 — Controle por Unidade
O sistema deve permitir diferentes unidades de medida, como:
- KG
- G
- Unidade
- Caixa
- Pacote
- Litro

---

## RF014 — Controle de Categorias
O sistema deve permitir organizar produtos por grupos/categorias.

---

## RF015 — Estoque Baixo
O sistema deve alertar quando produtos atingirem quantidade mínima configurada.

---

## RF016 — Bloqueio de Venda Sem Estoque
O sistema não deve permitir vendas de produtos indisponíveis.

---

## RF017 — Busca de Produtos
O sistema deve permitir pesquisa por:
- Referência
- Descrição
- Grupo
- Código do grupo

---

## RF018 — Precificação
O sistema deve permitir:
- Valor padrão de venda
- Valor promocional
- Preço por peso (100g)

---

## RF019 — Integração com E-commerce
O estoque deve ser sincronizado automaticamente com a loja virtual em tempo real.

---

## RF020 — Importação de Produtos
O sistema deve permitir importação de produtos via:
- Excel (.xlsx)
- CSV

---

## RF021 — Exportação de Estoque
O sistema deve permitir exportar relatórios de estoque em:
- Excel
- PDF

---

## RF022 — Dashboard de Estoque
O sistema deve apresentar:
- Produtos com baixo estoque
- Produtos mais vendidos
- Quantidade total em estoque
- Valor total do estoque
- Movimentações recentes

# 4.4 Loja Virtual

## RF023 — Catálogo de Produtos
Clientes devem visualizar produtos cadastrados.

---

## RF024 — Busca de Produtos
O sistema deve possuir busca por:
- Nome
- Categoria
- Marca

---

## RF025 — Filtros
O sistema deve permitir filtros:
- Categoria
- Preço
- Marca
- Promoção

---

## RF026 — Carrinho de Compras
Clientes devem conseguir adicionar produtos ao carrinho.

---

## RF027 — Finalização de Pedido
Clientes devem conseguir finalizar compras.

---

## RF028 — Cadastro de Clientes
O sistema deve permitir cadastro de clientes.

---

## RF029 — Área do Cliente
O cliente deve visualizar:
- Pedidos
- Dados pessoais
- Endereços

---

## RF030 — Cálculo de Frete
O sistema deve calcular frete automaticamente.

---

## RF031 — Métodos de Pagamento
O sistema deve aceitar:
- PIX
- Cartão
- Boleto

---

## RF032 — Status do Pedido
O cliente deve acompanhar:
- Aguardando pagamento
- Pago
- Separação
- Enviado
- Entregue
- Cancelado

---

# 4.5 Painel Administrativo

## RF033 — Dashboard Administrativo
O sistema deve possuir dashboard contendo:
- Vendas
- Pedidos
- Faturamento
- Produtos vendidos
- Estoque

---

## RF034 — Gestão de Pedidos
Administradores devem gerenciar pedidos.

---

## RF035 — Atualização de Status
O administrador deve alterar status dos pedidos.

---

## RF036 — Relatórios
O sistema deve gerar relatórios:
- Vendas
- Estoque
- Produtos
- Clientes
- Faturamento

---

## RF037 — Exportação de Relatórios
O sistema deve exportar relatórios em:
- PDF
- Excel

---

# 4.6 Integrações

## RF038 — Gateway de Pagamento
O sistema deve integrar com gateways de pagamento.

---

## RF039 — Correios e Transportadoras
O sistema deve calcular frete e rastreamento.

---

## RF040 — WhatsApp
O sistema deve permitir notificações via WhatsApp.

---

## RF041 — E-mails Automáticos
O sistema deve enviar e-mails automáticos de:
- Confirmação
- Pagamento
- Envio
- Recuperação de senha

---

# 5. Requisitos Não Funcionais

# 5.1 Performance

## RNF001 — Tempo de Resposta
O sistema deve responder em até 3 segundos.

---

## RNF002 — Acessos Simultâneos
O sistema deve suportar múltiplos usuários simultaneamente.

---

# 5.2 Segurança

## RNF003 — Criptografia
As senhas devem ser armazenadas criptografadas.

---

## RNF004 — HTTPS
O sistema deve utilizar HTTPS.

---

## RNF005 — Sessões Seguras
O sistema deve utilizar autenticação segura.

---

## RNF006 — Backup
O sistema deve possuir backups automáticos.

---

# 5.3 Usabilidade

## RNF007 — Responsividade
O sistema deve funcionar em:
- Desktop
- Tablet
- Celular

---

## RNF008 — Interface Intuitiva
O sistema deve possuir interface simples e intuitiva.

---

## RNF009 — Compatibilidade
O sistema deve funcionar nos principais navegadores:
- Chrome
- Edge
- Firefox
- Safari

---

# 5.4 Escalabilidade

## RNF010 — Estrutura Modular
O sistema deve permitir futuras expansões.

---

## RNF011 — Banco Escalável
O banco de dados deve suportar crescimento de dados.

---

# 5.5 Disponibilidade

## RNF012 — Disponibilidade
O sistema deve possuir disponibilidade mínima de 99%.

---

# 6. Tecnologias Utilizadas

## 6.1 Frontend
O frontend do sistema será desenvolvido utilizando:

- React
- Vite
- TailwindCSS
- Axios
- React Router DOM

---

## 6.2 Backend
O backend do sistema será desenvolvido utilizando:

- Python
- Django
- Django REST Framework (DRF)

---

## 6.3 Ambiente Virtual
O projeto backend deverá utilizar ambiente virtual Python com:

- venv

---

## 6.4 Banco de Dados
O sistema utilizará:

- MongoDB

---

## 6.5 Containerização
O sistema deverá utilizar:

- Docker
- Docker Compose

---

## 6.6 Infraestrutura
A infraestrutura do sistema deverá utilizar:

- VPS Linux
- Docker
- Nginx ou Caddy

---

## 6.7 Controle de Versão
O projeto deverá utilizar:

- Git
- GitHub

---

# 7. Estrutura Base do Projeto

## 7.1 Estrutura Frontend

```bash
frontend/
├── src/
├── public/
├── package.json
├── vite.config.js
└── tailwind.config.js
```

---

## 7.2 Estrutura Backend

```bash
backend/
├── venv/
├── app/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

---

## 7.3 Estrutura Banco de Dados

```bash
mongodb/
```

---

# 8. Requisitos Técnicos

## RT001 — API REST
O backend deverá fornecer API REST para comunicação com frontend.

---

## RT002 — Autenticação JWT
O sistema deverá utilizar autenticação JWT.

---

## RT003 — Dockerização
Todos os serviços deverão rodar via Docker.

---

## RT004 — Persistência de Dados
O MongoDB deverá possuir volume persistente.

---

## RT005 — Variáveis de Ambiente
O sistema deverá utilizar arquivo `.env` para:
- URLs
- Senhas
- Tokens
- Configurações

---

## RT006 — Segurança
As senhas deverão ser criptografadas.

---

## RT007 — Escalabilidade
O sistema deverá possuir arquitetura escalável e modular.

---

# 9. Dependências Backend

## Principais bibliotecas Python

```txt
Django
djangorestframework
djongo ou mongoengine
django-cors-headers
python-dotenv
gunicorn
pymongo
djangorestframework-simplejwt
Pillow
```

---

# 10. Serviços Docker

## Containers previstos

- Frontend React
- Backend Django
- MongoDB
- Nginx/Caddy

---

# 11. Deploy

## Ambiente de Produção

O sistema deverá ser implantado em VPS Linux utilizando:
- Docker Compose
- HTTPS
- Proxy reverso
- Backup automático

---

# 12. Objetivo da Arquitetura

A arquitetura foi definida visando:

- Alta performance
- Facilidade de manutenção
- Escalabilidade
- Segurança
- Facilidade de deploy
- Organização do sistema
- Separação clara entre frontend e backend