import bcrypt

class Customer:
    def __init__(self,
                first_name,
                last_name,
                email,
                phone,
                address,
                username,
                encrypted_password=None,
                plain_password=None,
                id=None,last_login=None):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.phone=phone
        self.address=address
        self.username=username
        self.encrypted_password=encrypted_password
        self.plain_password=plain_password
        self.last_login=last_login

        if plain_password:
            self.encrypt_password()

    def __str__(self):
        return (f"Customer(id={self.id}, name='{self.first_name} {self.last_name}', "
                f"email='{self.email}', username='{self.username}', "
                f"last_login={self.last_login})")

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        
        if self.id is not None and other.id is not None:
            return self.id == other.id
        
        return self.email == other.email or self.username == other.username

    
    def encrypt_password(self):
        """Convierte la plain_password en un hash seguro."""
        if self.plain_password:
            # Generar un "salt" (semilla aleatoria)
            salt = bcrypt.gensalt()
            # Encriptar y guardar en el atributo correspondiente
            hashed = bcrypt.hashpw(self.plain_password.encode('utf-8'), salt)
            self.encrypted_password = hashed.decode('utf-8')
            # Por seguridad, limpiamos la contraseña plana después de encriptar
            self.plain_password = None

    def check_password(self, given_pass):
        """Compara una contraseña plana con el hash guardado."""
        if not self.encrypted_password:
            return False
        return bcrypt.checkpw(given_pass.encode('utf-8'), self.encrypted_password.encode('utf-8'))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "username": self.username,
            "last_login": self.last_login
        }
        