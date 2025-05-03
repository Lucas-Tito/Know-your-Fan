import { useState } from 'react';
import { useAuth } from './AuthProvider';
import './login-form.css';

const LoginForm = () => {
  const [isLogin, setIsLogin] = useState(true); // Estado para alternar entre login e cadastro
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cpf: '',
    birthdate: '',
    address: '',
    phone: '',
    interests: [],
    teams: [],
    events: '',
    purchases: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        // Enviar login para backend
        const formBody = new URLSearchParams();
        formBody.append("username", formData.email);
        formBody.append("password", formData.password);
      
        const response = await fetch("http://localhost:8000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formBody.toString(),
        });
      
        const data = await response.json();
      
        if (response.ok) {
          login(data.access_token); // Ajuste seu contexto para aceitar token
        } else {
          setError("Falha ao fazer login. Por favor, tente novamente.");
        }
      } else {
        // Lógica para cadastro
        const response = await fetch('/submit-user-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.status === 'success') {
          login({ ...formData, id: data.id });
        } else {
          setError('Falha ao registrar usuário. Por favor, tente novamente.');
        }
      }
    } catch (err) {
      setError('Erro ao conectar ao servidor. Por favor, tente novamente mais tarde.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">
        {isLogin ? 'Login' : 'Cadastro de Fã de E-sports'}
      </h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
      {isLogin ? (
  <>
    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Email</label>
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Senha</label>
      <input
        type="password"
        name="password"
        value={formData.password || ''}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>
  </>
) : (
  <>
    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Nome Completo</label>
      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">CPF</label>
      <input
        type="text"
        name="cpf"
        value={formData.cpf}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Data de Nascimento</label>
      <input
        type="date"
        name="birthdate"
        value={formData.birthdate}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Endereço</label>
      <input
        type="text"
        name="address"
        value={formData.address}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Telefone</label>
      <input
        type="text"
        name="phone"
        value={formData.phone}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
        required
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Interesses</label>
      <input
        type="text"
        name="interests"
        value={formData.interests}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Times</label>
      <input
        type="text"
        name="teams"
        value={formData.teams}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Eventos</label>
      <input
        type="text"
        name="events"
        value={formData.events}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
      />
    </div>

    <div className="mb-4">
      <label className="block text-gray-700 mb-2">Compras</label>
      <input
        type="text"
        name="purchases"
        value={formData.purchases}
        onChange={handleChange}
        className="w-full px-3 py-2 border rounded-lg"
      />
    </div>
  </>
)}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          {loading ? 'Enviando...' : isLogin ? 'Entrar' : 'Cadastrar'}
        </button>
      </form>

      <div className="mt-4 text-center">
        <button
          type="button"
          onClick={() => setIsLogin(!isLogin)}
          className="text-blue-600 hover:underline"
        >
          {isLogin ? 'Não tem uma conta? Cadastre-se' : 'Já tem uma conta? Faça login'}
        </button>
      </div>
    </div>
  );
};

export default LoginForm;