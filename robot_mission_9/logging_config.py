
# logging_config.py
import logging
import os

def configurer_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger  # Si le logger a déjà des handlers, on ne fait rien
    
    logger.setLevel(logging.DEBUG)  # Vous pouvez ajuster le niveau de log ici*
    
    log_file = './logs'
    if not os.path.exists(log_file):
        os.makedirs(log_file)
        
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Créer un StreamHandler pour afficher les logs dans la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Niveau de log pour la console
    console_handler.setFormatter(formatter)

    # Créer plusieurs FileHandler
    fichier_handler1 = logging.FileHandler('logs/infos.log', mode='w')
    fichier_handler2 = logging.FileHandler('logs/errors.log',mode='w')
    fichier_handler3 = logging.FileHandler('logs/debug.log',mode='w')

    # Configurer les niveaux de log pour chaque FileHandler
    fichier_handler1.setLevel(logging.INFO)
    fichier_handler2.setLevel(logging.WARNING)
    fichier_handler3.setLevel(logging.DEBUG)

    # Créer des Formatter et les associer aux FileHandler
    fichier_handler1.setFormatter(formatter)
    fichier_handler2.setFormatter(formatter)
    fichier_handler3.setFormatter(formatter)

    # Ajouter les FileHandler au logger principal
    logger.addHandler(fichier_handler1)
    logger.addHandler(fichier_handler2)
    logger.addHandler(fichier_handler3)
    # Ajouter le StreamHandler au logger principal
    logger.addHandler(console_handler)

    return logger

# logger = configurer_logger()
