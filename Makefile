IMAGE ?= stm32-build
build:
	docker run --rm -v $(PWD):/workspace:z -w /workspace \
			   --user $(shell id -u):$(shell id -g) $(IMAGE) \
			   make -C firmware all