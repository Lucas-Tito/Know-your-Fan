
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from IPython.display import display, HTML, Image
from datetime import datetime

# Criar um formulário HTML para coleta de dados
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>FURIA - Know Your Fan</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #2a2a2a;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header img {
            width: 200px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #444;
            background-color: #333;
            color: white;
            border-radius: 5px;
        }
        .btn {
            background-color: #ff5500;
            color: white;
            border: none;
            padding: 12px 20px;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
            width: 100%;
            margin-top: 20px;
        }
        .btn:hover {
            background-color: #ff7700;
        }
        .section-title {
            border-bottom: 2px solid #ff5500;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
        }
        .checkbox-item {
            width: 50%;
            margin-bottom: 10px;
        }
        .checkbox-item input {
            width: auto;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://furia.gg/wp-content/uploads/2022/09/logo-furia-branco.png" alt="FURIA Logo">
            <h1>Know Your Fan</h1>
            <p>Ajude-nos a conhecer você melhor e receba experiências exclusivas!</p>
        </div>

        <h2 class="section-title">Dados Pessoais</h2>
        <div class="form-group">
            <label for="name">Nome Completo</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="form-group">
            <label for="email">E-mail</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="form-group">
            <label for="cpf">CPF</label>
            <input type="text" id="cpf" name="cpf" required>
        </div>

        <div class="form-group">
            <label for="birthdate">Data de Nascimento</label>
            <input type="date" id="birthdate" name="birthdate" required>
        </div>

        <div class="form-group">
            <label for="address">Endereço Completo</label>
            <textarea id="address" name="address" rows="3" required></textarea>
        </div>

        <div class="form-group">
            <label for="phone">Telefone</label>
            <input type="tel" id="phone" name="phone" required>
        </div>

        <h2 class="section-title">Seus Interesses</h2>
        <div class="form-group">
            <label>Quais jogos você acompanha?</label>
            <div class="checkbox-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="csgo" name="games" value="csgo">
                    <label for="csgo">CS:GO / CS2</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="valorant" name="games" value="valorant">
                    <label for="valorant">Valorant</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="lol" name="games" value="lol">
                    <label for="lol">League of Legends</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="dota2" name="games" value="dota2">
                    <label for="dota2">Dota 2</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="r6" name="games" value="r6">
                    <label for="r6">Rainbow Six Siege</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="apex" name="games" value="apex">
                    <label for="apex">Apex Legends</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="fortnite" name="games" value="fortnite">
                    <label for="fortnite">Fortnite</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="other" name="games" value="other">
                    <label for="other">Outros</label>
                </div>
            </div>
        </div>

        <div class="form-group">
            <label>Quais times da FURIA você acompanha?</label>
            <div class="checkbox-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="csgo_team" name="teams" value="csgo_team">
                    <label for="csgo_team">CS:GO / CS2</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="valorant_team" name="teams" value="valorant_team">
                    <label for="valorant_team">Valorant</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="lol_team" name="teams" value="lol_team">
                    <label for="lol_team">League of Legends</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="r6_team" name="teams" value="r6_team">
                    <label for="r6_team">Rainbow Six Siege</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="apex_team" name="teams" value="apex_team">
                    <label for="apex_team">Apex Legends</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="female_team" name="teams" value="female_team">
                    <label for="female_team">FURIA Feminina</label>
                </div>
            </div>
        </div>

        <div class="form-group">
            <label for="events">Eventos que você participou no último ano</label>
            <textarea id="events" name="events" rows="3" placeholder="Ex: Major Rio 2022, ESL Pro League, etc."></textarea>
        </div>

        <div class="form-group">
            <label for="purchases">Produtos da FURIA que você comprou no último ano</label>
            <textarea id="purchases" name="purchases" rows="3" placeholder="Ex: Camisa oficial, mousepad, etc."></textarea>
        </div>

        <h2 class="section-title">Redes Sociais</h2>
        <div class="form-group">
            <label for="instagram">Instagram</label>
            <input type="text" id="instagram" name="instagram" placeholder="@seu_usuario">
        </div>

        <div class="form-group">
            <label for="twitter">Twitter/X</label>
            <input type="text" id="twitter" name="twitter" placeholder="@seu_usuario">
        </div>

        <div class="form-group">
            <label for="twitch">Twitch</label>
            <input type="text" id="twitch" name="twitch" placeholder="seu_usuario">
        </div>

        <div class="form-group">
            <label for="discord">Discord</label>
            <input type="text" id="discord" name="discord" placeholder="seu_usuario#0000">
        </div>

        <h2 class="section-title">Perfis em Plataformas de E-sports</h2>
        <div class="form-group">
            <label for="faceit">FACEIT</label>
            <input type="text" id="faceit" name="faceit" placeholder="Link do seu perfil">
        </div>

        <div class="form-group">
            <label for="esea">ESEA</label>
            <input type="text" id="esea" name="esea" placeholder="Link do seu perfil">
        </div>

        <div class="form-group">
            <label for="gamersclub">GamersClub</label>
            <input type="text" id="gamersclub" name="gamersclub" placeholder="Link do seu perfil">
        </div>

        <div class="form-group">
            <label for="steam">Steam</label>
            <input type="text" id="steam" name="steam" placeholder="Link do seu perfil">
        </div>

        <h2 class="section-title">Upload de Documentos</h2>
        <div class="form-group">
            <label for="id_document">Documento de Identidade (RG ou CNH)</label>
            <input type="file" id="id_document" name="id_document">
        </div>

        <div class="form-group">
            <label for="selfie">Selfie para Verificação</label>
            <input type="file" id="selfie" name="selfie">
        </div>

        <button type="submit" class="btn">ENVIAR DADOS</button>
    </div>
</body>
</html>
"""

with open('furia_fan_form.html', 'w') as f:
    f.write(form_html)

print("Formulário HTML criado com sucesso: furia_fan_form.html")

# Função para validação de documentos com IA
def validate_document(document_image, selfie_image):
    # Em um cenário real, usaríamos uma API de reconhecimento facial
    # como AWS Rekognition, Azure Face API ou Google Cloud Vision

    # Simulação de validação
    validation_result = {
        "document_valid": True,
        "face_match": True,
        "confidence_score": 0.95,
        "verification_timestamp": datetime.now().isoformat()
    }

    return validation_result

# Função para conexão com redes sociais
def connect_social_media(social_profiles):
    # Em um cenário real, usaríamos as APIs oficiais:
    # - Twitter API v2
    # - Instagram Graph API
    # - Twitch API
    # - Discord API

    # Simulação de dados coletados
    social_data = {
        "twitter": {
            "following_esports_accounts": ["FURIA", "MIBR", "TeamLiquid", "G2Esports"],
            "interactions_with_furia": 45,
            "esports_tweets_percentage": 0.68
        },
        "instagram": {
            "following_esports_accounts": ["furiagg", "fallen", "coldzera", "gaules"],
            "interactions_with_furia": 32,
            "esports_posts_percentage": 0.42
        },
        "twitch": {
            "subscribed_channels": ["furiatv", "gaules", "btsbrasiltv"],
            "watch_time_esports": 120,  # horas
            "favorite_categories": ["CS:GO", "Valorant", "Just Chatting"]
        }
    }

    return social_data

# Função para validação de perfis de e-sports
def validate_esports_profiles(profile_links):
    # Em um cenário real, faríamos web scraping ou usaríamos APIs:
    # - FACEIT API
    # - ESEA API
    # - GamersClub API (não oficial)
    # - Steam API

    # Simulação de dados validados
    profiles_data = {
        "faceit": {
            "valid": True,
            "level": 8,
            "elo": 2100,
            "matches": 1250,
            "favorite_game": "CS:GO"
        },
        "gamersclub": {
            "valid": True,
            "level": 20,
            "matches": 850,
            "favorite_maps": ["Mirage", "Inferno", "Nuke"]
        },
        "steam": {
            "valid": True,
            "games_owned": 48,
            "csgo_hours": 3200,
            "valorant_hours": 1200
        }
    }

    return profiles_data

# Criar visualizações e dashboard
# Simulação de dados de um fã
fan_data = {
    "personal_info": {
        "name": "João Silva",
        "email": "joao.silva@email.com",
        "cpf": "123.456.789-00",
        "birthdate": "1995-03-15",
        "address": "Rua das Flores, 123 - São Paulo, SP",
        "phone": "(11) 98765-4321"
    },
    "interests": {
        "games": ["CS:GO", "Valorant", "League of Legends"],
        "teams": ["FURIA CS:GO", "FURIA Valorant", "FURIA Feminina"],
        "events_attended": ["Major Rio 2022", "ESL Pro League Season 16", "BLAST Premier Spring Finals 2023"],
        "purchases": ["Camisa Oficial 2023", "Mousepad FURIA", "Boné FURIA"]
    },
    "social_media": {
        "twitter": {
            "username": "@joao_furia_fan",
            "following_esports_accounts": ["FURIA", "MIBR", "TeamLiquid", "G2Esports", "NaVi", "FalleN", "arT", "KSCERATO"],
            "interactions_with_furia": 45,
            "esports_tweets_percentage": 0.68
        },
        "instagram": {
            "username": "@joao_silva",
            "following_esports_accounts": ["furiagg", "fallen", "coldzera", "gaules", "mibr", "teamliquid"],
            "interactions_with_furia": 32,
            "esports_posts_percentage": 0.42
        },
        "twitch": {
            "username": "joao_silva_gaming",
            "subscribed_channels": ["furiatv", "gaules", "btsbrasiltv", "fallenINSIDER"],
            "watch_time_esports": 120,  # horas
            "favorite_categories": ["CS:GO", "Valorant", "Just Chatting"]
        }
    },
    "esports_profiles": {
        "faceit": {
            "valid": True,
            "level": 8,
            "elo": 2100,
            "matches": 1250,
            "favorite_game": "CS:GO"
        },
        "gamersclub": {
            "valid": True,
            "level": 20,
            "matches": 850,
            "favorite_maps": ["Mirage", "Inferno", "Nuke"]
        },
        "steam": {
            "valid": True,
            "games_owned": 48,
            "csgo_hours": 3200,
            "valorant_hours": 1200
        }
    },
    "document_verification": {
        "document_valid": True,
        "face_match": True,
        "confidence_score": 0.95,
        "verification_timestamp": "2023-10-15T14:30:45"
    },
    "engagement_score": 85  # Score de 0-100 baseado em todos os dados
}

# Criar visualizações
plt.figure(figsize=(15, 10))

# 1. Gráfico de barras para jogos acompanhados
plt.subplot(2, 2, 1)
games_hours = {
    "CS:GO": fan_data["esports_profiles"]["steam"]["csgo_hours"],
    "Valorant": fan_data["esports_profiles"]["steam"]["valorant_hours"],
    "League of Legends": 800,  # Valor simulado
    "Outros": 500  # Valor simulado
}
plt.bar(games_hours.keys(), games_hours.values(), color=["#ff5500", "#1a1a1a", "#3366cc", "#999999"])
plt.title("Horas de Jogo por Título")
plt.ylabel("Horas")
plt.xticks(rotation=45)

# 2. Gráfico de pizza para interações nas redes sociais
plt.subplot(2, 2, 2)
social_interactions = {
    "Twitter": fan_data["social_media"]["twitter"]["interactions_with_furia"],
    "Instagram": fan_data["social_media"]["instagram"]["interactions_with_furia"],
    "Twitch": 25  # Valor simulado
}
plt.pie(list(social_interactions.values()), labels=list(social_interactions.keys()), autopct="%1.1f%%", 
        colors=["#1DA1F2", "#C13584", "#6441A4"], startangle=90)
plt.title("Interações com FURIA nas Redes Sociais")

# 3. Gráfico de linha para atividade ao longo do tempo (simulado)
plt.subplot(2, 2, 3)
months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
engagement = [65, 70, 68, 75, 80, 85, 90, 88, 92, 85, 82, 85]  # Valores simulados
plt.plot(months, engagement, marker="o", linestyle="-", color="#ff5500")
plt.title("Engajamento ao Longo do Ano")
plt.ylabel("Nível de Engajamento")
plt.grid(True, linestyle="--", alpha=0.7)

# 4. Gráfico de radar para perfil do fã
plt.subplot(2, 2, 4)
categories = ["Jogos", "Eventos", "Compras", "Social Media", "Plataformas"]
values = [85, 70, 60, 90, 80]  # Valores simulados

# Criar gráfico de radar
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
values += values[:1]  # Fechar o polígono
angles += angles[:1]  # Fechar o polígono
categories += categories[:1]  # Fechar o polígono

ax = plt.subplot(2, 2, 4, polar=True)
ax.plot(angles, values, linewidth=2, linestyle="solid", color="#ff5500")
ax.fill(angles, values, color="#ff5500", alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
ax.set_ylim(0, 100)
ax.set_title("Perfil do Fã", y=1.1)

plt.tight_layout()
plt.savefig("fan_profile_dashboard.png")
print("Dashboard criado com sucesso: fan_profile_dashboard.png")

# Criar um relatório de perfil do fã
fan_profile_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Perfil do Fã - FURIA</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: white;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: #2a2a2a;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #ff5500;
            padding-bottom: 20px;
        }
        .header img {
            width: 200px;
            margin-bottom: 20px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section-title {
            border-bottom: 2px solid #ff5500;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        .info-row {
            display: flex;
            margin-bottom: 10px;
        }
        .info-label {
            font-weight: bold;
            width: 200px;
        }
        .info-value {
            flex: 1;
        }
        .tag {
            display: inline-block;
            background-color: #ff5500;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            margin-right: 5px;
            margin-bottom: 5px;
        }
        .score-container {
            background-color: #333;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-top: 30px;
        }
        .score {
            font-size: 48px;
            font-weight: bold;
            color: #ff5500;
        }
        .score-label {
            font-size: 18px;
            margin-top: 10px;
        }
        .dashboard {
            width: 100%;
            margin-top: 30px;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://furia.gg/wp-content/uploads/2022/09/logo-furia-branco.png" alt="FURIA Logo">
            <h1>Perfil do Fã</h1>
        </div>

        <div class="section">
            <h2 class="section-title">Dados Pessoais</h2>
            <div class="info-row">
                <div class="info-label">Nome:</div>
                <div class="info-value">João Silva</div>
            </div>
            <div class="info-row">
                <div class="info-label">E-mail:</div>
                <div class="info-value">joao.silva@email.com</div>
            </div>
            <div class="info-row">
                <div class="info-label">Data de Nascimento:</div>
                <div class="info-value">1995-03-15</div>
            </div>
            <div class="info-row">
                <div class="info-label">Endereço:</div>
                <div class="info-value">Rua das Flores, 123 - São Paulo, SP</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Interesses</h2>
            <div class="info-row">
                <div class="info-label">Jogos:</div>
                <div class="info-value">
                    <span class="tag">CS:GO</span><span class="tag">Valorant</span><span class="tag">League of Legends</span>
                </div>
            </div>
            <div class="info-row">
                <div class="info-label">Times:</div>
                <div class="info-value">
                    <span class="tag">FURIA CS:GO</span><span class="tag">FURIA Valorant</span><span class="tag">FURIA Feminina</span>
                </div>
            </div>
            <div class="info-row">
                <div class="info-label">Eventos Participados:</div>
                <div class="info-value">
                    <span class="tag">Major Rio 2022</span><span class="tag">ESL Pro League Season 16</span><span class="tag">BLAST Premier Spring Finals 2023</span>
                </div>
            </div>
            <div class="info-row">
                <div class="info-label">Compras:</div>
                <div class="info-value">
                    <span class="tag">Camisa Oficial 2023</span><span class="tag">Mousepad FURIA</span><span class="tag">Boné FURIA</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Redes Sociais</h2>
            <div class="info-row">
                <div class="info-label">Twitter:</div>
                <div class="info-value">@joao_furia_fan</div>
            </div>
            <div class="info-row">
                <div class="info-label">Instagram:</div>
                <div class="info-value">@joao_silva</div>
            </div>
            <div class="info-row">
                <div class="info-label">Twitch:</div>
                <div class="info-value">joao_silva_gaming</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Perfis de E-sports</h2>
            <div class="info-row">
                <div class="info-label">FACEIT:</div>
                <div class="info-value">Nível 8 | ELO: 2100</div>
            </div>
            <div class="info-row">
                <div class="info-label">GamersClub:</div>
                <div class="info-value">Nível 20 | 850 partidas</div>
            </div>
            <div class="info-row">
                <div class="info-label">Horas em CS:GO:</div>
                <div class="info-value">3200 horas</div>
            </div>
            <div class="info-row">
                <div class="info-label">Horas em Valorant:</div>
                <div class="info-value">1200 horas</div>
            </div>
        </div>

        <div class="score-container">
            <div class="score">85</div>
            <div class="score-label">Pontuação de Engajamento</div>
        </div>

        <div class="section">
            <h2 class="section-title">Dashboard</h2>
            <img src="fan_profile_dashboard.png" alt="Dashboard do Fã" class="dashboard">
        </div>
    </div>
</body>
</html>
"""

with open('fan_profile.html', 'w') as f:
    f.write(fan_profile_html)

print("Relatório de perfil do fã criado com sucesso: fan_profile.html")
print("Projeto 'Know Your Fan' executado com sucesso!")
print("Arquivos gerados:")
print("1. furia_fan_form.html - Formulário para coleta de dados")
print("2. fan_profile.html - Relatório de perfil do fã")
print("3. fan_profile_dashboard.png - Dashboard com visualizações")
