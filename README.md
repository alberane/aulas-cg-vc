# Computação Gráfica & Visão Computacional

## Organização do Conteúdo e dos Projetos

O repositório está organizado em pastas separadas para cada aula, facilitando o acesso ao conteúdo e exemplos de cada tema abordado.

- `aula_xx/`: Contém subpastas para cada aula, com códigos e materiais específicos.
- `aula_xx/venv`: deve ser criado um ambiente virtual Python para isolar as dependências do projeto.
- `aula_xx/requirements.txt`: Lista de todas as bibliotecas necessárias para executar os exemplos.

## Como preparar o ambiente para cada aula

1. Acesse a pasta correspondente à aula que deseja executar e siga os passos abaixo para preparar o ambiente.
   ```bash
   cd aula_xx
   ```

2. **Crie o ambiente virtual (caso ainda não exista):**
   ```bash
   python3 -m venv venv
   ```
   
3. **Ative o ambiente virtual:**
    - No Windows:
    ```bash
    venv\Scripts\activate
    ```
    - No Linux/Mac:
    ```bash
    source venv/bin/activate
    ```
   
4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   
