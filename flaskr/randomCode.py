import random,string


class generarCodigo():
    def get_random_alphanumeric_string(lenght):
        letters_and_digits =  string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(lenght)))
        return result_str


