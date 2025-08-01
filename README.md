# Computação Gráfica & Visão Computacional

## Organização dos códigos e Ambientes virtuais (venvs)

O repositório está organizado em pastas separadas para cada aula, facilitando o acesso ao conteúdo e exemplos de cada tema abordado.

- `aula-xx_x/`: Contém subpastas para cada aula, com códigos e materiais específicos.
- `aula-xx_x/venv`: deve ser criado um ambiente virtual Python para isolar as dependências do projeto.
- `aula-xx_xrequirements.txt`: Lista de todas as bibliotecas necessárias para executar os exemplos.

## Como preparar o ambiente para cada aula

1. Acesse a pasta correspondente à aula que deseja executar e siga os passos abaixo para preparar o ambiente.
   ```bash
   cd aula-xx_x
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
   
Pode ser necessário fechar e abrir o terminal novamente.

4. **Testanto o VENV:**

   ```bash
   which python
   ```
O comando deve retornar o caminho do interpretador python, e ele deve apontar para o VENV.
   
5. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Atualizando o requirements.txt:**

   Após instalar ou remover pacotes no ambiente virtual, atualize o arquivo `requirements.txt` com:

   ```bash
   pip freeze > requirements.txt
    ```

