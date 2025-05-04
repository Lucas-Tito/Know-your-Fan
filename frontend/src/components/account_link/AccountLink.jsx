import React from 'react';
import './account_link.css';
import LinkAccountBtn from '../link_account_btn/LinkAccountBtn';
import bluesky_logo from '../../assets/bluesky_logo.png'; // Caminho para a imagem local
import steam_logo from '../../assets/steam_logo.png'; // Caminho para outra imagem local


const AccountLink = () => {
  return (
    <div className="account-link-root">
        <LinkAccountBtn
            image={steam_logo} 
            title="Associar Conta Steam" 
            platform="steam"
        />
        <LinkAccountBtn
            image={bluesky_logo} 
            title="Associar Conta Bluesky" 
            platform="bluesky"
        />
    </div>
  );
};

export default AccountLink;
