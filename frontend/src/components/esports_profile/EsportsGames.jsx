import React from 'react';
import './esports_games.css'; 

const properties = [
  {
    title: 'cs2',
    image: 'http://media.steampowered.com/steamcommunity/public/images/apps/100/077b050ef3e89cd84e2c5a575d78d53b54058236.jpg',
    price: '128',
  },
  {
    title: 'cs2',
    image: 'http://media.steampowered.com/steamcommunity/public/images/apps/100/077b050ef3e89cd84e2c5a575d78d53b54058236.jpg',
    price: '128',
  },
  {
    title: 'cs2',
    image: 'http://media.steampowered.com/steamcommunity/public/images/apps/100/077b050ef3e89cd84e2c5a575d78d53b54058236.jpg',
    price: '128',
  },
  {
    title: 'cs2',
    image: 'http://media.steampowered.com/steamcommunity/public/images/apps/100/077b050ef3e89cd84e2c5a575d78d53b54058236.jpg',
    price: '128',
  },
];

export default function EsportsGames() {
  return (
    <div className="featured-section">
      <h2>Jogos Competitivos de -USERNAME-</h2>
      <div className="property-grid">
        {properties.map((prop, idx) => (
          <div className="property-card" key={idx}>
            <img src={prop.image} alt={prop.title} />
            <div className="property-card-content">
              <h3>{prop.title}</h3>
              <div className="property-footer">
                <strong>{prop.price}</strong>
              </div>
            </div>
          </div>
        ))}
      </div>
      <button className="btn-outline">Ver Todos os Jogos</button>
    </div>
  );
}
