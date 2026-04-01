# -- Settings ------------------------------------------------------------------

# Use latest version of PowerShell on Windows
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# -- Variables -----------------------------------------------------------------

package := "icolyzer"

export PYTEST_ADDOPTS := if os() == "windows" { "-p no:prysk" } else { "" }

# -- Recipes -------------------------------------------------------------------

# Setup Python environment
[group('setup')]
setup:
	uv venv --allow-existing
	uv sync --all-extras

# Check code with various linters
[group('lint')]
check: setup
	uv run mypy "{{package}}"
	uv run flake8
	uv run pylint .

# Run tests
[default]
[group('test')]
test: check
	uv run pytest .
