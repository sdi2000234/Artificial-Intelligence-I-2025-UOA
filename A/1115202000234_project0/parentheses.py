def complete_parentheses(ekfrasi):
    stack = []  # gia na metraw poses aristeres tha xreistwe
    ekfrasi_oloklirwmeni = []  # telikh lista me tis swstes parentheseis
    
    # pername apo thn ekfrasi
    for token in ekfrasi:
        if token == ')':
            # gia kathe deksia parenthesi, bazoume mia aristeri sto swsto simio
            stack.append('(')
        ekfrasi_oloklirwmeni.append(token)
    
    # # prosthetw tis aristeres parenthesis apo to stack sto swsto simio
    while stack:
        ekfrasi_oloklirwmeni.insert(0, stack.pop())  # eisagwgi sthn arxh
    
    return ekfrasi_oloklirwmeni

# Example usage
ekfrasi = [1, '+', 2, ')', '*', 3, '-', 4, ')', '*', 5, '-', 6, ')', ')', ')']
print("Ekfrasi prin")
print(ekfrasi)
teliko_apotelesma = complete_parentheses(ekfrasi)
print("Ekfrasi meta")
print(teliko_apotelesma)
