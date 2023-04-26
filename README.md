## Descrição das ativades e funcionalidades do sistemas proposto 

- O sistema foi desenvolvido utilizando Python no back-end, e para o front-end optei por não utilizar nenhum framework, utilizando HTML, CSS e JavaScript puro. O banco de dados escolhido foi o PostgreSQL.

- criei o banco de dados Sistema com a query 
Create Database Sistema 

- A estrutura do banco de dados foi criada através de migrações, que podem ser encontradas no projeto.

- Para iniciar, criei uma consulta diretamente no banco para cadastrar alguns usuários teste. Não utilizei padrões de segurança de senha, pois é um projeto para entrega rápida.


## Aqui estão as consultas iniciais:

INSERT INTO users (username, password) VALUES ('user1', 'pass1');

INSERT INTO users (username, password) VALUES ('user2', 'pass2');

INSERT INTO users (username, password) VALUES ('user3', 'pass3');

INSERT INTO users (username, password) VALUES ('user4', 'pass4');

Com isso, foram adicionados 4 usuários ao banco.

- As funcionalidades implementadas incluem tela de login, aviso de senha incorreta, confirmação ao assumir uma tarefa e botão para sair do sistema.

- Utilizei o Flask para o back-end em Python.

- No front-end, usei o Quill para definir os campos como Rich Text. Aqui está o link: https://cdn.quilljs.com/1.3.6

- A fonte utilizada no sistema foi a Nunito, disponível no Google Fonts: https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap


## Siga estas etapas para utilizar o sistema 

1 - Execute o arquivo migrate.py para inicializar e criar os dados no banco de dados.

2 - Insira a consulta SQL fornecida acima para adicionar usuários de teste.

3 - Execute o arquivo app.py para iniciar o sistema.


## Requisitos de sistema e software:

1 - Python 3.7 ou superior

2 - Flask 2.1.1 ou superior

3 - PostgreSQL 12 ou superior


## Instruções detalhadas de instalação e configuração:

1 - Instalar o Python 3.7 ou superior

2 - Instalar o PostgreSQL e criar um banco de dados para o projeto

3 - Clonar o repositório do projeto

4 - Criar um ambiente virtual Python e ativá-lo

5 - Configurar as variáveis de ambiente ou arquivo de configuração com as informações do banco de dados

6 - Executar o script migrate.py para criar as tabelas e estrutura do banco de dados

7 - Inserir a consulta inicial para adicionar os usuários de teste

8 - Executar o arquivo app.py para iniciar a aplicação

## Possíveis melhorias e próximos passos:

1 - Implementar um mecanismo de autenticação e autorização mais seguro, como OAuth ou JWT

2 - Aprimorar a interface do usuário e a experiência do usuário (UI/UX) com base no feedback dos usuários

3 - Adicionar funcionalidades de pesquisa e filtragem avançadas para melhorar a usabilidade do aplicativo

4 - Implementar recursos de notificação para alertar os usuários sobre atualizações de tarefas e observações

5 - Deixar o sistema responsivel para celulares

6 - Aprimorar a acessibilidade do sistema