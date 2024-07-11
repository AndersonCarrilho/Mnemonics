import random
from mnemonic import Mnemonic
from multiprocessing import Pool

# Lista de idiomas suportados pela biblioteca mnemonic
supported_languages = Mnemonic.list_languages()

def generate_mnemonics(language, mnemonic_types):
    m = Mnemonic(language)
    mnemonics = []
    
    for mnemonic_type in mnemonic_types:
        if mnemonic_type == '12':
            words_count = '12 words'
            strength = 128
        elif mnemonic_type == '18':
            words_count = '18 words'
            strength = 192
        elif mnemonic_type == '24':
            words_count = '24 words'
            strength = 256
        
        for word in m.wordlist:
            # Garantir que a palavra comece com uma letra do alfabeto
            first_letter = word[0].lower()
            if first_letter not in 'abcdefghijklmnopqrstuvwxyz':
                continue
            
            prefix = f"{word} "
            # Gerar o restante das palavras aleatoriamente
            random_suffix = m.generate(strength)
            mnemonic = prefix + ' '.join(random_suffix.split()[1:])  # Remover a primeira palavra (palavra inicial)
            mnemonics.append(mnemonic)
    
    return mnemonics

def ask_mnemonic_types():
    while True:
        print("Qual tipo de mnemônico você deseja gerar?")
        print("1. Mnemônicos de 12 palavras")
        print("2. Mnemônicos de 18 palavras")
        print("3. Mnemônicos de 24 palavras")
        print("4. Todos os tipos (12, 18 e 24 palavras)")
        choice = input("Digite o número da opção desejada (1/2/3/4): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                return ['12']
            elif choice == '2':
                return ['18']
            elif choice == '3':
                return ['24']
            elif choice == '4':
                return ['12', '18', '24']
        else:
            print("Opção inválida. Por favor, escolha uma das opções disponíveis.")

if __name__ == '__main__':
    # Número de processos a serem usados (pode ajustar conforme necessário)
    num_processes = len(supported_languages)
    
    # Perguntar ao usuário quais tipos de mnemônicos gerar
    mnemonic_types = ask_mnemonic_types()
    
    # Usar Pool de processos para gerar mnemônicos para cada idioma
    with Pool(num_processes) as pool:
        results = pool.starmap(generate_mnemonics, [(lang, mnemonic_types) for lang in supported_languages])
    
    # Exibir resultados
    for result in results:
        for mnemonic in result:
            print(mnemonic)
        print("=" * 20)  # Separador entre idiomas
