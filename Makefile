PY := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
UVICORN := $(PY) -m uvicorn
VERSION_FILE := VERSION
TOKEN_FILE := .dev_token

.PHONY: version token up clean

version:
	@echo "Generating $(VERSION_FILE) from git..."
	@echo $$(git describe --tags --always --dirty 2>/dev/null || echo dev) > $(VERSION_FILE)
	@echo "Wrote $(VERSION_FILE):" $$(cat $(VERSION_FILE))

token:
	@echo "Generating development JWT token into $(TOKEN_FILE)..."
	@$(PY) - <<'PY' > $(TOKEN_FILE)
import os
from app.auth import create_access_token
user = os.environ.get("DEV_TOKEN_SUB", "admin")
# Create a short-lived token for local/dev use
print(create_access_token(data={"sub": user}))
PY
	@echo "Token written to $(TOKEN_FILE)"

up: version token
	@echo "Starting uvicorn..."
	$(UVICORN) main:app --reload

clean:
	@rm -f $(VERSION_FILE) $(TOKEN_FILE)
