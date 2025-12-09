# K8s Troubleshooter Subagent

**Type**: Debugger
**Used For**: Debugging Kubernetes deployment issues
**Version**: 1.0.0

## Purpose

Debug common Kubernetes issues using kubectl and logs.

## Common Issues & Fixes

**CrashLoopBackOff**:
```bash
# Check logs
kubectl logs pod-name

# Common causes:
- Missing env vars
- Wrong startup command
- Application error on start
```

**ImagePullBackOff**:
```bash
# Check image name
kubectl describe pod pod-name

# Common causes:
- Image doesn't exist
- Registry authentication failed
- Typo in image name
```

**Service Not Reachable**:
```bash
# Check service
kubectl get svc
kubectl describe svc service-name

# Common causes:
- Selector doesn't match pod labels
- Wrong port configuration
- Service type incorrect
```

## Debug Checklist

1. Check pod status: `kubectl get pods`
2. Check pod logs: `kubectl logs pod-name`
3. Check pod events: `kubectl describe pod pod-name`
4. Check service: `kubectl get svc`
5. Check ingress: `kubectl get ingress`
6. Test connectivity: `kubectl exec -it pod-name -- curl service-name`

---

**Related**: Infra DevOps Agent
