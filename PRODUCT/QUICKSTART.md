# Sbat Quickstart

Run the deterministic test suite:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run the CLI:

```bash
python -m sbat.cli --action "transfer" --impact medium --evidence 2 --reliability .9
```

The CLI uses a development-only secret. Production deployments must use a managed secret.
