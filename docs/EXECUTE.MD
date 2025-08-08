# Execução da aplicação 
## 🏃‍♂️ Execução do Projeto Inner
Para executar o projeto Inner, siga os passos abaixo:
1. **Instalar Dependências**:
   Certifique-se de que todas as dependências estão instaladas. Execute:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar Variáveis de Ambiente**:
    Crie um arquivo `.env` na raiz do projeto e adicione as variaveis de ambiente enviadas pelo whatsapp.
3. **Executar o Servidor**:
   Inicie o servidor com o comando:
   ```bash
   make run
   ```
4. **Acessar a Aplicação**:
   Abra o navegador e acesse `http://localhost:8000/docs`.

5. **Inicie o playground**:
    Execute o comando abaixo para iniciar o playground:
    ```bash
    make playground
    ```

   Acesse o playground em `http://localhost:3000` para interagir com os agentes.


## 🧪 Testes Automatizado
Para garantir a qualidade do código, o projeto utiliza testes automatizados. Siga os passos abaixo para executar os testes:
1. **Instalar Dependências de Teste**:
    Certifique-se de que as dependências de teste estão instaladas. Execute:
    ```bash
    pip install -r requirements-dev.txt
    ```

2. **Configurar Ambiente de Teste**:
    Certifique-se de que o ambiente virtual está ativado e o `PYTHONPATH` está configurado corretamente:
    ```bash
    export PYTHONPATH="$(pwd)/inner/src"
    ```

3. **Executar os Testes**:
    Utilize o comando abaixo para executar todos os testes:
    ```bash
    make test-coverage
    ```

4. **Verificar Cobertura de Testes**:
    Após a execução dos testes, você pode verificar a cobertura de código gerada. O relatório será salvo em `htmlcov/index.html`. Abra este arquivo no navegador para visualizar a cobertura de testes.


