import { useState } from 'react';
import { useAuth } from '../auth/AuthProvider';

const DocumentUpload = () => {
  const { user } = useAuth();
  const [rgDocument, setRgDocument] = useState(null);
  const [identityDocument, setIdentityDocument] = useState(null);
  const [selfie, setSelfie] = useState(null);
  const [rgLoading, setRgLoading] = useState(false);
  const [identityLoading, setIdentityLoading] = useState(false);
  const [rgResult, setRgResult] = useState(null);
  const [identityResult, setIdentityResult] = useState(null);
  const [errors, setErrors] = useState({});

  const validateRG = async (e) => {
    e.preventDefault();
    setRgLoading(true);
    setErrors({});

    if (!rgDocument) {
      setErrors(prev => ({ ...prev, rg: 'Por favor, selecione um documento RG' }));
      setRgLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('rg_document', rgDocument);
    formData.append('user_id', user.id);

    try {
      const response = await fetch('/api/validate-rg', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setRgResult(result);
      
      if (!result.valid) {
        setErrors(prev => ({ ...prev, rg: 'Documento inválido ou não reconhecido' }));
      }
    } catch (error) {
      console.error('Error validating RG:', error);
      setErrors(prev => ({ ...prev, rg: 'Erro ao validar documento. Tente novamente.' }));
    } finally {
      setRgLoading(false);
    }
  };

  const verifyIdentity = async (e) => {
    e.preventDefault();
    setIdentityLoading(true);
    setErrors({});

    if (!identityDocument || !selfie) {
      setErrors(prev => ({ 
        ...prev, 
        identity: !identityDocument ? 'Selecione um documento' : 'Selecione uma selfie' 
      }));
      setIdentityLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('document', identityDocument);
    formData.append('selfie', selfie);
    formData.append('user_id', user.id);

    try {
      const response = await fetch('/verify-identity', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setIdentityResult(result);
      
      if (!result.face_match) {
        setErrors(prev => ({ ...prev, identity: 'Verificação falhou. Rosto não corresponde ao documento.' }));
      }
    } catch (error) {
      console.error('Error verifying identity:', error);
      setErrors(prev => ({ ...prev, identity: 'Erro ao verificar identidade. Tente novamente.' }));
    } finally {
      setIdentityLoading(false);
    }
  };

  const handleFileChange = (setter) => (e) => {
    if (e.target.files && e.target.files[0]) {
      setter(e.target.files[0]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* RG Validation */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Validação de Documento</h3>
          <form onSubmit={validateRG}>
            <div className="mb-4">
              <label className="block text-gray-700 mb-2">Upload do RG</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange(setRgDocument)}
                className="w-full p-2 border rounded"
              />
              {errors.rg && <p className="text-red-500 text-sm mt-1">{errors.rg}</p>}
            </div>
            
            <button
              type="submit"
              disabled={rgLoading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
            >
              {rgLoading ? 'Validando...' : 'Validar RG'}
            </button>
            
            {rgResult && (
              <div className={`mt-4 p-4 rounded ${rgResult.valid ? 'bg-green-100' : 'bg-red-100'}`}>
                <p className="font-medium">{rgResult.valid ? 'RG Validado com Sucesso!' : 'Validação Falhou'}</p>
                {rgResult.valid && rgResult.rg_number && (
                  <p className="text-sm mt-1">Número do RG: {rgResult.rg_number}</p>
                )}
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
