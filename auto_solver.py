import sys
import time
import database as db
import strategy
from utils import remove_accents


def compute_response(guess, solution):
    """Gera a resposta [0,1,2,...] comparando o chute com a solução real."""
    response = [0] * len(guess)
    solution_letters = list(solution)

    # 1a passada: acertos exatos (bit=1)
    for i, (g, s) in enumerate(zip(guess, solution)):
        if g == s:
            response[i] = 1
            solution_letters[i] = None

    # 2a passada: letra existe mas em posição errada (bit=2)
    for i, g in enumerate(guess):
        if response[i] == 1:
            continue
        if g in solution_letters:
            response[i] = 2
            solution_letters[solution_letters.index(g)] = None
        else:
            response[i] = 0

    return response


def auto_solve(solution, starter_word="serio"):
    solution = remove_accents(solution).lower()
    valid_solutions = db.UNACCENTED_VALID_SOLUTIONS

    for turn in range(1, 7):
        print(f"\nNumber of valid solutions: {len(valid_solutions)}...")

        start_time = time.time()
        if turn == 1:
            guess = starter_word
        else:
            guess = strategy.get_best_guess(
                valid_guesses=db.UNACCENTED_VALID_SOLUTIONS,
                valid_solutions=valid_solutions)
        elapsed_time = "{:.3f}".format(time.time() - start_time)
        print(f"Use guess: '{guess}'. (Time elapsed: {elapsed_time} seconds)")

        response = compute_response(guess, solution)
        print(f"Response: {response}")

        valid_solutions = strategy.filter_words_after_guess(
            words=valid_solutions,
            guess=guess,
            response=response)

        if len(valid_solutions) < 0:
            print(f"Possible solutions: {valid_solutions}")

        if response == [1, 1, 1, 1, 1]:
            print(f"\nFound solution '{guess}' after {turn} turns.")
            return turn

        if len(valid_solutions) == 0:
            print("\nNenhuma solução restante — algo deu errado (palavra fora da lista?).")
            return None

    print("\nNão resolveu em 6 tentativas.")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python auto_solver.py <palavra_solucao> [chute_inicial]")
        sys.exit(1)

    target = sys.argv[1]
    starter = sys.argv[2] if len(sys.argv) > 2 else "areio"
    auto_solve(target, starter)