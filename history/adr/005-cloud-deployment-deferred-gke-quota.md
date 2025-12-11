# ADR-005: Cloud Deployment Deferred Due to GKE Quota

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2025-12-11
- **Feature:** Phase V - Cloud Deployment
- **Context:** Phase V requires cloud Kubernetes deployment with Kafka and Dapr for event-driven architecture

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Cloud deployment strategy
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - GKE, DOKS, smaller cluster
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects infrastructure and demo
-->

## Decision

**Defer cloud deployment to GKE pending GCP quota increase.**

**Current State:**
- Local Minikube deployment with Strimzi Kafka + Dapr: FULLY FUNCTIONAL
- GCP project `evolution-todo-v2` created with billing linked
- Docker images pushed to Artifact Registry (backend:v1, frontend:v1)
- GKE Autopilot cluster created, then DELETED due to quota limits

**Root Cause:**
- GCP CPUS_ALL_REGIONS quota: 4 available / 10 limit
- Kafka + Dapr + App pods require ~24 CPUs
- GKE Autopilot scaled nodes but hit quota ceiling

**Action Items:**
1. Request quota increase at: https://console.cloud.google.com/iam-admin/quotas?project=evolution-todo-v2
2. Increase CPUS_ALL_REGIONS to 24
3. Wait for approval (typically 2-24 hours)
4. Redeploy using documented commands in SESSION_HANDOFF.md

## Rationale

### Why Defer (Not Find Workaround)

1. **Hackathon Demo Ready:** Local Minikube demonstrates full Phase V functionality
2. **No Feature Gap:** All event-driven code (models, service, handlers) is complete
3. **Cost Control:** GKE cluster deleted immediately to prevent charges
4. **Clean Recovery:** All GCP resources (project, AR, images) preserved for redeployment

### Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Standard GKE 1-node cluster | Rejected | Kafka won't fit in 6 CPUs |
| Redis pub/sub instead of Kafka | Rejected | Compromises Phase V architecture |
| DigitalOcean DOKS | Considered | User chose GCP, images already in AR |
| Wait for quota, redeploy later | **Accepted** | Clean path forward |

### What Was Tried and Failed

1. **Redpanda**: Too heavy for Minikube resource constraints
2. **Bitnami Kafka**: Image paywall since August 2025
3. **GKE Autopilot**: Quota exceeded during scale-up

### What Works

1. **Strimzi Kafka Operator**: Official K8s way to run Kafka
2. **Kafka 4.0.0**: Required version (3.8.0 unsupported)
3. **Dapr**: All components deployed, sidecar injection working
4. **Local Demo**: Full event flow testable on Minikube

## Consequences

### Positive

1. **No Charges:** GKE cluster deleted, $0 ongoing cost
2. **Images Ready:** Artifact Registry has both images for instant redeploy
3. **Code Complete:** No code changes needed when quota approved
4. **Demo Available:** Local Minikube proves full functionality

### Negative

1. **Cloud Demo Delayed:** Cannot demonstrate GKE until quota approved
2. **Manual Redeployment:** Need to recreate cluster when quota available
3. **Potential Review Impact:** Hackathon judges may prefer cloud deployment

### Mitigation

- SESSION_HANDOFF.md contains exact redeploy commands
- Test script `scripts/test-kafka-dapr.sh` verifies local deployment
- Local demo video can show full Phase V functionality

## Related Documents

- `docs/SESSION_HANDOFF.md` - Resume point for cloud deployment
- `infra/dapr/components/pubsub.yaml` - Kafka pub/sub component
- `infra/dapr/subscriptions/tasks.yaml` - Event subscriptions
- `scripts/test-kafka-dapr.sh` - Verification script
- `.claude/skills/kafka-dapr-patterns.md` - Event patterns reference
