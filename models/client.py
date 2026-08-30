from datetime import datetime
import uuid

class Client:
    def __init__(self, first_name, last_name, email, phone):
        self.client_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.kyc_status = 'pending'
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_kyc(self, status):
        self.kyc_status = status
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'kyc_status': self.kyc_status
        }
