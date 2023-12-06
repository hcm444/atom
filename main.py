import pygame
import sys
import math


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bohr Model Simulation")


black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


proton_radius = 10
electron_radius = 5
electron_distances = [50, 75, 100, 125, 150, 175, 200]
max_electrons_per_ring = [2, 8, 8, 18, 18, 32, 32]
electron_angles = []
electron_ring_indices = []
electron_speed = 0.5
rotate_electron_rings = False


proton_position = [width // 2, height // 2]

font = pygame.font.Font(None, 36)

element_mapping = {}


with open("elements.txt", "r") as file:
    for line in file:
        elements = line.strip().split(',')
        if len(elements) == 5:
            number, name, symbol, protons, neutrons = elements
            atomic_mass = int(protons) + int(neutrons)
            element_mapping[int(number)] = {
                "name": name,
                "symbol": symbol,
                "protons": int(protons),
                "neutrons": int(neutrons),
                "atomic_mass": atomic_mass
            }

fixed_electrons_in_ring_1 = 2


electron_angles = []
electron_ring_indices = []
initial_electron_angles = []

def add_electrons_to_ring(ring_index, num_electrons):
    for _ in range(num_electrons):
        electron_angles.append(0)
        electron_ring_indices.append(ring_index)
        initial_electron_angles.append(0)


add_electrons_to_ring(0, fixed_electrons_in_ring_1)


for ring, max_electrons in enumerate(max_electrons_per_ring[1:]):
    add_electrons_to_ring(ring + 1, max_electrons)

clock = pygame.time.Clock()

def add_electron():
    if len(electron_angles) < sum(max_electrons_per_ring):
        for ring, max_electrons in enumerate(max_electrons_per_ring):
            if electron_ring_indices.count(ring) < max_electrons:
                initial_electron_angles.append(0)
                electron_angles.append(0)
                electron_ring_indices.append(ring)


                reset_initial_angles()
                return


def remove_electron():
    if electron_angles:
        electron_angles.pop()
        removed_ring = electron_ring_indices.pop()
        initial_electron_angles.pop()


        reset_initial_angles()


        for i in range(len(electron_ring_indices)):
            if electron_ring_indices[i] == removed_ring:
                electron_angles[i] = initial_electron_angles[i]
            elif electron_ring_indices[i] > removed_ring:
                electron_ring_indices[i] -= 1


def reset_initial_angles():
    for i in range(len(initial_electron_angles)):
        initial_electron_angles[i] = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                add_electron()
            elif event.key == pygame.K_a:
                remove_electron()
            elif event.key == pygame.K_w:
                rotate_electron_rings = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                rotate_electron_rings = False

    screen.fill(black)

    pygame.draw.circle(screen, blue, (int(proton_position[0]), int(proton_position[1])), proton_radius)

    total_electrons = len(electron_angles)


    if rotate_electron_rings:
        for i in range(len(electron_angles)):
            electron_angles[i] += electron_speed


    for i, distance in enumerate(electron_distances):
        electrons_in_ring = electron_ring_indices.count(i)
        if electrons_in_ring > 0:
            angle_increment = 360 / electrons_in_ring
            for j in range(electrons_in_ring):
                if i == 0:
                    angle = j * angle_increment
                else:
                    angle = j * angle_increment + (angle_increment / 2)

                electron_position = [
                    proton_position[0] + distance * math.cos(math.radians(angle + electron_angles[j])),
                    proton_position[1] + distance * math.sin(math.radians(angle + electron_angles[j]))
                ]

                pygame.draw.circle(screen, yellow, (int(electron_position[0]), int(electron_position[1])),
                                   electron_radius)


    for i, distance in enumerate(electron_distances):
        electrons_in_ring = electron_ring_indices.count(i)
        text = font.render(f"Ring {i + 1}: {electrons_in_ring}", True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 30))


    total_text = font.render(f"Electrons: {total_electrons}", True, (255, 255, 255))
    screen.blit(total_text, (10, height - 160))


    if 1 <= total_electrons <= max(element_mapping.keys()):
        element_info = element_mapping.get(total_electrons, {})
        element_text = font.render(
            f"Element: {element_info.get('name', 'Unknown')} ({element_info.get('symbol', '??')})", True,
            (255, 255, 255))
        proton_text = font.render(f"Protons: {element_info.get('protons', 'Unknown')}", True, (255, 255, 255))
        neutron_text = font.render(f"Neutrons: {element_info.get('neutrons', 'Unknown')}", True, (255, 255, 255))
        atomic_mass_text = font.render(f"Atomic Mass: {element_info.get('atomic_mass', 'Unknown')}", True,
                                       (255, 255, 255))

        screen.blit(element_text, (10, height - 40))
        screen.blit(proton_text, (10, height - 130))
        screen.blit(neutron_text, (10, height - 100))
        screen.blit(atomic_mass_text, (10, height - 70))
        rotate_electron_rings_enabled = True  # Allow spinning
    else:
        unknown_text = font.render("Element: Unknown", True, (255, 255, 255))
        screen.blit(unknown_text, (10, height - 40))
        rotate_electron_rings_enabled = False  # Disable spinning

    pygame.display.flip()
    clock.tick(60)
