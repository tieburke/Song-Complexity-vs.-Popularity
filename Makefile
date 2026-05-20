demo: create_graphs.py
	@echo
	@echo Open the desktop to see the results
	@echo
	@python create_graphs.py

test: unit_tests.py
	@echo Testing unit_tests ...
	@chmod +x ./unit_tests.py
	@./unit_tests.py -v
	@echo

clean:
	@rm -fr __pycache__