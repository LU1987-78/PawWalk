from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.dog import Dog

dog_bp = Blueprint('dog', __name__)

@dog_bp.route('/dogs', methods=['GET'])
def get_dogs():
    """Obter cachorros de um usuário"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'success': False, 'error': 'user_id é obrigatório'}), 400
        
        dogs = Dog.query.filter_by(id_dono=user_id).all()
        
        return jsonify({
            'success': True,
            'dogs': [dog.to_dict() for dog in dogs]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dog_bp.route('/dogs', methods=['POST'])
def create_dog():
    """Cadastrar um novo cachorro"""
    try:
        data = request.get_json()
        
        dog = Dog(
            id_dono=data['id_dono'],
            nome=data['nome'],
            raca=data.get('raca'),
            idade=data.get('idade'),
            temperamento=data.get('temperamento'),
            observacoes=data.get('observacoes'),
            foto_url=data.get('foto_url')
        )
        
        db.session.add(dog)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'dog': dog.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@dog_bp.route('/dogs/<int:dog_id>', methods=['GET'])
def get_dog(dog_id):
    """Obter detalhes de um cachorro específico"""
    try:
        dog = Dog.query.get_or_404(dog_id)
        
        return jsonify({
            'success': True,
            'dog': dog.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dog_bp.route('/dogs/<int:dog_id>', methods=['PUT'])
def update_dog(dog_id):
    """Atualizar informações de um cachorro"""
    try:
        dog = Dog.query.get_or_404(dog_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'nome' in data:
            dog.nome = data['nome']
        if 'raca' in data:
            dog.raca = data['raca']
        if 'idade' in data:
            dog.idade = data['idade']
        if 'temperamento' in data:
            dog.temperamento = data['temperamento']
        if 'observacoes' in data:
            dog.observacoes = data['observacoes']
        if 'foto_url' in data:
            dog.foto_url = data['foto_url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'dog': dog.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@dog_bp.route('/dogs/<int:dog_id>', methods=['DELETE'])
def delete_dog(dog_id):
    """Excluir um cachorro"""
    try:
        dog = Dog.query.get_or_404(dog_id)
        
        db.session.delete(dog)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cachorro excluído com sucesso'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

