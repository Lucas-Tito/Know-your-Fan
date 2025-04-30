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

- Python 3.8+
- Pandas e NumPy para análise de dados
- Matplotlib e Seaborn para visualizações
- HTML/CSS para interface do usuário
- APIs de redes sociais e plataformas de e-sports

### Instalação e Uso

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/know-your-fan-furia.git
cd know-your-fan-furia
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o notebook:
```bash
jupyter notebook know_your_fan_notebook.ipynb
```

4. Siga as instruções no notebook para preencher seus dados e gerar seu perfil

### Instalação no Ubuntu usando Conda

Se você estiver usando Ubuntu e encontrar problemas com a instalação padrão, recomendamos usar o Conda:

1. Instale o Miniconda:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
- Responda "yes" para aceitar os termos
- Confirme o local de instalação (ou altere se necessário)
- **Importante**: Quando perguntar se deseja inicializar o Miniconda3, responda "yes"

2. Feche e reabra o terminal, ou execute:
```bash
source ~/.bashrc
```

3. Verifique se o Conda está ativado:
```bash
conda --version
```
Se o comando não for reconhecido, ative o Conda manualmente:
```bash
source ~/miniconda3/bin/activate
```

4. Crie um ambiente Conda para o projeto:
```bash
conda create -n know_your_fan_env python=3.8
conda activate know_your_fan_env
```

5. Instale as dependências:
```bash
conda install pandas numpy matplotlib seaborn ipython jupyter pillow requests
```

6. Execute o notebook:
```bash
python know_your_fan_notebook.py
```

Esta abordagem evita problemas de compatibilidade com versões mais recentes do Python no Ubuntu.


### Estrutura do Projeto

- `know_your_fan_notebook.ipynb`: Notebook principal com toda a implementação
- `furia_fan_form.html`: Formulário para coleta de dados
- `fan_profile.html`: Relatório de perfil do fã
- `fan_profile_dashboard.png`: Dashboard com visualizações
- `README.md`: Documentação do projeto

### Demonstração

Assista ao vídeo de demonstração [aqui](#).
