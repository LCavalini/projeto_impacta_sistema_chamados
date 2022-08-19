# Sistema de Controle de Manutenção de Máquinas de Autoatendimento (SCMMA)

Repositório do SCMMA (Sistema de Controle de Manutenção de Máquinas de Autoatendimento), que é um sistema para abertura, gerenciamento e acompanhamento de chamados de suporte técnico para máquinas de autoatendimento de bilhetes de transporte.

Este projeto foi desenvolvido para a avaliação da disciplina **Software Product: Analysis, Specification, Project & Implementation** do curso de **Análise e Desenvolvimento de Sistemas** da **Faculdade Impacta**.	

## Ferramentas necessárias

1. [Python versão 3.10.6](https://www.python.org/downloads/release/python-3106/)
2. [Git](https://www.python.org/downloads/release/python-3106/)
3. Qualquer editor de texto, como o [Visual Studio Code](https://code.visualstudio.com/)

## Como usar este repositório em ambiente local

1. Baixar e instalar as ferramentas necessárias.
2. Abrir um terminal Linux ou o Windows Powershell no diretório desejado e digitar ``git clone https://github.com/LCavalini/scmma.git``.
3. Criar um ambiente virtual: ``python -m venv venv`` (Windows) ou ``python3 -m venv venv`` (Linux).
4. Ativar o ambiente virtual: ``.\venv\Scripts\activate`` (Windows) ou ``source ./venv/bin/activate`` (Linux).
5. Instalar as dependências do projeto: ``pip install -r requirements.txt``.
6. Testar a aplicação web em ambiente local: ``python ./scmma/manage.py runserver``