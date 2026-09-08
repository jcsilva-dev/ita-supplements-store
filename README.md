# E-commerce de Suplementos

Plataforma de e-commerce desenvolvida com Python e Django para uma loja de suplementos, com foco em catálogo de produtos, carrinho de compras e fluxo de atendimento e finalização de pedidos via WhatsApp.

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de simular um cenário real de negócio, desde a descoberta dos produtos pelo cliente até o encaminhamento do pedido para atendimento.

A aplicação possui uma estrutura de catálogo, gerenciamento de produtos e variantes, carrinho de compras, avaliações e recomendações, além da integração do fluxo de checkout com o WhatsApp.

A decisão de não utilizar um gateway de pagamento foi intencional: o sistema organiza as informações do pedido e direciona o cliente para o WhatsApp da loja, onde o atendimento e a conclusão da venda acontecem.

## Funcionalidades

- Catálogo e listagem de produtos
- Categorias e busca
- Página de detalhes dos produtos
- Gerenciamento de preços e disponibilidade
- Variantes de produtos
- Recomendações de produtos
- Carrinho de compras
- Avaliações e feedbacks
- Fluxo de checkout via WhatsApp
- Painel administrativo para gerenciamento da aplicação
- Layout responsivo

## Arquitetura

A aplicação foi estruturada utilizando Django Apps para separar responsabilidades do domínio e facilitar a evolução do projeto.

A camada de apresentação utiliza Django Templates, HTML, CSS e JavaScript, enquanto as regras de negócio e persistência são implementadas utilizando Python, Django e Django ORM.

O projeto também foi desenvolvido pensando em organização, reutilização de lógica e separação de responsabilidades, evitando concentrar toda a regra de negócio nas views.

## Fluxo de compra

O fluxo principal da aplicação funciona da seguinte forma:

```text
Catálogo
   ↓
Produto
   ↓
Seleção de variante
   ↓
Carrinho
   ↓
Resumo do pedido
   ↓
WhatsApp
   ↓
Atendimento e finalização da venda



## Fluxo de compra

O carrinho é responsável por organizar os produtos e quantidades selecionados pelo cliente. No momento do checkout, as informações do pedido são utilizadas para construir a mensagem enviada ao atendimento da loja pelo WhatsApp.

## Tecnologias

### Backend

- Python
- Django
- Django ORM

### Banco de dados

- PostgreSQL
- SQL

### Frontend

- HTML
- CSS
- JavaScript
- Django Templates

### Ferramentas

- Git
- GitHub
- VS Code

## Objetivos técnicos

Além da implementação das funcionalidades de e-commerce, o projeto foi utilizado para aprofundar conceitos de desenvolvimento de aplicações web com Django, incluindo:

- Modelagem de dados e relacionamentos
- Organização de Django Apps
- Django ORM
- QuerySets e Managers
- Separação de responsabilidades
- Regras de negócio
- Validação de dados
- Operações transacionais
- Integração entre diferentes partes da aplicação
- Testes
- Organização e manutenção do código

## Status

Projeto desenvolvido como uma aplicação de e-commerce funcional e utilizado como projeto de estudo e evolução prática em desenvolvimento web com Django.

Novas funcionalidades e melhorias podem ser incorporadas conforme a evolução da arquitetura.

## Autor

**José Carlos Silva**

GitHub: [@jcsilva-dev](https://github.com/jcsilva-dev)

LinkedIn: [jcsilva-dev](https://www.linkedin.com/in/jcsilva-dev)
