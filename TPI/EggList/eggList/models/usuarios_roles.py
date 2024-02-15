from eggList import db

usuarios_roles = db.Table('usuarios_roles',
                          db.Column('usuario_id', db.Integer(), db.ForeignKey('usuarios.id', ondelete="CASCADE")),
                          db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
                          )
