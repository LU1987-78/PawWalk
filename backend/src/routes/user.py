from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import db, User, UserType

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Obter lista de usuários"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Criar um novo usuário"""
    try:
        data = request.get_json()
        
        # Verificar se o email já existe
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        user = User(
            nome=data['nome'],
            email=data['email'],
            senha=generate_password_hash(data['senha']),
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            tipo_usuario=UserType(data.get('tipo_usuario', 'owner'))
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obter um usuário específico"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualizar um usuário"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'nome' in data:
            user.nome = data['nome']
        if 'telefone' in data:
            user.telefone = data['telefone']
        if 'endereco' in data:
            user.endereco = data['endereco']
        if 'senha' in data:
            user.senha = generate_password_hash(data['senha'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/auth/login', methods=['POST'])
def login():
    """Autenticar usuário"""
    try:
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.senha, data['senha']):
            return jsonify({
                'success': True,
                'user': user.to_dict(),
                'message': 'Login realizado com sucesso'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Email ou senha inválidos'
            }), 401
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

