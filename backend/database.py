from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from passlib.context import CryptContext

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://mongodb:27017/')
        self.db = self.client['furia_fans']

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user_by_email(self, email):
        return self.db.users.find_one({"email": email})

    # Para criar usuário com senha hasheada (exemplo)
    def create_user(self, user_data):
        user_data["hashed_password"] = pwd_context.hash(user_data["password"])
        del user_data["password"]
        return self.db.users.insert_one(user_data)

    def save_user_data(self, user_data):
        return self.db.users.insert_one(user_data)

    def get_user_data(self, user_id):
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        return self.db.users.find_one({'_id': user_id})

    def update_user_data(self, user_id, new_data):
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        return self.db.users.update_one(
            {'_id': user_id},
            {'$set': new_data}
        )

    def get_all_users(self):
        """
        Retorna todos os usuários do banco de dados
        """
        users = list(self.db.users.find())
        # Converter ObjectId para string para serialização JSON
        for user in users:
            if '_id' in user:
                user['_id'] = str(user['_id'])
        return users

    def update_user_social_account(self, user_id, account_data):
        """
        Adiciona ou atualiza uma conta de rede social ao perfil do usuário
        """
        # Verificar se o usuário já tem essa plataforma vinculada
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        user = self.get_user_data(user_id)
        if not user:
            return False

        # Inicializar array de contas sociais se não existir
        if 'social_accounts' not in user:
            self.db.users.update_one(
                {'_id': user_id},
                {'$set': {'social_accounts': []}}
            )

        # Remover conta existente da mesma plataforma (se houver)
        self.db.users.update_one(
            {'_id': user_id},
            {'$pull': {'social_accounts': {'platform': account_data['platform']}}}
        )

        # Adicionar nova conta
        return self.db.users.update_one(
            {'_id': user_id},
            {'$push': {'social_accounts': account_data}}
        )

    def remove_user_social_account(self, user_id, platform):
        """
        Remove uma conta de rede social do perfil do usuário
        """
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass
        result = self.db.users.update_one(
            {'_id': user_id},
            {'$pull': {'social_accounts': {'platform': platform}}}
        )
        return result.modified_count > 0

    def get_user(self, user_id):
        """
        Obtém os dados de um usuário pelo ID
        """
        from bson.objectid import ObjectId

        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                pass

        return self.db.users.find_one({'_id': user_id})