import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { validateEsportsProfile, addEsportsProfile, getUserEsportsProfiles } from '../../services/validationAPI';
import EsportsGames from '../../components/esports_profile/EsportsGames';
import ProfileCard from '../../components/esports_profile/ProfileCard';
import cs2StatsMock from './cs2StatsMock';
import profileAnalysisMock from './profileAnalysisMock';

const EsportsProfile = () => {
  console.log("EsportsProfile - Componente renderizado"); 

  const { user } = useAuth();
  const [profileUrl, setProfileUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [validationResult, setValidationResult] = useState(null);
  const [userProfiles, setUserProfiles] = useState([]);
  const [fetchingProfiles, setFetchingProfiles] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

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
      console.log("EsportsProfile - Perfis carregados:", profiles); // Log para depuração
      setUserProfiles(profiles);
    } catch (err) {
      console.error('Error fetching user profiles:', err);
    } finally {
      setFetchingProfiles(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setValidationResult(null);
    setSuccessMessage('');

    if (!profileUrl) {
      setError('Por favor, informe a URL do perfil de e-sports');
      setLoading(false);
      return;
    }

    try {
      // Primeiro validamos o perfil
      const validation = await validateEsportsProfile(profileUrl, user._id);
      setValidationResult(validation);

      if (validation.valid) {
        // Se for válido, adicionamos ao perfil do usuário
        const profileData = {
          profile_url: profileUrl,
          notes: notes
        };

        const result = await addEsportsProfile(user._id, profileData);
        if (result.valid) {
          setSuccessMessage('Perfil adicionado com sucesso!');
          setProfileUrl('');
          setNotes('');
          // Atualizar a lista de perfis
          fetchUserProfiles();
        }
      }
    } catch (err) {
      console.error('Error validating esports profile:', err);
      setError(err.message || 'Erro ao validar perfil de e-sports');
    } finally {
      setLoading(false);
    }
  };

  const getPlatformIcon = (platform) => {
    const icons = {
      'faceit': '🎮',
      'gamersclub': '🎯',
      'twitch': '📺',
      'esea': '🎲',
      'battlefy': '🏆',
      'challengermode': '🥇',
      'steam': '🎮',
      'discord': '💬',
      'default': '🎯'
    };

    return icons[platform?.toLowerCase()] || icons.default;
  };

  const getRelevanceColor = (relevance) => {
    if (!relevance || !relevance.score) return 'text-gray-500';
    
    const score = relevance.score;
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-green-500';
    if (score >= 40) return 'text-yellow-500';
    if (score >= 20) return 'text-orange-500';
    return 'text-red-500';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-8 text-center">Perfis de E-Sports</h2>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h3 className="text-xl font-semibold mb-4">Adicionar Novo Perfil</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="profileUrl" className="block text-gray-700 mb-2">
              URL do Perfil (Faceit, GamersClub, etc)
            </label>
            <input
              type="url"
              id="profileUrl"
              value={profileUrl}
              onChange={(e) => setProfileUrl(e.target.value)}
              placeholder="https://www.faceit.com/en/players/yourname"
              className="w-full p-2 border rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="notes" className="block text-gray-700 mb-2">
              Notas (opcional)
            </label>
            <textarea
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Adicione informações sobre este perfil..."
              className="w-full p-2 border rounded"
              rows="3"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            {loading ? 'Validando...' : 'Validar e Adicionar Perfil'}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
              {error}
            </div>
          )}

          {successMessage && (
            <div className="mt-4 p-4 bg-green-100 text-green-700 rounded">
              {successMessage}
            </div>
          )}

          {validationResult && (
            <div className="mt-4 p-4 bg-gray-100 rounded">
              <h4 className="font-medium mb-2">Resultado da Validação:</h4>
              
              {validationResult.valid ? (
                <div>
                  <p className="text-green-600 font-semibold">✓ Perfil Válido</p>
                  
                  {validationResult.profile_data && (
                    <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                      <div><span className="font-medium">Plataforma:</span> {validationResult.profile_data.platform}</div>
                      <div><span className="font-medium">Username:</span> {validationResult.profile_data.username || validationResult.profile_data.nickname}</div>
                      
                      {validationResult.profile_data.stats && (
                        <>
                          <div><span className="font-medium">Level/Rank:</span> {validationResult.profile_data.stats.level || validationResult.profile_data.stats.rank || 'N/A'}</div>
                          <div><span className="font-medium">Jogos:</span> {validationResult.profile_data.stats.games || 'N/A'}</div>
                          {validationResult.profile_data.stats.elo && (
                            <div><span className="font-medium">ELO:</span> {validationResult.profile_data.stats.elo}</div>
                          )}
                        </>
                      )}
                    </div>
                  )}
                  
                  {validationResult.relevance_analysis && (
                    <div className="mt-3 border-t pt-2">
                      <h5 className="font-medium">Análise de Relevância:</h5>
                      <div className={`font-semibold ${getRelevanceColor(validationResult.relevance_analysis)}`}>
                        Score: {validationResult.relevance_analysis.score || 'N/A'}/100
                      </div>
                      <p className="text-sm mt-1">{validationResult.relevance_analysis.summary}</p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-red-600">✗ Perfil Inválido: {validationResult.error}</p>
              )}
            </div>
          )}
        </form>
      </div>

      {/* Lista de perfis */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Seus Perfis de E-Sports</h3>
        
        {fetchingProfiles ? (
          <p className="text-center py-4">Carregando perfis...</p>
        ) : userProfiles.length > 0 ? (
          <div className="divide-y">
            {userProfiles.map((profile, index) => (
              <div key={index} className="py-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">{getPlatformIcon(profile.platform)}</span>
                    <div>
                      <h4 className="font-medium">{profile.username || 'Usuário'}</h4>
                      <a href={profile.profile_url} target="_blank" rel="noopener noreferrer" 
                         className="text-blue-600 text-sm hover:underline">
                        {profile.platform || 'Plataforma desconhecida'}
                      </a>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm ${getRelevanceColor(profile.relevance)}`}>
                    {profile.relevance?.score ? `${profile.relevance.score}/100` : 'N/A'}
                  </div>
                </div>
                
                {profile.validation_data?.stats && (
                  <div className="mt-2 grid grid-cols-3 gap-2 text-sm">
                    <div><span className="font-medium">Rank:</span> {profile.validation_data.stats.rank || profile.validation_data.stats.level || 'N/A'}</div>
                    <div><span className="font-medium">Jogos:</span> {profile.validation_data.stats.games || 'N/A'}</div>
                    {profile.validation_data.stats.elo && (
                      <div><span className="font-medium">ELO:</span> {profile.validation_data.stats.elo}</div>
                    )}
                  </div>
                )}
                
                {profile.notes && (
                  <div className="mt-2 text-sm bg-gray-50 p-2 rounded">
                    <span className="font-medium">Notas:</span> {profile.notes}
                  </div>
                )}
                
                <div className="mt-2 text-xs text-gray-500">
                  Validado em: {formatDate(profile.validated_at)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center py-4 text-gray-500">
            Você ainda não adicionou nenhum perfil de e-sports.
          </p>
        )}
      </div>

      <ProfileCard
        profileUrl="https://avatars.steamstatic.com/cbc9049654e4f66db4136d5e22c88c524da262ca_full.jpg"
        nickname="TitoPrkt"
        stats={cs2StatsMock}
        profileAnalysis={profileAnalysisMock}
      />
      <EsportsGames/>
    </div>
  );
};

export default EsportsProfile;