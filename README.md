# otel-eval-bridge

`otel-eval-bridge` converts exported OpenTelemetry or Phoenix-style GenAI spans
into local eval cases while preserving trace and span references.

## At a Glance

| | |
| --- | --- |
| Job | Extract trace-linked eval inputs, expected values, observations, and provider/model metadata. |
| Built for | Eval engineers and observability teams turning recorded traces into regression inputs. |
| Differentiator | Dependency-free file bridge with default secret and email redaction. |
| Produces | JSONL eval cases, a trace-reference manifest, and eval results attached back to cases. |

## Install

```bash
python -m pip install "otel-eval-bridge==0.1.2"
```

## Verified Quickstart

Run from a source checkout:

```bash
otel-eval-bridge extract examples/genai_trace.json \
  --out /tmp/eval-cases.jsonl

otel-eval-bridge manifest /tmp/eval-cases.jsonl \
  --out /tmp/eval-manifest.json

otel-eval-bridge attach /tmp/eval-cases.jsonl examples/eval_results.json \
  --out /tmp/trace-linked-results.json
```

The bundled trace export produces two eval cases and an
`auraone.eval-run-manifest.v1` manifest.

## Input and Output Contract

The reader accepts a JSON list, a top-level `spans` list, or OTLP JSON
`resourceSpans[].scopeSpans[].spans[]`. Phoenix-style `input.value`,
`output.value`, `llm.provider`, and `llm.model_name` attributes are normalized
to the bridge's GenAI fields.

Each emitted case can include:

- trace ID, span ID, and span name;
- prompt/input, expected value, and observed completion;
- provider and model metadata.

`attach` matches result entries by trace ID first and span ID second.

## Runtime, Data, and Network Boundary

- All commands read and write local JSON or JSONL files.
- The CLI does not receive OTLP traffic, export telemetry, call an observability
  backend, run an eval, or make network requests.
- Redaction is enabled by default for sensitive keys, `sk-...`, `pypi-...`,
  bearer tokens, and email addresses.
- `--no-redact` disables that protection. Default redaction is pattern-based and
  is not a comprehensive privacy or compliance control.

## Limitations

- The bridge extracts eval inputs from exported trace data only. It does not run
  a scorer, validate observability semantics, or prove trace completeness.
- Redaction is pattern-based and intentionally small. Review emitted cases
  before sharing them outside the originating environment.

## Compatibility

The published `auraone-agent-studio-open` CLI declares
`otel-eval-bridge>=0.1.0` as a runtime dependency and exposes local trace import
and eval-case extraction paths. The JSONL output can also be adapted by an
in-house eval runner.

## Publication Status

Verified on 2026-07-13:

- PyPI: [`otel-eval-bridge==0.1.2`](https://pypi.org/project/otel-eval-bridge/0.1.2/)
- GitHub release: [`v0.1.2`](https://github.com/auraoneai/otel-eval-bridge/releases/tag/v0.1.2)
- The source, wheel, source distribution, and release tag are aligned on
  `0.1.2`.

## Next Action

Export a sanitized trace sample, inspect the generated cases for residual
sensitive data, then connect the JSONL file to the eval runner that owns scoring.
