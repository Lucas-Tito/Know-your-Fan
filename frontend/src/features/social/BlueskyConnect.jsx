// src/features/social/BlueskyConnect.jsx
import { useAuth } from '../auth/AuthProvider';
import { linkBlueskyAccount } from '../../services/socialMediaAPI';

function BlueskyConnect() {
  const { user } = useAuth();
  
  const handleConnect = async () => {
    const result = await linkBlueskyAccount({
      identifier: 'user@example.com',
      password: 'senha123'
    });
    
    if (result.status === 'success') {
      // Atualizar estado do usuário
    }
  };

  return <button onClick={handleConnect}>Conectar BlueSky</button>;
}