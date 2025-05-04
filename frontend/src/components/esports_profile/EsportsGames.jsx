import React from 'react';
import './esports_games.css'; 


export default function EsportsGames({ games }) {
  return (
    <div className="featured-section">
      <h2>Jogos Competitivos do Usuário</h2>
      <div className="property-grid">
        {games?.map((games, idx) => (
          <div className="property-card" key={idx}>
            <img src={games?.img_icon_url} alt={games?.name} />
            <div className="property-card-content">
              <h3>{games?.name}</h3>
              <div className="property-footer">
                <strong>{games?.playtime_hours}</strong>
              </div>
            </div>
          </div>
        ))}
      </div>
      <button className="btn-outline">Ver Todos os Jogos</button>
    </div>
  );
}
