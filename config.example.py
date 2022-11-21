LOG_FOLDER = './logs'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
LOG_FILE = 'app.log'
LOG_MAX_BYTES = 1048576
LOG_COUNT = 10

APP_PORT = 3000             #Порт, на котором запускается бэкенд
APP_HOST = 'localhost'      #Хост бэкенда

DB_HOST = '[Сервер БД]'
DB_NAME = '[Имя БД]'
DB_PORT = '[Порт БД]'
DB_USER = '[Пользователь БД]'
DB_PASSWORD = '[Пароль пользователя БД]'

IMAGE_PATH = '../static/images/'
IMAGE_NAME_LENGTH = 8

JWT_SECRET_KEY = '0b50eca328e641ae0fcc67cfbe902a6dd605ac3a49392ff477981526c7e1264a'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_MINUTES = 1440

LDAP_BASE_DN = '[DN, в котором происходит поиск пользователей]'         #например, 'dc=gkzd,dc=local'
LDAP_SERVER_NAME = '[Имя контроллера домена AD]'
LDAP_BIND_USER_NAME = '[Имя пользователя с правами чтения дерева домена AD]'
LDAP_BIND_USER_PASSWORD = '[Пароль пользователя]'

TEMP_DIR = 'tmp'
TEMP_NAME_LENGTH = 16

MAIL_HOST = '[Адрес почтового сервера]'
MAIL_PORT = '[Порт для отправки сообщений]'
MAIL_USER = '[Учетная запись отправителя почтовых уведомлений]'
MAIL_PASS = '[Пароль отправителя почтовых уведомлений]'


