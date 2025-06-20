SISTEMA DE CONTROLE DE ESTOQUE - PYTHON
===========================================

📦 FUNCIONALIDADES:
- Login com controle de acesso (admin e usuário comum)
- Cadastro e edição de produtos
- Registro de movimentações (entradas e saídas)
- Gerenciamento de usuários (somente para administradores)
- Relatório mensal com resumo de entradas, saídas e saldo
- Interface visual com Tkinter

-------------------------------------------
🔐 LOGIN PADRÃO
-------------------------------------------
Usuário: admin

Senha : admin

⚠️ Caso o login não funcione:
1. Exclua o arquivo 'estoque.db'
2. Execute o script 'banco.py' para recriar o banco de dados com usuário padrão

-------------------------------------------
🚀 COMO EXECUTAR O SISTEMA
-------------------------------------------
1. Certifique-se de ter o Python instalado (recomenda-se versão 3.10+)
2. Execute os arquivos na seguinte ordem:

   - Etapa 1: criar banco de dados (somente na primeira vez)
     > python banco.py

   - Etapa 2: abrir o sistema
     > python tela_login.py

3. O sistema será aberto somente após o login válido.

-------------------------------------------
📁 ESTRUTURA DE ARQUIVOS
-------------------------------------------
- banco.py .......... Criação do banco SQLite e tabelas
- tela_login.py ..... Tela inicial de login
- main.py ............ Menu principal e controle das telas
- produtos.py ........ Cadastro de produtos
- movimentacoes.py ... Registro de entradas e saídas
- usuarios.py ........ Gerenciamento de usuários (admin)
- relatorio.py ....... Relatório financeiro mensal
- estoque.db ......... Arquivo do banco de dados SQLite (gerado automaticamente)

-------------------------------------------
🛠️ OBSERVAÇÕES
-------------------------------------------
- Senhas são armazenadas com criptografia SHA-256
- Usuários comuns não podem acessar nem excluir outros usuários
- Caso deseje redefinir o banco, delete 'estoque.db' e rode 'banco.py' novamente
