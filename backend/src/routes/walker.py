from flask import Blueprint, request, jsonify
from src.models.user import db, User, UserType
from src.models.walker import Walker
from src.models.review import Review
from sqlalchemy import func

walker_bp = Blueprint('walker', __name__)

@walker_bp.route('/walkers', methods=['GET'])
def get_walkers():
    """Buscar passeadores com filtros opcionais"""
    try:
        # Parâmetros de filtro
        location = request.args.get('location')
        min_rating = request.args.get('min_rating', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Query base
        query = db.session.query(Walker).join(User)
        
        # Aplicar filtros
        if max_price:
            query = query.filter(Walker.preco_por_passeio <= max_price)
        
        if min_rating:
            query = query.filter(Walker.avaliacao_media >= min_rating)
        
        # TODO: Implementar filtro por localização quando tivermos coordenadas
        
        walkers = query.all()
        
        return jsonify({
            'success': True,
            'walkers': [walker.to_dict() for walker in walkers]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@walker_bp.route('/walkers/<int:walker_id>', methods=['GET'])
def get_walker(walker_id):
    """Obter detalhes de um passeador específico"""
    try:
        walker = Walker.query.get_or_404(walker_id)
        
        # Buscar avaliações recentes
        reviews = Review.query.filter_by(id_passeador=walker_id).limit(5).all()
        
        walker_data = walker.to_dict()
        walker_data['reviews'] = [review.to_dict() for review in reviews]
        
        return jsonify({
            'success': True,
            'walker': walker_data
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@walker_bp.route('/walkers', methods=['POST'])
def create_walker():
    """Criar perfil de passeador"""
    try:
        data = request.get_json()
        
        # Verificar se o usuário existe
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404
        
        # Verificar se já é um passeador
        existing_walker = Walker.query.get(data['user_id'])
        if existing_walker:
            return jsonify({'success': False, 'error': 'Usuário já é um passeador'}), 400
        
        # Criar perfil de passeador
        walker = Walker(
            id=data['user_id'],
            experiencia=data.get('experiencia', ''),
            descricao=data.get('descricao', ''),
            preco_por_passeio=data['preco_por_passeio'],
            disponibilidade=data.get('disponibilidade', {}),
            documentos_verificados=False
        )
        
        # Atualizar tipo do usuário
        user.tipo_usuario = UserType.WALKER
        
        db.session.add(walker)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'walker': walker.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@walker_bp.route('/walkers/<int:walker_id>', methods=['PUT'])
def update_walker(walker_id):
    """Atualizar perfil de passeador"""
    try:
        walker = Walker.query.get_or_404(walker_id)
        data = request.get_json()
        
        # Atualizar campos
        if 'experiencia' in data:
            walker.experiencia = data['experiencia']
        if 'descricao' in data:
            walker.descricao = data['descricao']
        if 'preco_por_passeio' in data:
            walker.preco_por_passeio = data['preco_por_passeio']
        if 'disponibilidade' in data:
            walker.disponibilidade = data['disponibilidade']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'walker': walker.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@walker_bp.route('/walkers/<int:walker_id>/reviews', methods=['GET'])
def get_walker_reviews(walker_id):
    """Obter avaliações de um passeador"""
    try:
        reviews = Review.query.filter_by(id_passeador=walker_id).all()
        
        return jsonify({
            'success': True,
            'reviews': [review.to_dict() for review in reviews]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

