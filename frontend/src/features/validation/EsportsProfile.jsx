import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { validateEsportsProfile, addEsportsProfile, getUserEsportsProfiles } from '../../services/validationAPI';
import EsportsGames from '../../components/esports_profile/EsportsGames';
import ProfileCard from '../../components/esports_profile/ProfileCard';
import cs2StatsMock from './cs2StatsMock';
import profileAnalysisMock from './profileAnalysisMock';
import "./esports_profile.css"
import gamesMock from './gamesMock';

const EsportsProfile = () => {
  console.log("EsportsProfile - Componente renderizado"); 

  const { user } = useAuth();
  const [profileValidation, setProfileValidation] = useState([]);
  const [fetchingProfiles, setFetchingProfiles] = useState(false);

  // Carregar perfis existentes do usuário
  useEffect(() => {
    console.log("EsportsProfile - Usuário recebido do AuthProvider:", user); // Log para depuração
    if (user && user._id) {
      console.log("EsportsProfile - ID do usuário encontrado:", user._id); // Log para depuração
      fetchUserProfiles();
    } else {
      console.warn("EsportsProfile - ID do usuário está undefined ou user é null."); // Log para depuração
    }
  }, [user]);

  const fetchUserProfiles = async () => {
    try {
      console.log("EsportsProfile - Buscando perfis para o ID do usuário:", user._id); // Log para depuração
      setFetchingProfiles(true);
      const profiles = await getUserEsportsProfiles(user._id);
      const validation = await validateEsportsProfile(profiles, user._id);

      setProfileValidation(validation);
      console.log("EsportsProfile - validation:", profileValidation); // Log para depuração
      
    } catch (err) {
      console.error('Error fetching user profiles:', err);
    } finally {
      setFetchingProfiles(false);
    }
  };

  return (
    <div className='esports_profile_root'>
      {profileValidation?.profile_data ? (
        <>
          <ProfileCard
            profileUrl={profileValidation.profile_data.avatar}
            nickname={profileValidation.profile_data.nickname}
            stats={profileValidation.profile_data.cs2_stats}
            profileAnalysis={profileValidation.relevance}
          />
          <EsportsGames
            games={profileValidation.profile_data.esports_games}
          />
        </>
      ) : (
        <p className='loading'>Carregando...</p> // opcional, para mostrar enquanto não tem dados
      )}
    </div>
  );
};

export default EsportsProfile;