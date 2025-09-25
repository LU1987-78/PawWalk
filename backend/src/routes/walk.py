from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.walk import Walk, WalkStatus
from src.models.walker import Walker
from src.models.review import Review
from src.models.payment import Payment, PaymentStatus
from datetime import datetime

walk_bp = Blueprint('walk', __name__)

@walk_bp.route('/walks', methods=['POST'])
def create_walk():
    """Criar uma nova solicitação de passeio"""
    try:
        data = request.get_json()
        
        # Converter strings de data para datetime
        data_hora_inicio = datetime.fromisoformat(data['data_hora_inicio'].replace('Z', '+00:00'))
        data_hora_fim_estimada = datetime.fromisoformat(data['data_hora_fim_estimada'].replace('Z', '+00:00'))
        
        walk = Walk(
            id_dono=data['id_dono'],
            id_passeador=data['id_passeador'],
            id_cachorro=data['id_cachorro'],
            data_hora_inicio=data_hora_inicio,
            data_hora_fim_estimada=data_hora_fim_estimada,
            local_encontro=data.get('local_encontro'),
            duracao_estimada=data.get('duracao_estimada'),
            preco_total=data['preco_total'],
            observacoes_dono=data.get('observacoes_dono'),
            status=WalkStatus.PENDING
        )
        
        db.session.add(walk)
        db.session.flush()  # Para obter o ID do passeio
        
        # Criar registro de pagamento
        payment = Payment(
            id_passeio=walk.id,
            id_dono=data['id_dono'],
            id_passeador=data['id_passeador'],
            valor=data['preco_total'],
            status=PaymentStatus.PENDING,
            metodo_pagamento=data.get('metodo_pagamento', 'cartao')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'walk': walk.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@walk_bp.route('/walks/<int:walk_id>', methods=['GET'])
def get_walk(walk_id):
    """Obter detalhes de um passeio"""
    try:
        walk = Walk.query.get_or_404(walk_id)
        
        return jsonify({
            'success': True,
            'walk': walk.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@walk_bp.route('/walks', methods=['GET'])
def get_walks():
    """Obter passeios de um usuário (dono ou passeador)"""
    try:
        user_id = request.args.get('user_id', type=int)
        user_type = request.args.get('user_type')  # 'owner' ou 'walker'
        
        if not user_id or not user_type:
            return jsonify({'success': False, 'error': 'user_id e user_type são obrigatórios'}), 400
        
        if user_type == 'owner':
            walks = Walk.query.filter_by(id_dono=user_id).all()
        elif user_type == 'walker':
            walks = Walk.query.filter_by(id_passeador=user_id).all()
        else:
            return jsonify({'success': False, 'error': 'user_type deve ser owner ou walker'}), 400
        
        return jsonify({
            'success': True,
            'walks': [walk.to_dict() for walk in walks]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@walk_bp.route('/walks/<int:walk_id>/status', methods=['PUT'])
def update_walk_status(walk_id):
    """Atualizar status de um passeio"""
    try:
        walk = Walk.query.get_or_404(walk_id)
        data = request.get_json()
        
        new_status = data.get('status')
        if not new_status:
            return jsonify({'success': False, 'error': 'Status é obrigatório'}), 400
        
        # Validar transições de status
        valid_statuses = [status.value for status in WalkStatus]
        if new_status not in valid_statuses:
            return jsonify({'success': False, 'error': 'Status inválido'}), 400
        
        walk.status = WalkStatus(new_status)
        
        # Se o passeio foi finalizado, registrar o horário
        if new_status == WalkStatus.COMPLETED.value:
            walk.data_hora_fim_real = datetime.utcnow()
            
            # Atualizar status do pagamento
            if walk.pagamento:
                walk.pagamento.status = PaymentStatus.PROCESSED
        
        # Adicionar observações do passeador se fornecidas
        if 'observacoes_passeador' in data:
            walk.observacoes_passeador = data['observacoes_passeador']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'walk': walk.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@walk_bp.route('/walks/<int:walk_id>/review', methods=['POST'])
def create_review():
    """Criar avaliação para um passeio"""
    try:
        walk_id = int(request.view_args['walk_id'])
        walk = Walk.query.get_or_404(walk_id)
        data = request.get_json()
        
        # Verificar se o passeio foi concluído
        if walk.status != WalkStatus.COMPLETED:
            return jsonify({'success': False, 'error': 'Passeio deve estar concluído para ser avaliado'}), 400
        
        # Verificar se já existe avaliação
        existing_review = Review.query.filter_by(id_passeio=walk_id).first()
        if existing_review:
            return jsonify({'success': False, 'error': 'Passeio já foi avaliado'}), 400
        
        review = Review(
            id_passeio=walk_id,
            id_dono=walk.id_dono,
            id_passeador=walk.id_passeador,
            nota=data['nota'],
            comentario=data.get('comentario', '')
        )
        
        db.session.add(review)
        
        # Atualizar média de avaliações do passeador
        walker = Walker.query.get(walk.id_passeador)
        if walker:
            reviews = Review.query.filter_by(id_passeador=walk.id_passeador).all()
            total_reviews = len(reviews) + 1  # +1 para incluir a nova avaliação
            total_rating = sum([r.nota for r in reviews]) + data['nota']
            walker.avaliacao_media = total_rating / total_reviews
            walker.numero_avaliacoes = total_reviews
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'review': review.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

