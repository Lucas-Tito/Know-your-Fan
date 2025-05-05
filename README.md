# Know Your Fan - FURIA Esports

## Solução para coleta e análise de dados de fãs de e-sports

Este projeto implementa uma solução completa para o desafio "Know Your Fan", permitindo à FURIA conhecer melhor seus fãs e oferecer experiências personalizadas.

### Funcionalidades

- **Coleta de dados pessoais**: Formulário para coleta de informações básicas, interesses e preferências
- **Upload e validação de documentos**: Sistema de verificação de identidade com IA usando AWS Rekognition
- **Conexão com redes sociais**: Análise de interações e comportamento nas redes sociais, incluindo integração com a API do BlueSky
- **Validação de perfis de e-sports**: Integração com plataformas como FACEIT, GamersClub e Steam
- **Dashboard personalizado**: Visualização completa do perfil do fã

### Tecnologias Utilizadas

- Python 3.9+.
- React.
- FastAPI para API REST.
- MongoDB para armazenamento de dados.
- Docker e Docker Compose para containerização.
- AWS IAM para verificação de documentos.
- JWT Auth.
- OpenRouter para integração com IA.

## Acesse o deploy pelo link abaixo:

https://know-your-fan-production.up.railway.app

### Instalação e Uso com Docker

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/know-your-fan-furia.git
cd know-your-fan-furia
```

2. Configure as credenciais AWS:
   - Crie um arquivo `.env` na raiz do projeto com suas credenciais AWS IAM:
   ```
   AWS_ACCESS_KEY_ID=sua_access_key_aqui
   AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
   AWS_REGION=us-east-1
   ```
   - Certifique-se de que o usuário IAM tenha permissões para o serviço Rekognition

3. Inicie os contêineres com Docker Compose:
```bash
docker-compose up -d
```

4. A aplicação estará disponível em `http://localhost:8000`

### Comandos Docker úteis

Para reiniciar completamente a aplicação (reconstruindo as imagens):
```bash
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

### Verificando se a aplicação está rodando

1. Verifique os logs dos contêineres:
```bash
docker-compose logs -f app
```

2. Acesse a documentação da API:
```
http://localhost:8000/docs
```

3. Faça uma requisição de teste:
```bash
curl -X POST "http://localhost:8000/submit-user-data" \
  -H "Content-Type: application/json" \
  -d '{"name":"Teste","email":"teste@example.com","cpf":"12345678900","birthdate":"1990-01-01","address":"Rua Teste, 123","phone":"11999999999","interests":["CSGO"],"teams":["FURIA"],"events":"","purchases":""}'
```

4. Verifique o status dos contêineres:
```bash
docker-compose ps
```

5. Verifique os dados no MongoDB:
```bash
docker exec -it $(docker ps -q --filter name=mongodb) mongosh
use furia_fans
db.users.find()
```

### Desenvolvimento local sem Docker

Se preferir desenvolver sem Docker, siga estas etapas:

1. Instale o MongoDB localmente
2. Instale as dependências Python:
```bash
cd backend
pip install -r requirements.txt
```
3. Execute a aplicação:
```bash
uvicorn app:app --reload
```

### Verificação de RG com AWS Rekognition

Este projeto utiliza o serviço AWS Rekognition para verificação de documentos de identidade (RG). O sistema:

- Detecta faces no documento
- Extrai texto usando OCR
- Valida o formato e conteúdo do RG

O Free Tier da AWS permite aproximadamente 2.500 verificações de RG por mês sem custo adicional durante os primeiros 12 meses.
