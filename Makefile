OUTDIR=proto

.PHONY: default
default:
	-mkdir -p $(OUTDIR)
	python -m grpc_tools.protoc -I. --python_out=$(OUTDIR) --pyi_out=$(OUTDIR) --grpc_python_out=$(OUTDIR) ./grpc.proto
