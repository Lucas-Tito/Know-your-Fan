# Know Your Fan - FURIA Esports

## Solução para coleta e análise de dados de fãs de e-sports

Este projeto implementa uma solução completa para o desafio "Know Your Fan", permitindo à FURIA conhecer melhor seus fãs e oferecer experiências personalizadas.

### Funcionalidades

- **Coleta de dados pessoais**: Formulário para coleta de informações básicas, interesses e preferências
- **Upload e validação de documentos**: Sistema de verificação de identidade com IA
- **Conexão com redes sociais**: Análise de interações e comportamento nas redes sociais
- **Validação de perfis de e-sports**: Integração com plataformas como FACEIT, GamersClub e Steam
- **Dashboard personalizado**: Visualização completa do perfil do fã

### Tecnologias Utilizadas

- Python 3.9+
- FastAPI para API REST
- MongoDB para armazenamento de dados
- Docker e Docker Compose para containerização
- Integração com APIs de redes sociais e plataformas de e-sports

### Instalação e Uso com Docker

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/know-your-fan-furia.git
cd know-your-fan-furia
```

2. Inicie os contêineres com Docker Compose:
```bash
docker-compose up -d
```

3. A aplicação estará disponível em `http://localhost:8000`

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

