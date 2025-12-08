import pygame
import math

class UI:
    """Classe pour gérer l'affichage/interface utilisateur du jeu"""
    
    @staticmethod
    def draw_menu(screen, width, height):
        """Dessine le menu principal avec 3 boutons"""
        screen.fill((0, 0, 0))  # Fond noir
        
        # Titre
        big_font = pygame.font.Font(None, 100)
        title = big_font.render("WORMS", True, (0, 255, 0))
        title_rect = title.get_rect(center=(width // 2, height // 4))
        screen.blit(title, title_rect)
        
        # Bouton Jouer
        play_button = pygame.Rect(width // 2 - 150, height // 2 - 70, 300, 60)
        pygame.draw.rect(screen, (0, 200, 0), play_button)
        pygame.draw.rect(screen, (255, 255, 255), play_button, 3)
        
        button_font = pygame.font.Font(None, 50)
        play_text = button_font.render("JOUER", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=play_button.center)
        screen.blit(play_text, play_text_rect)
        
        # Bouton Settings
        settings_button = pygame.Rect(width // 2 - 150, height // 2 + 10, 300, 60)
        pygame.draw.rect(screen, (50, 50, 200), settings_button)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3)
        
        settings_text = button_font.render("PARAMETRES", True, (255, 255, 255))
        settings_text_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_text_rect)
        
        # Bouton Quitter
        quit_button = pygame.Rect(width // 2 - 150, height // 2 + 90, 300, 60)
        pygame.draw.rect(screen, (200, 0, 0), quit_button)
        pygame.draw.rect(screen, (255, 255, 255), quit_button, 3)
        
        quit_text = button_font.render("QUITTER", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_text_rect)
        
        return play_button, settings_button, quit_button
    
    @staticmethod
    def draw_settings(screen, width, height, controls):
        """Dessine l'écran des paramètres pour changer les touches"""
        screen.fill((30, 30, 30))  # Fond gris foncé
        
        # Titre
        title_font = pygame.font.Font(None, 80)
        title = title_font.render("PARAMETRES", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width // 2, 60))
        screen.blit(title, title_rect)
        
        # Instructions
        small_font = pygame.font.Font(None, 30)
        instruction = small_font.render("Cliquez sur une action pour changer sa touche", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(width // 2, 120))
        screen.blit(instruction, instruction_rect)
        
        # Afficher les contrôles
        control_font = pygame.font.Font(None, 36)
        y_offset = 180
        button_rects = {}
        
        control_labels = {
            'left': 'Déplacer à gauche',
            'right': 'Déplacer à droite',
            'jump': 'Sauter',
            'aim_up': 'Angle vers le haut',
            'aim_down': 'Angle vers le bas',
            'shoot': 'Tirer',
            'weapon_menu': 'Menu d\'arme'
        }
        
        for key, label in control_labels.items():
            # Label de l'action
            action_text = control_font.render(f"{label}:", True, (255, 255, 255))
            screen.blit(action_text, (100, y_offset))
            
            # Bouton avec la touche actuelle
            key_name = pygame.key.name(controls[key]).upper()
            button_rect = pygame.Rect(width - 250, y_offset - 5, 150, 40)
            pygame.draw.rect(screen, (70, 70, 70), button_rect)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
            
            key_text = control_font.render(key_name, True, (0, 255, 0))
            key_text_rect = key_text.get_rect(center=button_rect.center)
            screen.blit(key_text, key_text_rect)
            
            button_rects[key] = button_rect
            y_offset += 60
        
        # Bouton Retour
        back_button = pygame.Rect(width // 2 - 100, height - 80, 200, 50)
        pygame.draw.rect(screen, (0, 150, 0), back_button)
        pygame.draw.rect(screen, (255, 255, 255), back_button, 3)
        
        back_font = pygame.font.Font(None, 40)
        back_text = back_font.render("RETOUR", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)
        
        return button_rects, back_button
    
    @staticmethod
    def draw_key_prompt(screen, width, height, action):
        """Dessine une fenêtre pour demander une nouvelle touche"""
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        prompt_font = pygame.font.Font(None, 50)
        prompt_text = prompt_font.render(f"Appuyez sur une touche pour '{action}'", True, (255, 255, 0))
        prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2))
        screen.blit(prompt_text, prompt_rect)
        
        cancel_font = pygame.font.Font(None, 30)
        cancel_text = cancel_font.render("Appuyez sur ESC pour annuler", True, (200, 200, 200))
        cancel_rect = cancel_text.get_rect(center=(width // 2, height // 2 + 60))
        screen.blit(cancel_text, cancel_rect)
    
    @staticmethod
    def draw_game_setup(screen, width, height, num_players, worms_per_player):
        """Dessine l'écran de configuration de partie"""
        screen.fill((20, 20, 40))  # Fond bleu foncé
        
        # Titre
        title_font = pygame.font.Font(None, 80)
        title = title_font.render("CONFIGURATION", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width // 2, 80))
        screen.blit(title, title_rect)
        
        label_font = pygame.font.Font(None, 45)
        value_font = pygame.font.Font(None, 60)
        button_font = pygame.font.Font(None, 40)
        
        # Nombre de joueurs
        players_label = label_font.render("Nombre de joueurs :", True, (200, 200, 200))
        screen.blit(players_label, (150, 180))
        
        # Boutons - et + pour joueurs
        minus_players = pygame.Rect(width // 2 - 100, 220, 50, 50)
        plus_players = pygame.Rect(width // 2 + 50, 220, 50, 50)
        
        pygame.draw.rect(screen, (200, 50, 50) if num_players > 2 else (100, 100, 100), minus_players)
        pygame.draw.rect(screen, (255, 255, 255), minus_players, 2)
        minus_text = value_font.render("-", True, (255, 255, 255))
        screen.blit(minus_text, (width // 2 - 88, 218))
        
        pygame.draw.rect(screen, (50, 200, 50), plus_players)
        pygame.draw.rect(screen, (255, 255, 255), plus_players, 2)
        plus_text = value_font.render("+", True, (255, 255, 255))
        screen.blit(plus_text, (width // 2 + 60, 218))
        
        # Valeur nombre de joueurs
        players_value = value_font.render(str(num_players), True, (0, 255, 255))
        players_value_rect = players_value.get_rect(center=(width // 2, 245))
        screen.blit(players_value, players_value_rect)
        
        # Nombre de vers par joueur
        worms_label = label_font.render("Vers par joueur :", True, (200, 200, 200))
        screen.blit(worms_label, (150, 330))
        
        # Boutons - et + pour vers
        minus_worms = pygame.Rect(width // 2 - 100, 370, 50, 50)
        plus_worms = pygame.Rect(width // 2 + 50, 370, 50, 50)
        
        pygame.draw.rect(screen, (200, 50, 50) if worms_per_player > 1 else (100, 100, 100), minus_worms)
        pygame.draw.rect(screen, (255, 255, 255), minus_worms, 2)
        minus_text2 = value_font.render("-", True, (255, 255, 255))
        screen.blit(minus_text2, (width // 2 - 88, 368))
        
        pygame.draw.rect(screen, (50, 200, 50), plus_worms)
        pygame.draw.rect(screen, (255, 255, 255), plus_worms, 2)
        plus_text2 = value_font.render("+", True, (255, 255, 255))
        screen.blit(plus_text2, (width // 2 + 60, 368))
        
        # Valeur nombre de vers
        worms_value = value_font.render(str(worms_per_player), True, (0, 255, 255))
        worms_value_rect = worms_value.get_rect(center=(width // 2, 395))
        screen.blit(worms_value, worms_value_rect)
        
        # Sélecteur de terrain
        terrain_label = label_font.render("Terrain :", True, (200, 200, 200))
        screen.blit(terrain_label, (150, 480))
        
        # Boutons flèches pour changer de terrain
        prev_terrain = pygame.Rect(width // 2 - 200, 520, 50, 50)
        next_terrain = pygame.Rect(width // 2 + 150, 520, 50, 50)
        
        pygame.draw.rect(screen, (100, 100, 200), prev_terrain)
        pygame.draw.rect(screen, (255, 255, 255), prev_terrain, 2)
        prev_text = value_font.render("<", True, (255, 255, 255))
        screen.blit(prev_text, (width // 2 - 188, 518))
        
        pygame.draw.rect(screen, (100, 100, 200), next_terrain)
        pygame.draw.rect(screen, (255, 255, 255), next_terrain, 2)
        next_text = value_font.render(">", True, (255, 255, 255))
        screen.blit(next_text, (width // 2 + 162, 518))
        
        # Visualizer du terrain (miniature)
        visualizer_rect = pygame.Rect(width // 2 - 140, 520, 280, 140)
        pygame.draw.rect(screen, (50, 50, 50), visualizer_rect)
        pygame.draw.rect(screen, (255, 255, 255), visualizer_rect, 2)
        
        # Bouton Commencer
        start_button = pygame.Rect(width // 2 - 120, height - 100, 240, 60)
        pygame.draw.rect(screen, (0, 200, 0), start_button)
        pygame.draw.rect(screen, (255, 255, 255), start_button, 3)
        
        start_text = button_font.render("COMMENCER", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)
        
        return minus_players, plus_players, minus_worms, plus_worms, prev_terrain, next_terrain, visualizer_rect, start_button
    
    @staticmethod
    def draw_pause_menu(screen, width, height):
        """Dessine le menu pause avec 3 boutons"""
        # Overlay semi-transparent
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Titre PAUSE
        title_font = pygame.font.Font(None, 100)
        title = title_font.render("PAUSE", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width // 2, height // 4))
        screen.blit(title, title_rect)
        
        # Bouton Continuer
        continue_button = pygame.Rect(width // 2 - 150, height // 2 - 70, 300, 60)
        pygame.draw.rect(screen, (0, 200, 0), continue_button)
        pygame.draw.rect(screen, (255, 255, 255), continue_button, 3)
        
        button_font = pygame.font.Font(None, 50)
        continue_text = button_font.render("CONTINUER", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        screen.blit(continue_text, continue_text_rect)
        
        # Bouton Settings
        settings_button = pygame.Rect(width // 2 - 150, height // 2 + 10, 300, 60)
        pygame.draw.rect(screen, (50, 50, 200), settings_button)
        pygame.draw.rect(screen, (255, 255, 255), settings_button, 3)
        
        settings_text = button_font.render("PARAMETRES", True, (255, 255, 255))
        settings_text_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_text_rect)
        
        # Bouton Quitter
        quit_button = pygame.Rect(width // 2 - 150, height // 2 + 90, 300, 60)
        pygame.draw.rect(screen, (200, 0, 0), quit_button)
        pygame.draw.rect(screen, (255, 255, 255), quit_button, 3)
        
        quit_text = button_font.render("QUITTER", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_text_rect)
        
        return continue_button, settings_button, quit_button
    
    @staticmethod
    def draw_player(screen, player):
        """Dessine le joueur"""
        pygame.draw.rect(screen, (0, 255, 0), player.rect)
        player.draw_hp(screen)
    
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
    def draw_hud(screen, player, charging_power, time_remaining=None):
        """Affiche l'angle, la puissance et le timer en haut à gauche"""
        font = pygame.font.Font(None, 36)
        
        angle_text = font.render(f"Angle: {player.aim_angle}°", True, (255, 255, 255))
        screen.blit(angle_text, (10, 10))
        
        power_text = font.render(f"Puissance: {int(charging_power)}", True, (255, 255, 255))
        screen.blit(power_text, (10, 50))
        
        # Afficher le timer
        if time_remaining is not None:
            timer_color = (255, 0, 0) if time_remaining <= 5 else (255, 255, 255)
            timer_text = font.render(f"Temps: {int(time_remaining)}s", True, timer_color)
            screen.blit(timer_text, (10, 90))
    
    @staticmethod
    def draw_trajectory(screen, trajectory_calc, player, charging_power):
        """Dessine la trajectoire prédite pendant la charge"""
        if charging_power > 0:
            is_grenade = player.selected_weapon == "grenade"
            trajectory_points = trajectory_calc.calculate_trajectory_points(
                player.rect.centerx, player.rect.centery,
                player.aim_angle, charging_power,
                is_grenade=is_grenade,
                air_friction=player.air_friction_enabled
            )
            # Couleur différente selon l'arme
            color = (0, 255, 0) if is_grenade else (255, 100, 100)
            trajectory_calc.draw_trajectory(screen, trajectory_points, color=color)
    
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
    
    @staticmethod
    def draw_weapon_menu(screen, worm, selected_weapon, air_friction):
        """Dessine le menu de sélection d'arme au-dessus du ver"""
        menu_width = 200
        menu_height = 105
        menu_x = worm.rect.centerx - menu_width // 2
        menu_y = worm.rect.top - menu_height - 10
        
        # S'assurer que le menu reste dans l'écran
        menu_x = max(10, min(menu_x, screen.get_width() - menu_width - 10))
        menu_y = max(10, menu_y)
        
        # Fond du menu
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (40, 40, 40), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)
        
        font = pygame.font.Font(None, 28)
        
        # Option Roquette
        rocket_rect = pygame.Rect(menu_x, menu_y, menu_width, 30)
        rocket_color = (0, 150, 0) if selected_weapon == "rocket" else (70, 70, 70)
        pygame.draw.rect(screen, rocket_color, rocket_rect)
        pygame.draw.rect(screen, (255, 255, 255), rocket_rect, 1)
        
        rocket_text = font.render("Roquette", True, (255, 255, 255))
        rocket_text_rect = rocket_text.get_rect(center=rocket_rect.center)
        screen.blit(rocket_text, rocket_text_rect)
        
        # Option Grenade
        grenade_rect = pygame.Rect(menu_x, menu_y + 35, menu_width, 30)
        grenade_color = (0, 150, 0) if selected_weapon == "grenade" else (70, 70, 70)
        pygame.draw.rect(screen, grenade_color, grenade_rect)
        pygame.draw.rect(screen, (255, 255, 255), grenade_rect, 1)
        
        grenade_text = font.render("Grenade", True, (255, 255, 255))
        grenade_text_rect = grenade_text.get_rect(center=grenade_rect.center)
        screen.blit(grenade_text, grenade_text_rect)
        
        # Option Frottements d'air
        friction_rect = pygame.Rect(menu_x, menu_y + 70, menu_width, 30)
        pygame.draw.rect(screen, (70, 70, 70), friction_rect)
        pygame.draw.rect(screen, (255, 255, 255), friction_rect, 1)
        
        friction_status = "ON" if air_friction else "OFF"
        friction_color = (0, 255, 0) if air_friction else (255, 100, 100)
        friction_text = font.render(f"Frottements: {friction_status}", True, friction_color)
        friction_text_rect = friction_text.get_rect(center=friction_rect.center)
        screen.blit(friction_text, friction_text_rect)
