import logging

logger = logging.getLogger('global_logger')

logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler('logs/debug.log')
info_handler = logging.FileHandler('logs/info.log')

console_handler = logging.StreamHandler()

debug_handler.setLevel(logging.DEBUG)
info_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)

debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

debug_handler.setFormatter(debug_formatter)
info_handler.setFormatter(info_formatter)
console_handler.setFormatter(console_formatter)

logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(console_handler)
