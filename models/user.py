from database import db

"""
    A ideia dessa tabela é evitar que um usuário forje a mensagem de outro usuário.
    O servidor gravará o último token válido de login do usuário, assim quando o cliente
    mobile enviar a mensagem, o servidor validará e buscará através desse token. 
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, nullable=False)
    ra = db.Column(db.Text, nullable=False)
