from GameManager import GameManager

def main():
    game_manager = GameManager()
    
    if game_manager.run_menu():
        game_manager.run_game()

if __name__ == "__main__":
    main()
