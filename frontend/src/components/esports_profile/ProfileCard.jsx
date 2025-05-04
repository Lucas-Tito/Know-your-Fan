import React from 'react';
import './profile_card.css';

const formatTimePlayed = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    return `${hours}h`;
};

const ProfileCard = ({ profileUrl, nickname, stats, profileAnalysis }) => {
    const kills = stats?.cs2_stats?.basic_stats?.total_kills;
    const deaths = stats?.cs2_stats?.basic_stats?.total_deaths;
    const headshots = stats?.cs2_stats?.basic_stats?.total_kills_headshot;
    const kd = (kills / deaths).toFixed(2);
    const hsPercent = ((headshots / kills) * 100).toFixed(1);
    const matchesPlayed = stats?.cs2_stats?.basic_stats?.total_matches_played;
    const matchesWon = stats?.cs2_stats?.basic_stats?.total_matches_won;
    const winRate = ((matchesWon / matchesPlayed) * 100).toFixed(1);
    const timePlayed = formatTimePlayed(stats?.cs2_stats?.basic_stats?.total_time_played);

    const relevant = profileAnalysis?.relevance?.final_relevance;
    const confidence = profileAnalysis?.relevance?.ai_analysis?.confidence;
    const reason = profileAnalysis?.relevance?.ai_analysis?.reason;

    console.log("oi"+relevant);
    
    return (
        <div className="card">
            <img src={profileUrl} alt="profile" className="avatar" />
            <h2 className="nickname">{nickname}</h2>
            <div className='profile-info'>
                <div className='profile-info-section'>
                    <h3>Relevância do Conteúdo</h3>
                    <div className="stats">
                        <div><span className="label">Relevância:</span> {relevant.toString()}</div>
                        <div><span className="label">Confiança:</span> {confidence.toString()}</div>
                        <div><span className="label">Motivo:</span> {reason}</div>
                    </div>
                </div>
                <div className='profile-info-section'>
                    <h3>Stats</h3>
                    <div className="stats">
                        <div><span className="label">K/D:</span> {kd}</div>
                        <div><span className="label">HS%:</span> {hsPercent}%</div>
                        <div><span className="label">Partidas:</span> {matchesPlayed}</div>
                        <div><span className="label">winRate:</span> {winRate}%</div>
                        <div><span className="label">Tempo:</span> {timePlayed}</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfileCard;
