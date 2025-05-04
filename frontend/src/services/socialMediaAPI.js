/**
 * API Service para integração com redes sociais
 */

// Função para vincular conta BlueSky
export const linkBlueskyAccount = async (userId, credentials) => {
  try {
    const response = await fetch(`/api/users/${userId}/bluesky`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao vincular conta BlueSky');
    }

    return await response.json();
  } catch (error) {
    console.error('BlueSky link error:', error);
    throw error;
  }
};

// Função para atualizar dados da conta BlueSky
export const updateBlueskyAccount = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}/bluesky/update`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao atualizar conta BlueSky');
    }

    return await response.json();
  } catch (error) {
    console.error('BlueSky update error:', error);
    throw error;
  }
};

// Função para desvincular conta de rede social
export const unlinkSocialAccount = async (userId, platform) => {
  try {
    const response = await fetch(`/api/users/${userId}/social-accounts/${platform}`, {
      method: 'DELETE'
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Erro ao desvincular conta ${platform}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Social account unlink error:', error);
    throw error;
  }
};

// Função para obter atividades de esports do usuário
export const getEsportsActivity = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}/esports-activity`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao obter atividades de esports');
    }

    return await response.json();
  } catch (error) {
    console.error('Get esports activity error:', error);
    throw error;
  }
};

// Função para obter dados do usuário
export const getUserData = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao obter dados do usuário');
    }

    return await response.json();
  } catch (error) {
    console.error('Get user data error:', error);
    throw error;
  }
};