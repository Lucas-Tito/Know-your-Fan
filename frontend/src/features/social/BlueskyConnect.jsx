import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { linkBlueskyAccount, updateBlueskyAccount, unlinkSocialAccount, getUserData } from '../../services/socialMediaAPI';

const BlueskyConnect = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [updateLoading, setUpdateLoading] = useState(false);
  const [unlinkLoading, setUnlinkLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [credentials, setCredentials] = useState({
    identifier: '',
    password: ''
  });
  const [linkedAccount, setLinkedAccount] = useState(null);

  useEffect(() => {
    // Verificar se o usuário já tem uma conta do Bluesky vinculada
    const fetchUserData = async () => {
      try {
        const userData = await getUserData(user.id);
        const blueskyAccount = userData.social_accounts?.find(
          account => account.platform === 'bluesky'
        );
        
        if (blueskyAccount) {
          setLinkedAccount(blueskyAccount);
        }
      } catch (err) {
        console.error('Error fetching user data:', err);
      }
    };

    if (user?.id) {
      fetchUserData();
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      // Remover @ do início do identificador, se presente
      const normalizedIdentifier = credentials.identifier.startsWith('@') 
        ? credentials.identifier.substring(1) 
        : credentials.identifier;

      const result = await linkBlueskyAccount(user.id, {
        identifier: normalizedIdentifier,
        password: credentials.password
      });

      if (result.status === 'success') {
        setMessage('Conta Bluesky vinculada com sucesso!');
        setCredentials({ identifier: '', password: '' });
        // Atualizar informações da conta vinculada
        const userData = await getUserData(user.id);
        const blueskyAccount = userData.social_accounts?.find(
          account => account.platform === 'bluesky'
        );
        setLinkedAccount(blueskyAccount);
      } else {
        setError(result.message || 'Falha ao vincular conta Bluesky');
      }
    } catch (err) {
      setError(err.message || 'Erro ao vincular conta Bluesky');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async () => {
    setUpdateLoading(true);
    setMessage('');
    setError('');

    try {
      const result = await updateBlueskyAccount(user.id);
      
      if (result.status === 'success') {
        setMessage('Dados da conta Bluesky atualizados com sucesso!');
        // Atualizar informações da conta vinculada
        const userData = await getUserData(user.id);
        const blueskyAccount = userData.social_accounts?.find(
          account => account.platform === 'bluesky'
        );
        setLinkedAccount(blueskyAccount);
      } else {
        setError(result.message || 'Falha ao atualizar dados da conta Bluesky');
      }
    } catch (err) {
      setError(err.message || 'Erro ao atualizar dados da conta Bluesky');
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleUnlink = async () => {
    setUnlinkLoading(true);
    setMessage('');
    setError('');

    try {
      const result = await unlinkSocialAccount(user.id, 'bluesky');
      
      if (result.status === 'success') {
        setMessage('Conta Bluesky desvinculada com sucesso!');
        setLinkedAccount(null);
      } else {
        setError(result.message || 'Falha ao desvincular conta Bluesky');
      }
    } catch (err) {
      setError(err.message || 'Erro ao desvincular conta Bluesky');
    } finally {
      setUnlinkLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Bluesky Connect</h2>

      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {message}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {linkedAccount ? (
        <div className="mb-6">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-lg mb-2">Conta vinculada</h3>
            <p className="mb-1"><strong>Handle:</strong> @{linkedAccount.handle}</p>
            {linkedAccount.display_name && (
              <p className="mb-1"><strong>Nome de exibição:</strong> {linkedAccount.display_name}</p>
            )}
            <p className="mb-1"><strong>Seguidores:</strong> {linkedAccount.followers_count}</p>
            <p className="mb-1"><strong>Seguindo:</strong> {linkedAccount.following_count}</p>
            
            {linkedAccount.esports_posts && (
              <div className="mt-3">
                <p className="font-semibold">Posts relacionados a e-sports: {linkedAccount.esports_posts.count}</p>
                {linkedAccount.esports_posts.sample && linkedAccount.esports_posts.sample.length > 0 && (
                  <div className="mt-2">
                    <p className="font-medium">Amostra de posts:</p>
                    <ul className="mt-1 list-disc pl-5">
                      {linkedAccount.esports_posts.sample.map((post, index) => (
                        <li key={index} className="text-sm text-gray-700">{post.text}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            
            <div className="mt-4 flex space-x-2">
              <button
                onClick={handleUpdate}
                disabled={updateLoading}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                {updateLoading ? 'Atualizando...' : 'Atualizar dados'}
              </button>
              
              <button
                onClick={handleUnlink}
                disabled={unlinkLoading}
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                {unlinkLoading ? 'Desvinculando...' : 'Desvincular conta'}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-700 mb-2">Identificador (handle ou email)</label>
            <input
              type="text"
              name="identifier"
              value={credentials.identifier}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded-lg"
              placeholder="@usuario ou email@exemplo.com"
              required
            />
          </div>
          
          <div>
            <label className="block text-gray-700 mb-2">Senha</label>
            <input
              type="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
          >
            {loading ? 'Conectando...' : 'Conectar conta Bluesky'}
          </button>
          
          <p className="text-sm text-gray-600 mt-2">
            Suas credenciais serão usadas apenas para autenticação e serão armazenadas com segurança.
          </p>
        </form>
      )}
    </div>
  );
};

export default BlueskyConnect;