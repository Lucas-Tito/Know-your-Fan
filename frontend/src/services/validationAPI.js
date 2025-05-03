// src/services/validationAPI.js
export const validateDocument = async (documentFile, selfieFile) => {
    const formData = new FormData();
    formData.append('document', documentFile);
    formData.append('selfie', selfieFile);
    
    const response = await fetch('/api/validate/document', {
      method: 'POST',
      body: formData
    });
    return response.json();
};