# Sistema de Controle de Manutenção de Máquinas de Autoatendimento (SCMMA)

Repositório do SCMMA (Sistema de Controle de Manutenção de Máquinas de Autoatendimento), que é um sistema para abertura, gerenciamento e acompanhamento de chamados de suporte técnico para máquinas de autoatendimento de bilhetes de transporte.

Este projeto foi desenvolvido para a avaliação da disciplina **Software Product: Analysis, Specification, Project & Implementation** do curso de **Análise e Desenvolvimento de Sistemas** da **Faculdade Impacta**.	

## Ferramentas necessárias

1. [Python versão 3.10.6](https://www.python.org/downloads/release/python-3106/)
2. [Git](https://www.python.org/downloads/release/python-3106/)
3. Qualquer editor de texto, como o [Visual Studio Code](https://code.visualstudio.com/)

## Como usar este repositório em ambiente local

1. Baixar e instalar as ferramentas necessárias.
2. Abrir um terminal Linux ou o Windows Powershell no diretório onde deseja armazenar o projeto e digitar ``git clone https://github.com/LCavalini/scmma.git``.
3. Entrar no diretório do projeto: ``cd ./scmma``.
4. Criar um ambiente virtual: ``python -m venv venv`` (Windows) ou ``python3 -m venv venv`` (Linux).
5. Ativar o ambiente virtual: ``.\venv\Scripts\activate`` (Windows) ou ``source ./venv/bin/activate`` (Linux).
6. Instalar as dependências do projeto: ``pip install -r requirements.txt``.
7. Criar as migrações do banco de dados: ``python .\scmma\manage.py makemigrations chamados`` (Windows) ou ``python3 ./scmma/manage.py makemigrations chamados`` (Linux).
8. Alterar o banco de dados: ``python .\scmma\manage.py migrate`` (Windows) ou ``python3 ./scmma/manage.py migrate`` (Linux).
9. Criar o usuário administrador: ``python .\scmma\manage.py createsuperuser`` (Windows) ou ``python3 ./scmma/manage.py createsuperuser`` (Linux).
10. Registrar no seu email Google um app de terceiro com o nome ``scmma`` e criar uma senha, conforme instruções deste [link](https://support.google.com/accounts/answer/185833?hl=pt-BR).
11. Criar um arquivo de credenciais conforme a seção  [Como criar um arquivo de credenciais para envio de emails](#como-criar-um-arquivo-de-credenciais-para-envio-de-emails).
12. Testar a aplicação web em ambiente local: ``python .\scmma\manage.py runserver`` (Windows) ou ``python3 ./scmma/manage.py runserver`` (Linux).

## Como executar os testes automáticos

Digitar o comando abaixo no terminal:

``python .\scmma\manage.py test chamados\tests`` (Windows) ou ``python3 ./scmma/manage.py test chamados/tests`` (Linux).

## Como criar um arquivo de credenciais para envio de emails

1. Crie um arquivo com o nome ``credenciais.json`` no diretório ``scmma/scmma`` (onde se encontra o arquivo ``settings.py``).
2. Escreva no arquivo o conteúdo abaixo:


 ```
    {
        "EMAIL_HOST_USER": "SUBSTITUA PELO SEU E-MAIL DO DOMÍNIO GMAIL",
        "EMAIL_HOST_PASSWORD": "SUBSTITUA PELA SUA SENHA DE APP CRIADA"
    }
 ```