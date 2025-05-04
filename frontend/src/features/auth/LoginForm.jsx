import { useState } from 'react';
import { useAuth } from './AuthProvider';
import './login-form.css';
import { useNavigate } from 'react-router-dom';
import loginArt from "../../assets/login_art.png"
import DocumentUpload from '../validation/DocumentUpload';


const LoginForm = () => {
  const navigate = useNavigate(); // Adicione o hook useNavigate
  const [isLogin, setIsLogin] = useState(true); // Estado para alternar entre login e cadastro
  const [currentSection, setCurrentSection] = useState(1); // Estado para controlar a seção atual
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
    purchases: '',
    password: ''
  });

  fetch('https://know-your-fan-production-c1f0.up.railway.app/users')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login, register } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: (name === "interests" || name === "teams") ? value.split(',').map(s => s.trim()) : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        // Chamar o método login do contexto
        await login(formData.email, formData.password);
        navigate('/dashboard'); // Redirecionar para o dashboard após login bem-sucedido
      } else {
        await register(formData);
      }
    } catch (err) {
      setError('Erro ao conectar ao servidor. Por favor, tente novamente mais tarde.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-container">
      {/* Contêiner da imagem */}
      <div className="image-container">
        <img
          src={loginArt}
          alt="E-sports Fan"
          className='login_art'
        />
      </div>

      {/* Contêiner do formulário */}
      <div className="form-container">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Bem vindo FURIOSO!
        </h2>

        <div className="toggle-container">
          <button
            className={`toggle-button ${isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(true)}
          >
            Login
          </button>
          <button
            className={`toggle-button ${!isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>


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
              {currentSection === 1 && (
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

                  <button
                    type="button"
                    onClick={() => setCurrentSection(2)}
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                  >
                    Próxima
                  </button>
                </>
              )}

              {currentSection === 2 && (
                <>
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

                  <button
                    type="button"
                    onClick={() => setCurrentSection(1)}
                    className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition duration-200 mb-2"
                  >
                    Voltar
                  </button>

                  <button
                    type="button"
                    onClick={() => setCurrentSection(3)}
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                  >
                    Próxima
                  </button>

                </>
              )}

              {currentSection === 3 && (
                <>

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

                  <button
                    type="button"
                    onClick={() => setCurrentSection(2)}
                    className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition duration-200 mb-2"
                  >
                    Voltar
                  </button>

                  <button
                    type="button"
                    onClick={() => setCurrentSection(4)}
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                  >
                    Próxima
                  </button>
                </>
              )}

              {currentSection === 4 && (
                <>

                  <DocumentUpload />

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

                  <button
                    type="button"
                    onClick={() => setCurrentSection(3)}
                    className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition duration-200 mb-2"
                  >
                    Voltar
                  </button>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
                  >
                    {loading ? 'Enviando...' : 'Cadastrar'}
                  </button>
                </>
              )}
            </>
          )}




          {isLogin ?
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-200"
            >
              {loading ? 'Enviando...' : isLogin ? 'Entrar' : 'Cadastrar'}
            </button>
            : ""

          }
        </form>
      </div>
    </div>
  );
};

export default LoginForm;