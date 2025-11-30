🧯 Monitor de Botijões – UPX 3

Integrantes: 
Felipe Hennri Leite Lobo
João Marcelo Ferreira
Jorge Martesi Júnior
Lauro Cesar Leandro Filho
Miguel Santana Cruz
Pedro Henrique Matieli Nogueira Cardoso

TÍTULO:
Monitoramento e Análise do Consumo de Gás Natural

Aplicativo desktop desenvolvido em Python para registrar, acompanhar e finalizar botijões de gás, auxiliando o usuário a monitorar o consumo e avaliar o desempenho de cada botijão ao longo do tempo.
O sistema também gera gráficos automáticos com base na duração de uso, permitindo identificar padrões de consumo e otimizar o uso doméstico.

⚙️ Tecnologias Utilizadas

Python 3.10+ – Linguagem principal do projeto

Tkinter – Interface gráfica desktop

PostgreSQL (Supabase) – Banco de dados relacional

psycopg2-binary – Conexão entre Python e PostgreSQL

pandas – Manipulação e análise de dados

matplotlib – Geração de gráficos de consumo

📁 Estrutura do Projeto
UPX3/
├── main_app.py       # Interface principal (Tkinter)
├── botijao.py        # Funções de registro, acompanhamento e finalização
├── user.py           # Funções de autenticação e cadastro de usuários
├── db.py             # Conexão com o banco de dados PostgreSQL
└── README.md         # Documentação do projeto

🗄️ Configuração do Banco de Dados

No PostgreSQL (ou Supabase), crie as tabelas abaixo:

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL
);

CREATE TABLE botijoes (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL,
    litragem VARCHAR(10) NOT NULL,
    empresa VARCHAR(50) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);


No arquivo db.py, configure sua conexão com o banco:

import psycopg2

def conectar():
    return psycopg2.connect(
        host="SEU_HOST",
        database="SEU_BANCO",
        user="SEU_USUARIO",
        password="SUA_SENHA"
    )

💻 Como Executar o Projeto

Instale as dependências:

pip install psycopg2-binary pandas matplotlib


Navegue até a pasta do projeto:

cd C:\caminho\para\UPX3


Execute o aplicativo:

python main_app.py


Funcionalidades disponíveis:

Login e cadastro de usuário

Registro de botijões (com litragem, empresa e data de início)

Finalização de botijões (com data final e cálculo automático de desempenho)

Acompanhamento completo de botijões

Geração de gráfico de duração média com Matplotlib

📅 Formatos e Regras

Data: DD/MM/AAAA → convertida automaticamente para formato do banco (AAAA-MM-DD).

Litragem: aceita valores numéricos, ex.: 5, 13, 20.

O aplicativo exibe todas as mensagens dentro da interface, sem depender do terminal.

👨‍💻 Integrantes do Grupo
RA / Nome Completo
235573	/ Miguel Santana Cruz
235834 / Lauro Cesar Leandro Filho
235104 / Felipe Henri Leite Lobo
235319 / Pedro Henrique M. N. Cardoso
240236	/ Jorge Martesi Júnior
235319 / João Marcelo Ferreira Cau
🧱 Histórico e Controle de Versão

O projeto foi desenvolvido colaborativamente via Git e GitHub, com commits individuais de cada integrante.

Cada atualização contemplou incrementos de funcionalidades, correções de integração e ajustes de interface.

As branches foram utilizadas para desenvolvimento modular (main_app, botijao, interface, database) e posterior integração na main.

🚀 Próximos Passos

Implementar notificações automáticas quando o consumo for atípico.

Criar relatórios mensais em PDF.

Disponibilizar uma versão web integrada à nuvem.
