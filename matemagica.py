import pygame
import random

# Inicializa o pygame
pygame.init()

# Inicializa o mixer para som
pygame.mixer.init()
print("Mixer init:", pygame.mixer.get_init())

# Carrega os sons (adicione esses arquivos na pasta do projeto)
som_correto = pygame.mixer.Sound("correto.wav")
som_errado = pygame.mixer.Sound("errado.wav")

# Configurações da tela (modo tela cheia em janela)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Jogo Educativo de Matemática")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

# Fontes
font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 60)

# Carrega imagem de fundo
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Função para gerar uma questão matemática
def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    display_operator = '×' if operator == '*' else operator
    question = f"{num1} {display_operator} {num2}"
    answer = eval(f"{num1} {operator} {num2}")
    return question, str(answer)

# Função para reiniciar o jogo
def reset_game():
    global question, correct_answer, user_answer, score, error_message
    question, correct_answer = generate_question()
    user_answer = ""
    score = 0
    error_message = ""

# Variáveis do jogo
question, correct_answer = generate_question()
user_answer = ""
score = 0
running = True
error_message = ""
show_title_screen = True

# Loop principal
while running:
    screen.blit(background, (0, 0))

    if show_title_screen:
        # Tela de título
        title_text = font.render("Matemática básica com GPT", True, BLUE)
        start_text = small_font.render("Pressione ENTER para começar", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                show_title_screen = False

    else:
        # Tela do jogo
        question_text = font.render(question, True, BLUE)
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, HEIGHT // 3))

        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
        pygame.draw.rect(screen, LIGHT_BLUE, input_box)

        user_text = font.render(user_answer, True, BLACK)
        text_rect = user_text.get_rect(center=input_box.center)
        screen.blit(user_text, text_rect)

        if error_message:
            error_text = small_font.render(error_message, True, RED)
            screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 1.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_answer == correct_answer:
                        som_correto.play()
                        score += 1
                        if score == 10:
                            running = False
                        else:
                            question, correct_answer = generate_question()
                            user_answer = ""
                            error_message = ""
                    else:
                        som_errado.play()
                        error_message = "Para tentar novamente, pressione a tecla R"
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.key == pygame.K_r:
                    reset_game()
                else:
                    if event.unicode.isdigit() or event.unicode == '-':
                        user_answer += event.unicode

    pygame.display.flip()

# Tela de Parabéns
screen.fill(YELLOW)
congrats_text = font.render("Parabéns! Você concluiu o jogo!", True, GREEN)
screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()