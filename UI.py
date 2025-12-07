import pygame
import math

class UI:
    """Classe pour gérer l'affichage/interface utilisateur du jeu"""
    
    @staticmethod
    def draw_player(screen, player):
        """Dessine le joueur"""
        pygame.draw.rect(screen, (0, 255, 0), player.rect)
        player.draw_hp(screen)
    
    @staticmethod
    def draw_enemy(screen, enemy):
        """Dessine l'ennemi s'il est vivant"""
        if enemy.is_alive():
            enemy.draw(screen)
    
    @staticmethod
    def draw_aim_line(screen, player, length=50):
        """Dessine la ligne de visée du joueur"""
        angle_rad = math.radians(player.aim_angle)
        end_x = player.rect.centerx + length * math.cos(angle_rad)
        end_y = player.rect.centery + length * math.sin(angle_rad)
        pygame.draw.line(screen, (255, 255, 0),
                        (player.rect.centerx, player.rect.centery),
                        (end_x, end_y), 3)
    
    @staticmethod
    def draw_hud(screen, player, charging_power):
        """Affiche l'angle et la puissance en haut à gauche"""
        font = pygame.font.Font(None, 36)
        
        angle_text = font.render(f"Angle: {player.aim_angle}°", True, (255, 255, 255))
        screen.blit(angle_text, (10, 10))
        
        power_text = font.render(f"Puissance: {int(charging_power)}", True, (255, 255, 255))
        screen.blit(power_text, (10, 50))
    
    @staticmethod
    def draw_trajectory(screen, trajectory_calc, player, charging_power):
        """Dessine la trajectoire prédite pendant la charge"""
        if charging_power > 0:
            trajectory_points = trajectory_calc.calculate_trajectory_points(
                player.rect.centerx, player.rect.centery,
                player.aim_angle, charging_power
            )
            trajectory_calc.draw_trajectory(screen, trajectory_points, color=(255, 100, 100))
    
    @staticmethod
    def draw_projectiles(screen, projectiles):
        """Dessine tous les projectiles actifs"""
        for projectile in projectiles:
            projectile.draw(screen)
    
    @staticmethod
    def draw_game_over(screen, width, height, winner):
        """Dessine l'écran de victoire/défaite avec bouton rejouer"""
        # Overlay gris semi-transparent
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((100, 100, 100))
        screen.blit(overlay, (0, 0))
        
        # Texte de victoire/défaite
        big_font = pygame.font.Font(None, 80)
        if winner == 'player':
            win_text = big_font.render("GAGNÉ !", True, (0, 255, 0))
        else:
            win_text = big_font.render("PERDU !", True, (255, 0, 0))
        text_rect = win_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(win_text, text_rect)
        
        # Bouton rejouer
        button_rect = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
        
        button_font = pygame.font.Font(None, 40)
        button_text = button_font.render("REJOUER", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
        
        return button_rect  # Retourner le rect du bouton pour détecter les clics
