class UserEntity:
    def __init__(self, id, nombre,email,roles_id):
        self.id = id
        self.nombre = nombre
        self.email=email
        self.roles_id=roles_id
    @staticmethod
    def convertToUser(json):
        return UserEntity(
            id=json['id'],
            nombre=json['nombre'],
            email=json['email'],
            roles_id=json['roles_id']
        )
    def to_list(self):
        return [self.id, self.nombre, self.email]

    def __str__(self):
        return f"UserEntity(id={self.id}, nombre={self.nombre}, email={self.email}, roles_id={self.roles_id})"