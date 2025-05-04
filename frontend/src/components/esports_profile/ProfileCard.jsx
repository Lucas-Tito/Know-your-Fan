import React from 'react';
import './profile_card.css';

const formatTimePlayed = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    return `${hours}h`;
};

const ProfileCard = ({ profileUrl, nickname, stats, profileAnalysis }) => {

    console.log("APIII", profileAnalysis);


    const kills = stats?.basic_stats?.total_kills;
    const deaths = stats?.basic_stats?.total_deaths;
    const headshots = stats?.basic_stats?.total_kills_headshot;
    const kd = (kills / deaths).toFixed(2);
    const hsPercent = ((headshots / kills) * 100).toFixed(1);
    const matchesPlayed = stats?.basic_stats?.total_matches_played;
    const matchesWon = stats?.basic_stats?.total_matches_won;
    const winRate = ((matchesWon / matchesPlayed) * 100).toFixed(1);
    const timePlayed = formatTimePlayed(stats?.basic_stats?.total_time_played);

    const relevant = profileAnalysis?.final_relevance;
    const confidence = profileAnalysis?.ai_analysis?.confidence;
    const reason = profileAnalysis?.ai_analysis?.reason;

    return (
        <>
            <div className="card">
                <img src={profileUrl} alt="profile" className="avatar" />
                <h2 className="nickname">{nickname}</h2>
                <div className='profile-info'>
                    <div className='profile-info-section'>
                        <h3>Relevância do Conteúdo</h3>
                        <div className="stats">
                            <div><span className="label_profile_card">Relevância:</span> {relevant?.toString()}</div>
                            <div><span className="label_profile_card">Confiança:</span> {confidence?.toString()}</div>
                        </div>
                    </div>
                    <div className='profile-info-section'>
                        <h3>Stats</h3>
                        <div className="stats">
                            <div><span className="label_profile_card">K/D:</span> {kd}</div>
                            <div><span className="label_profile_card">HS%:</span> {hsPercent}%</div>
                            <div><span className="label_profile_card">Partidas:</span> {matchesPlayed}</div>
                            <div><span className="label_profile_card">winRate:</span> {winRate}%</div>
                            <div><span className="label_profile_card">Tempo:</span> {timePlayed}</div>
                        </div>
                    </div>
                </div>
            </div>
            <span className="reason">{reason}</span>
        </>
    );
};

export default ProfileCard;
