import cv2
import numpy as np
import math
import time
# Função para redimensionar a imagem mantendo a proporção
def resize(image, width=None, height=None):
    if width is None and height is None:
        return image
    elif width is None:
        r = height / image.shape[0]
        dim = (int(image.shape[1] * r), height)
    else:
        r = width / image.shape[1]
        dim = (width, int(image.shape[0] * r))

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Função para desenhar o texto em uma imagem
def draw_text(image, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    x, y = position
    text_position = (x, y + text_size[1])
    cv2.putText(image, text, text_position, font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Verifica se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Não foi possível abrir a webcam.")
    exit()

# Obtém as dimensões da tela
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calcula as dimensões das telas na grade
grid_width = screen_width // 2
grid_height = screen_height // 2

# Loop principal
while True:
    # Captura o frame da webcam
    ret, frame = cap.read()

    if not ret:
        print("Não foi possível capturar o quadro.")
        break

    # Redimensiona a imagem da webcam para a resolução desejada
    resized_frame = resize(frame, width=grid_width, height=grid_height)

    # Cria uma imagem preta para o canto superior esquerdo
    black_screen = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)


    # Desenha um círculo vazado no canto inferior esquerdo
    circle_radius = min(grid_width, grid_height) // 2
    circle_center = (grid_width // 2, grid_height // 2)
    cv2.circle(black_screen, circle_center, circle_radius, (0, 255, 0), 2)

    # Adiciona a linha que gira como um radar
    #angle = (360 * time.time()) % 360  # Ângulo da linha (varia ao longo do tempo)
    #line_length = circle_radius  # Comprimento da linha
    #end_point = (int(circle_center[0] + line_length * math.cos(math.radians(angle))),
                 #int(circle_center[1] + line_length * math.sin(math.radians(angle))))
    #cv2.line(black_screen, circle_center, end_point, (0, 255, 0), 2)

    vertical_line_start = (
        int(circle_center[0]),
        int(circle_center[1] - circle_radius)
    )
    vertical_line_end = (
        int(circle_center[0]),
        int(circle_center[1] + circle_radius)
    )

    cv2.line(black_screen, vertical_line_start, vertical_line_end, (0, 255, 0), 2)
    horizontal_line_length = circle_radius  # Comprimento da linha horizontal
    horizontal_line_angle = 0

    horizontal_line_start = (
        int(circle_center[0] - horizontal_line_length / 2 * math.cos(math.radians(horizontal_line_angle))),
        int(circle_center[1] - horizontal_line_length / 2 * math.sin(math.radians(horizontal_line_angle)))
    )
    horizontal_line_end = (
        int(circle_center[0] + horizontal_line_length / 2 * math.cos(math.radians(horizontal_line_angle))),
        int(circle_center[1] + horizontal_line_length / 2 * math.sin(math.radians(horizontal_line_angle)))
    )

    cv2.line(black_screen, horizontal_line_start, horizontal_line_end, (0, 255, 0), 2)

    # Cria uma imagem vazia para o canto superior direito
    empty_screen = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Desenha o texto nas telas inferior esquerda
    text1 = "Motor1"
    text2 = "Motor2"
    text3 = "Motor3"
    text4 = "Motor4"
    text_position = (20, 40)
    draw_text(empty_screen, text1, text_position)
    draw_text(empty_screen, text2, (text_position[0], text_position[1] + 40))
    draw_text(empty_screen, text3, (text_position[0], text_position[1] + 80))
    draw_text(empty_screen, text4, (text_position[0], text_position[1] + 120))

    # Redimensiona a
    resized_frame = resize(frame, width=grid_width, height=grid_height)

    # Aplica o filtro Canny na imagem da webcam
    # Aplica o filtro Canny na imagem da webcam
    edges = cv2.Canny(resized_frame, 100, 200)

    # Cria uma imagem preta para o fundo
    black_background = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Define as cores das bordas e do fundo
    green_color = (0, 0, 255)
    black_color = (0, 0, 0)

    # Preenche o fundo com a cor preta
    black_background[:] = black_color

    # Copia as bordas para a imagem final
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    edges_colored[edges != 0] = (0, 255, 0)

    # Cria a janela principal e combina as telas usando HConcat e VConcat
    top_row = np.hstack((black_screen, resized_frame))
    bottom_row = np.hstack((empty_screen, edges_colored))
    full_screen = np.vstack((top_row, bottom_row))

    # Redimensiona a janela para preencher a tela mantendo a proporção
    resized_screen = resize(full_screen, width=screen_width, height=screen_height)

    # Exibe a janela em tela cheia
    cv2.namedWindow("Grid Window", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Grid Window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Grid Window", resized_screen)
    #you need to be carefully with what you need, take care of them and put your risk on this device
    #actually i dont know what i have to do
    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()