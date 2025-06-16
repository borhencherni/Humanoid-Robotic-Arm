import pygame
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Robotic Arm Simulation ")
font = pygame.font.SysFont('Arial', 20)


# Colors
WHITE = (255, 255, 255)
BLUE = (0, 102, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (245, 245, 245)  # lighter gray for less prominent grid lines
BLACK = (0, 0, 0)

# Arm parameters in cm
L1_cm = 10
L2_cm = 12
scale = 10  # pixels per cm
L1 = L1_cm * scale
L2 = L2_cm * scale
origin = (400, 300)

# State
running = True
frozen = False
target_pos = (0, 0)
clicked_coords = None

clock = pygame.time.Clock()

# Inverse Kinematics
def inverse_kinematics(x, y):
    dx = x - origin[0]
    dy = y - origin[1]
    D = math.hypot(dx, dy)

    if D > L1 + L2:
        dx *= (L1 + L2) / D
        dy *= (L1 + L2) / D
        D = L1 + L2

    cos_theta2 = (dx**2 + dy**2 - L1**2 - L2**2) / (2 * L1 * L2)
    theta2 = math.acos(max(-1, min(1, cos_theta2)))
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(dy, dx) - math.atan2(k2, k1)

    return theta1, theta2

# Draw Grid and Axes
def draw_grid():
    for x in range(0, 800, 20):
        pygame.draw.line(screen, BLACK, (x, 0), (x, 600), 1)
    for y in range(0, 600, 20):
        pygame.draw.line(screen, BLACK, (0, y), (800, y), 1)

    # Axes numbering every 50 px
    for x in range(0, 800, 50):
        label = font.render(str(x - origin[0]), True, BLACK)
        screen.blit(label, (x, origin[1] + 5))
    for y in range(0, 600, 50):
        label = font.render(str(origin[1] - y), True, BLACK)
        screen.blit(label, (origin[0] + 5, y))

def draw_angle_display(theta1_deg, theta2_deg):
    # Draw the background rectangle
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 40, WIDTH, 40))

    # Create the text surface
    text_surface = font.render(f'θ1 = {theta1_deg:.2f}°, θ2 = {theta2_deg:.2f}°', True, BLACK)

    # Draw text
    screen.blit(text_surface, (10, HEIGHT - 30))



# Main loop
while running:
    screen.fill(WHITE)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            frozen = not frozen
            if frozen:
                target_pos = pygame.mouse.get_pos()
                clicked_coords = target_pos
            else:
                clicked_coords = None

    if frozen:
        tx, ty = target_pos
    else:
        tx, ty = pygame.mouse.get_pos()

    theta1, theta2 = inverse_kinematics(tx, ty)

    # Joint positions
    x1 = origin[0] + L1 * math.cos(theta1)
    y1 = origin[1] + L1 * math.sin(theta1)
    x2 = x1 + L2 * math.cos(theta1 + theta2)
    y2 = y1 + L2 * math.sin(theta1 + theta2)

    # Draw Arm
    pygame.draw.line(screen, BLUE, origin, (x1, y1), 8)
    pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 8)
    pygame.draw.circle(screen, GREEN, origin, 10)
    pygame.draw.circle(screen, GREEN, (int(x1), int(y1)), 10)
    pygame.draw.circle(screen, GREEN, (int(x2), int(y2)), 10)
    pygame.draw.circle(screen, BLACK, (int(tx), int(ty)), 5)

    # Convert angles from radians to degrees
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)

# Call the function to draw angle display
    draw_angle_display(theta1_deg, theta2_deg)


    # Show clicked coordinates in cm
    if clicked_coords:
        dx = (clicked_coords[0] - origin[0]) / scale
        dy = (origin[1] - clicked_coords[1]) / scale  # inverted y-axis
        coord_text = f"({dx:.1f} cm, {dy:.1f} cm)"
        label = font.render(coord_text, True, BLACK)
        screen.blit(label, (clicked_coords[0] + 10, clicked_coords[1] - 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
