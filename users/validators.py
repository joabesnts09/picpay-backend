from django.core.exceptions import ValidationError


def validate_cpf(value):
    cpf = ''.join([char for char in value if char.isdigit()])
    
    if len(cpf) != 11:
        raise ValidationError('invalid CPF.')
    
    
    if cpf == cpf[0] * 11:
        raise ValidationError('invalid CPF.')
    
    def calculate_digit(cpf, multipliers):
        soma = sum(
            int(cpf[i]) * multipliers[i]
            for i in range(len(multipliers))
        )
        
        resto = soma % 11
        
        return 0 if resto < 2 else 11 - resto
    
    
    first_multiplier = list(range(10, 1, -1))
    first_digit = calculate_digit(cpf, first_multiplier)
    
    
    second_multiplier = list(range(11, 1, -1))
    second_digit = calculate_digit(cpf, second_multiplier)
    
    if not (cpf[-2] == str(first_digit) and (cpf[-1]) == str(second_digit)):
        raise ValidationError('invalid CPF.')