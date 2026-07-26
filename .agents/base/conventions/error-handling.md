---
role: convention
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 6
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Error Handling Conventions

## Error Classification

Every error falls into one of three categories:

| Category | Definition | Action |
|---|---|---|
| **Recoverable** | Expected failure modes that the system can handle gracefully. Network timeout, validation error, duplicate record. | Catch, handle, continue. Log at WARN level. |
| **Non-recoverable** | Unexpected failures that prevent the current operation but don't threaten the system. NPE from bad input, third-party API returning garbage. | Catch, wrap with context, propagate up. Log at ERROR level. |
| **Fatal** | System integrity is compromised. Database connection lost, out of memory, corrupted state. | Log at CRITICAL level. Fail fast. Restart. |

## Catch at Boundaries

- Catch exceptions at system boundaries: API controllers, CLI entry points, queue consumers, event handlers.
- Internal code should propagate errors, not suppress them. Let them bubble to the boundary handler.
- Boundary handlers convert internal exceptions to appropriate responses: HTTP 4xx/5xx, exit codes, dead-letter queues.

## Never Swallow Errors

- A `catch` block that silently discards the error (no logging, no handling, no propagation) is a bug.
- If an error is truly ignorable, document why with a comment: `// Ignoring because secondary cache is optional, primary is available`.
- The only acceptable empty catch is when the caught exception type guarantees the operation was a no-op.

## Add Context

When catching and re-throwing, add context. The original error alone rarely tells you enough:

```
# Bad:
try:
    process_order(order)
except Exception as e:
    raise RuntimeError("Failed") from e

# Good:
try:
    process_order(order)
except Exception as e:
    raise RuntimeError(
        f"Failed to process order {order.id} for customer {order.customer_id}"
    ) from e
```

- Include relevant identifiers and the operation being attempted.
- Chain the original exception (`from e` in Python, `InnerException` in .NET, `cause` in Java) so the stack trace is preserved.

## Fail Fast

- If a precondition is violated at system start (missing config, unreachable database), fail immediately with a clear error message. Don't limp along in a degraded state.
- Assertions in code are for programmer errors — states that should be impossible. Use them liberally in development and testing. Don't use them for user input validation.
- If you detect corrupted state during runtime, log the full context and fail the operation. Don't attempt to "fix" unknown corruption.

## Don't Catch Generic Exceptions

- Catching `Exception` (Python), `Error` (JavaScript), `Throwable` (Java), or `Exception` (C#) is a code smell. You're hiding errors you don't understand.
- Catch specific exception types. If the library throws `NetworkError`, catch `NetworkError`.
- If you must catch a broad type, at least log the full exception details and consider re-throwing after handling what you can.

## Logging Levels

| Level | When to Use |
|---|---|
| `DEBUG` | Detailed diagnostic info. Off in production. Variable values, step-by-step flow. |
| `INFO` | High-level operational events. Service started, request completed, batch job finished. |
| `WARN` | Recoverable anomaly. Retry succeeded after 2 attempts, fallback path used, deprecated API called. |
| `ERROR` | Operation failure. Request failed, job aborted, data lost for this operation. But system continues. |
| `CRITICAL` | System failure. Service is down, data corruption detected, cannot recover without intervention. |

## Retry with Backoff

- For transient failures (network, rate limits, temporary unavailability), retry with exponential backoff.
- Never retry indefinitely. Set a maximum number of retries (3-5 is typical).
- Don't retry on validation errors, not-found errors, or authentication failures. They won't succeed on retry.
- Use a jitter to avoid thundering herd: `delay = base_delay * (2 ** attempt) + random_jitter`.
- Circuit break: if a downstream service is failing repeatedly, stop calling it temporarily. Fail fast and give it time to recover.
