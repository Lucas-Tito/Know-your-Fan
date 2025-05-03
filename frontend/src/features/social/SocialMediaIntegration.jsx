import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { getEsportsActivity, getUserData } from '../../services/socialMediaAPI';
import BlueskyConnect from './BlueskyConnect';

const SocialMediaIntegration = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activityData, setActivityData] = useState(null);
  const [socialAccounts, setSocialAccounts] = useState([]);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('connect'); // 'connect' ou 'activity'

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userData = await getUserData(user.id);
        if (userData.social_accounts) {
          setSocialAccounts(userData.social_accounts);
        }
      } catch (err) {
        console.error('Error fetching user social accounts:', err);
      }
    };

    if (user?.id) {
      fetchUserData();
    }
  }, [user]);

  const fetchEsportsActivity = async () => {
    setLoading(true);
    setError('');

    try {
      const activity = await getEsportsActivity(user.id);
      setActivityData(activity);
    } catch (err) {
      setError('Falha ao obter atividades de e-sports. Verifique se você tem contas vinculadas.');
      console.error('Error fetching esports activity:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'activity' && user?.id && socialAccounts.length > 0) {
      fetchEsportsActivity();
    }
  }, [activeTab, socialAccounts, user]);

  const renderEngagementLevel = (level) => {
    if (level === 'high') {
      return <span className="px-2 py-1 bg-green-100 text-green-800 rounded">Alto</span>;
    } else if (level === 'medium') {
      return <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">Médio</span>;
    } else {
      return <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded">Baixo</span>;
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-8 text-center">Integração com Redes Sociais</h2>
      
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="flex border-b">
          <button
            className={`flex-1 py-3 font-medium ${activeTab === 'connect' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700'}`}
            onClick={() => setActiveTab('connect')}
          >
            Conectar Redes Sociais
          </button>
          <button
            className={`flex-1 py-3 font-medium ${activeTab === 'activity' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700'}`}
            onClick={() => setActiveTab('activity')}
          >
            Atividades de E-sports
          </button>
        </div>
        
        <div className="p-6">
          {activeTab === 'connect' && (
            <div>
              <p className="text-gray-700 mb-6">
                Conecte suas redes sociais para que possamos analisar seu perfil como fã de e-sports
                e oferecer uma experiência personalizada.
              </p>
              
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-4">Redes Sociais Disponíveis</h3>
                <div className="grid grid-cols-1 gap-4">
                  <div className="border p-4 rounded-lg">
                    <h4 className="font-medium mb-2">Bluesky</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Conecte sua conta Bluesky para analisarmos posts relacionados a e-sports e times que você segue.
                    </p>
                    <div className="text-sm text-blue-600">
                      {socialAccounts.find(acc => acc.platform === 'bluesky') ? (
                        <span className="text-green-600">✓ Conectado</span>
                      ) : (
                        'Não conectado'
                      )}
                    </div>
                  </div>
                  
                  {/* Placeholder para futuras integrações */}
                  <div className="border p-4 rounded-lg bg-gray-50">
                    <h4 className="font-medium mb-2">Twitter (Em breve)</h4>
                    <p className="text-sm text-gray-500">
                      Em desenvolvimento. Conecte sua conta Twitter para analisarmos seu interesse em e-sports.
                    </p>
                  </div>
                </div>
              </div>
              
              <BlueskyConnect />
            </div>
          )}
          
          {activeTab === 'activity' && (
            <div>
              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                  {error}
                </div>
              )}
              
              {loading ? (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
                  <p className="mt-2 text-gray-600">Carregando atividades...</p>
                </div>
              ) : socialAccounts.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-gray-600">
                    Você ainda não possui contas de redes sociais vinculadas.
                    Por favor, conecte pelo menos uma conta para ver suas atividades.
                  </p>
                </div>
              ) : activityData ? (
                <div>
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-3">Resumo de Atividades</h3>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-gray-600">Nível de Engajamento</p>
                          <p className="mt-1">{renderEngagementLevel(activityData.engagement_level)}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Total de Interações</p>
                          <p className="mt-1 font-semibold">{activityData.interactions.total}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {Object.keys(activityData.favorite_orgs).length > 0 && (
                    <div className="mb-6">
                      <h3 className="text-lg font-semibold mb-3">Organizações Favoritas</h3>
                      <ul className="bg-gray-50 p-4 rounded-lg">
                        {Object.entries(activityData.favorite_orgs).map(([org, count]) => (
                          <li key={org} className="flex justify-between items-center py-2 border-b last:border-b-0">
                            <span className="font-medium capitalize">{org}</span>
                            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                              {count} {count === 1 ? 'menção' : 'menções'}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-3">Detalhes por Plataforma</h3>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      {Object.entries(activityData.interactions.by_platform).map(([platform, count]) => (
                        <div key={platform} className="flex justify-between items-center py-2 border-b last:border-b-0">
                          <span className="font-medium capitalize">{platform}</span>
                          <span className="text-gray-700">{count} interações</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <button
                    onClick={fetchEsportsActivity}
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                  >
                    Atualizar Atividades
                  </button>
                </div>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-600">
                    Não foi possível encontrar atividades de e-sports em suas redes sociais.
                    Isso pode acontecer se você não tiver interações relacionadas a e-sports recentemente.
                  </p>
                  <button
                    onClick={fetchEsportsActivity}
                    className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    Tentar Novamente
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SocialMediaIntegration;