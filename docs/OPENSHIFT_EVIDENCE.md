# OpenShift Course Evidence

These steps use the real course OpenShift Pipelines environment. The screenshots are evidence from that live environment and are intentionally not included or simulated in this repository.

## Prepare the Namespace

1. Sign in to the course OpenShift console and select the project where the pipeline and service should run.
2. Confirm the course catalog tasks are installed in the project: `git-clone`, `flake8`, `nose`, and the `buildah` ClusterTask. The pipeline expects the course conventions for their parameters and workspace names.
3. In the Codespace terminal, authenticate `oc` against that same cluster and project, or use the console's Import YAML workflow with these files.
4. Create the shared workspace claim:

   ```bash
   oc apply -f .tekton/pvc.yml
   oc get pvc pipelinerun-pvc
   ```

   In the Pipelines console, open the PVC details and capture its storage class, `1Gi` request, `ReadWriteOnce` access mode, and filesystem volume mode as `oc-pipelines-console-pvc-details.jpeg` (or `.png`).

5. Apply the local tasks and pipeline:

   ```bash
   oc apply -f .tekton/tasks.yml
   oc apply -f .tekton/pipeline.yml
   ```

   In the Pipelines console, open `counter-service-pipeline` and capture the ordered cleanup, git-clone, flake8, nose, buildah, and openshift-client tasks as `oc-pipelines-oc-final.jpeg` (or `.png`).

## Run and Verify

1. Allow the pipeline service account to push to the internal image registry if the course project has not already granted it:

   ```bash
   oc adm policy add-role-to-user system:image-builder -z pipeline
   ```

2. Start the pipeline, replacing `<project>` with the active OpenShift project name:

   ```bash
   tkn pipeline start counter-service-pipeline \
     --param repo-url=https://github.com/pb1803/ci-cd-final-project.git \
     --param branch=main \
     --param image-ref=image-registry.openshift-image-registry.svc:5000/<project>/counter-service:latest \
     --workspace name=pipeline-workspace,claimName=pipelinerun-pvc \
     --showlog
   ```

3. In the console, inspect the PipelineRun and verify the six tasks complete successfully. Capture that actual successful run as `oc-pipelines-oc-green.jpeg` (or `.png`).
4. Confirm the deployment and service are ready, then inspect the application log:

   ```bash
   oc get deployment,service counter-service
   oc logs deployment/counter-service
   ```

   The pod should listen on port `8000`, and its startup log must contain the exact text `SERVICERUNNING`. To probe the API from the Codespace, run `oc port-forward service/counter-service 8000:8000` and request `http://127.0.0.1:8000/health` in another terminal.

5. Capture the three screenshots directly from the course console using the requested filenames. Do not upload screenshots until they show the PVC details, configured task sequence, and successful live PipelineRun respectively.