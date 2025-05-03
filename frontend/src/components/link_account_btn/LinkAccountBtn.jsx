import React, { useState } from 'react';
import './link_account_btn.css';

const LinkAccountBtn = ({ image, title, platform }) => {
  const [isModalOpen, setModalOpen] = useState(false);
  const [link, setLink] = useState('');

  const handleSubmit = async () => {
    const endpoint = platform === 'bluesky' ? '/api/link/bluesky' : '/api/link/steam';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link }),
      });

      if (!res.ok) {
        throw new Error('Erro ao enviar o link');
      }

      alert('Link enviado com sucesso!');
      setModalOpen(false);
      setLink('');
    } catch (err) {
      alert('Erro ao enviar o link: ' + err.message);
    }
  };

  return (
    <>
      <div className="dream-home-card" onClick={() => setModalOpen(true)} style={{ cursor: 'pointer' }}>
        <div className="external-link">&#8599;</div>
        <div className="icon-container">
          <div className="icon-circle">
            <img src={image} alt={title} className="icon-image" />
          </div>
          <p className="label">{title}</p>
        </div>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Insira o link da sua conta {platform}</h2>
            <input
              type="text"
              value={link}
              onChange={(e) => setLink(e.target.value)}
              placeholder="Cole o link aqui"
            />
            <div className="modal-actions">
              <button onClick={handleSubmit}>Enviar</button>
              <button onClick={() => setModalOpen(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default LinkAccountBtn;
