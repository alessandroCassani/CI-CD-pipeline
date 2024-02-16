class CheckCredentials:
    def __init__(self, email, password, dipartimento):
        self.email = email
        self.password = password
        self.dipartimento = dipartimento

    def validate_credentials(self):
        return self.email == 'alessandro' and self.password == 'ciao' and self.dipartimento == 'informatica'

    def check_and_return_message(self):
        if self.validate_credentials():
            return "Credenziali corrette. Accesso consentito."
        else:
            return "Credenziali non valide. Accesso rifiutato."

    def test_valid_credentials():
        checker = CheckCredentials('alessandro', 'ciao', 'informatica')
        result = checker.check_and_return_message()
        # assert result == "Credenziali corrette. Accesso consentito."

        if result != "Credenziali corrette. Accesso consentito.":
            print("Le credenziali non sono valide. L'accesso è stato rifiutato.")
        else:
            print("Le credenziali sono valide. L'accesso è stato accettato.")

    def test_invalid_credentials():
        checker = CheckCredentials('paolo', 'prova', 'fisica')
        result = checker.check_and_return_message()
        #assert result == "Credenziali non valide. Accesso rifiutato."
        
        if result != "Credenziali non valide. Accesso rifiutato.":
            print("Le credenziali sono valide. L'accesso è stato accettato.")
        else:
            print("Le credenziali non sono valide. L'accesso è stato rifiutato.")


      