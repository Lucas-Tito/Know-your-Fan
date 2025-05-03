/**
 * API Service para validação de documentos e perfis de e-sports
 */

// Função para validar RG
export const validateRG = async (userId, documentFile) => {
  try {
    const formData = new FormData();
    formData.append('rg_document', documentFile);
    formData.append('user_id', userId);

    const response = await fetch('/validate-rg', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao validar RG');
    }

    return await response.json();
  } catch (error) {
    console.error('RG validation error:', error);
    throw error;
  }
};

// Função para verificar identidade
export const verifyIdentity = async (userId, documentFile, selfieFile) => {
  try {
    const formData = new FormData();
    formData.append('document', documentFile);
    formData.append('selfie', selfieFile);
    formData.append('user_id', userId);

    const response = await fetch('/verify-identity', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao verificar identidade');
    }

    return await response.json();
  } catch (error) {
    console.error('Identity verification error:', error);
    throw error;
  }
};

// Função para adicionar perfil de e-sports
export const addEsportsProfile = async (userId, profileData) => {
  try {
    const response = await fetch(`/users/${userId}/esports-profiles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profileData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao adicionar perfil de e-sports');
    }

    return await response.json();
  } catch (error) {
    console.error('Add esports profile error:', error);
    throw error;
  }
};

// Função para validar perfil de e-sports (sem associar a usuário)
export const validateEsportsProfile = async (profileUrl, userId = null) => {
  try {
    const url = userId 
      ? `/validate-esports-profile?user_id=${userId}`
      : '/validate-esports-profile';
      
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ profile_url: profileUrl })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao validar perfil de e-sports');
    }

    return await response.json();
  } catch (error) {
    console.error('Validate esports profile error:', error);
    throw error;
  }
};

// Função para obter perfis de e-sports do usuário
export const getUserEsportsProfiles = async (userId) => {
  try {
    const response = await fetch(`/users/${userId}/esports-profiles`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Erro ao obter perfis de e-sports');
    }

    return await response.json();
  } catch (error) {
    console.error('Get esports profiles error:', error);
    throw error;
  }
};