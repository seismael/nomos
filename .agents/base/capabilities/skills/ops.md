---
role: capability
mode: skill
triggers: { phase: "*", type: ops, complexity: "*", valid: true }
layer: type
priority: 20
status: active
context_cost: medium
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Operations

Reference material for agents working on ops-type tasks. Covers infrastructure, CI/CD, configuration, and operational safety.

## Infrastructure as Code

All infrastructure changes must be version-controlled and reproducible:
- No manual console changes. If you click it, you must also code it.
- Infrastructure config lives in the repo: Terraform, CloudFormation, Pulumi, Ansible, Docker Compose.
- The repo is the source of truth for what's deployed. If they differ, the repo is right; fix the deployment.

## Common Ops Tasks

| Task | Typical Files | Safety Level |
|---|---|---|
| Dependency update | `package.json`, `requirements.txt`, `Cargo.toml` | Standard — review changelog, run tests |
| Configuration change | `.env`, `config.yaml`, feature flags | Standard — validate syntax, test in staging |
| CI/CD pipeline | `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml` | Standard/Complex — test on branch |
| Secret rotation | Secrets manager (not files!) | Complex — coordinate with dependent services |
| Database migration | Migration files, schema changes | Complex/Critical — backward compatible, tested rollback |
| Scaling adjustment | Auto-scaling config, instance sizes | Standard — monitor impact |
| Certificate renewal | Cert files, load balancer config | Standard — test in staging, monitor expiry dates |

## Safety Checklist

For every ops change, verify:
- [ ] **Documented:** What is changing and why. Written, not in someone's head.
- [ ] **Rollback plan:** Tested and documented. How do I undo this if it fails? (Mandatory.)
- [ ] **Blast radius:** What systems, teams, and users are affected? What breaks if this goes wrong?
- [ ] **Notified:** Affected teams know the change is happening, when, and what to watch for.
- [ ] **Monitoring:** Dashboards and alerts are configured for the change window. You'll know immediately if something breaks.
- [ ] **Staged:** Tested in a non-production environment first. If you can't test in staging, that's a risk to document.

## Deployment Patterns

| Pattern | How It Works | When to Use |
|---|---|---|
| **Blue-Green** | Two identical environments. Deploy to inactive, switch traffic. | Zero-downtime, instant rollback |
| **Canary** | Deploy to small % of traffic. Ramp up while monitoring. | Risky changes, need production validation |
| **Rolling** | Update instances one at a time. | Stateless services, can handle mixed versions |
| **Feature Flags** | Deploy code dark, enable via config. | Decouple deploy from release |

## Incident Response

1. **Detect:** Monitoring alerts, user reports, on-call pager. Acknowledge within SLA.
2. **Triage:** What's the severity? Scope (one user, one region, all)? Is it getting worse?
3. **Mitigate:** Stop the bleeding. Roll back, scale up, fail over, disable feature flag. Don't debug — mitigate first.
4. **Resolve:** Root cause fix after the incident is contained. Not during.
5. **Postmortem:** Blameless. What happened? Why? How do we prevent it? What monitoring would have caught it sooner?

## Observability

- **Logs:** Structured (JSON), searchable, with correlation IDs. Log at boundaries: requests, errors, state transitions.
- **Metrics:** RED (Rate, Errors, Duration) for services. USE (Utilization, Saturation, Errors) for resources.
- **Traces:** Distributed tracing for requests that span multiple services. Shows where time is spent.
- **Alerts:** On symptoms, not causes. "Error rate > 1%" not "CPU > 80%". Actionable — waking someone at 3am must be justified.

## Secrets Management

Never store secrets in: code, config files, environment variables checked into git, logs, or database dumps.

Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, GitHub Secrets). Secrets are injected at runtime, never at build time.
