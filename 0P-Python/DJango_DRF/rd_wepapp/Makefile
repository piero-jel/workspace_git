PRINT := @echo

# Default target para el run cuando ejecutamos make sin parametros
all:
	@make help --no-print-directory

help: ## Show help de los target dentro del Makefile.
	$(PRINT) "Help, descripcion de las acciones que se pueden ejecutar"
	$(PRINT)
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-20s\033[0m %s\n", $$1, $$2}'
	$(PRINT)

migrate: ## realiza la migracion de todos los modelos
	@python3 manage.py makemigrations
	@python3 manage.py migrate

shell: ## open shell iteractivo con los modelos disponibles
	@python3 manage.py shell

load_data: ## carga dato a la base desde un archivo con items del tipo objetos json, uno por cada linea del archivo.
	@python3 manage.py load_list_items --pathfile ../../items.json
#	@python3 manage.py load_from_json --pathfile ../../pretty_array_item.json

run: ## inicia el server
	@python3 manage.py runserver 127.0.0.1:8080

unittest: ## Ejecuta el unittest/test
	@python3 manage.py test -v 2
