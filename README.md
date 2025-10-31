Monitor de Botijões - UPX 3

Aplicativo desktop em Python para registrar, acompanhar e finalizar botijões de gás, além de gerar gráficos de duração média.

🔹 Pré-requisitos

Antes de rodar o app, certifique-se de ter instalado:

Python 3.10 ou superior
Baixe em: https://www.python.org/downloads/

PostgreSQL (ou outro banco configurado) com a tabela botijoes e usuarios.

Bibliotecas Python necessárias:

pip install psycopg2-binary pandas matplotlib


Obs.: psycopg2-binary é necessário para conectar ao PostgreSQL.

🔹 Estrutura do Projeto
UPX3/
│
├── main_app.py          # Código principal do app (Tkinter)
├── botijao.py           # Funções de botijões
├── user.py              # Funções de usuário
├── db.py                # Conexão com banco de dados
├── README.md            # Este tutorial
└── ... outros arquivos

🔹 Configuração do Banco de Dados

No PostgreSQL, crie a tabela botijoes (exemplo):

CREATE TABLE botijoes (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    litragem VARCHAR(10) NOT NULL,
    empresa VARCHAR(50) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE
);


E a tabela usuarios:

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL
);


No arquivo db.py, configure sua conexão:

import psycopg2

def conectar():
    return psycopg2.connect(
        host="SEU_HOST",
        database="SEU_BANCO",
        user="SEU_USUARIO",
        password="SUA_SENHA"
    )

🔹 Como Rodar o App

Abra o terminal/cmd e navegue até a pasta do projeto:

cd C:\caminho\para\UPX3


Execute o app:

python main_app.py


A tela de login aparecerá. Você pode:

Fazer login com um usuário existente.

Criar um novo usuário pelo cadastro na mesma tela.

No menu principal, você pode:

Registrar novo botijão

Finalizar botijão (com recomendação de duração)

Acompanhar todos os botijões

Gerar gráfico de duração média por litragem

🔹 Observações Importantes

A litragem deve ser enviada como string (ex.: "5kg", "13kg"), para compatibilidade com o banco (VARCHAR(10)).

O formato de data é DD/MM/AAAA.

O app exibe mensagens informativas no próprio aplicativo, sem precisar abrir o terminal.

🔹 Bibliotecas Utilizadas

Tkinter
 → Interface gráfica

psycopg2-binary
 → Conexão PostgreSQL

pandas
 → Manipulação de dados

matplotlib
 → Gráficos de duração
