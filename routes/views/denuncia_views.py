"""
routes/views/denuncia_views.py
Vistas de denuncias (Frontend)
"""
from flask import Blueprint, render_template, session, redirect, url_for
from controladores.controlador_denuncia_carro import crear_denuncia_carro, validar_id_denuncia

denuncia_views_bp = Blueprint('denuncia_views', __name__)


def require_login(func):
    """Decorador para requerir login"""
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth_views.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@denuncia_views_bp.route('/pendientes')
@require_login
def denuncia_pendiente():
    """Página de denuncias pendientes"""
    return render_template('denuncias/denuncia_pendiente.html')


@denuncia_views_bp.route('/resueltas')
@require_login
def denuncia_resuelta():
    """Página de denuncias resueltas"""
    return render_template('denuncias/denuncia_resuelta.html')


@denuncia_views_bp.route('/rechazadas')
@require_login
def denuncia_rechazadas():
    """Página de denuncias rechazadas"""
    return render_template('denuncias/denuncia_rechazadas.html')


@denuncia_views_bp.route('/detalle/<id>')
@require_login
def detalle_denuncia(id):
    """Detalle de denuncia (sin edición)"""
    return render_template('denuncias/detalle_denuncia.html', id=id, vision=False)


@denuncia_views_bp.route('/detalle/<id>/editar')
@require_login
def detalle_denuncias(id):
    id_denuncia = validar_id_denuncia(id)
    if id_denuncia == 1:
        return render_template('denuncias/detalle_denuncia_carro.html')
    else:
        return render_template('denuncias/detalle_denuncia.html', id=id, vision=True)
        