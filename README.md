# CI/CD Final Project: Hit Counter Service

This repository contains the IBM/Coursera Introduction to CI/CD final project: a small Flask REST API that creates, reads, increments, lists, and deletes named hit counters. It follows the application and test conventions in the [IBM Skills Network practice repository](https://github.com/ibm-developer-skills-network/wtecc-CICD_PracticeCode). The service is intended for course exercises; its counters are held in memory and reset when the process restarts.

## Technology

- Python 3.9, Flask, and Gunicorn
- Nose and Pinocchio for unit tests; Flake8 for linting
- GitHub Actions for continuous integration
- Tekton, Buildah, Kubernetes, and OpenShift for pipeline build and deployment

The service listens on `0.0.0.0:8000` and logs `SERVICERUNNING` at startup. Its API provides `GET /`, `GET /health`, `GET /counters`, `POST /counters/<name>`, `GET /counters/<name>`, `PUT /counters/<name>`, and `DELETE /counters/<name>`.

## Repository Layout

```text
.github/workflows/workflow.yml   GitHub Actions CI
.tekton/tasks.yml                Local cleanup, test, and deployment tasks
.tekton/pipeline.yml             Clone, lint, test, build, and deploy pipeline
.tekton/pvc.yml                  Shared pipeline workspace claim
k8s/                             Deployment and service manifests
service/                         Flask application and API routes
tests/                           Nose route tests
docs/OPENSHIFT_EVIDENCE.md       Course-cluster setup and evidence steps
```

## Run Locally

Python 3.9 is recommended to match the course dependencies.

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
flake8 --count --max-complexity=10 --max-line-length=127 --statistics
nosetests -v --with-spec --spec-color
flask run
```

The Flask configuration in [.flaskenv](.flaskenv) starts the service on port `8000`, bound to all interfaces. Alternatively, run `honcho start` or use the included [Dockerfile](Dockerfile).

## GitHub Actions

The [workflow](.github/workflows/workflow.yml) runs for pushes to `main`, pull requests targeting `main`, and manual dispatch. It uses a Python 3.9 job container, installs the pinned dependencies, runs Flake8, and executes the Nose suite. The real execution result is available in the repository's Actions tab after a GitHub run; no run result is inferred from local tests.

## Tekton and OpenShift

The [pipeline](.tekton/pipeline.yml) runs cleanup, `git-clone`, `flake8`, `nose`, `buildah`, and `openshift-client` in order. The shared workspace is bound to the [PVC](.tekton/pvc.yml). The catalog tasks `git-clone`, `flake8`, `nose`, and the Buildah ClusterTask must be installed in the course namespace. The local [tasks](.tekton/tasks.yml) supply cleanup, a combined test task, and a workspace-aware OpenShift client task.

See the [OpenShift evidence guide](docs/OPENSHIFT_EVIDENCE.md) for PVC creation, catalog prerequisites, pipeline submission, application checks, and the required screenshots. The pipeline image parameter must name a writable image registry destination, typically `image-registry.openshift-image-registry.svc:5000/<project>/counter-service:latest`.

## Attribution

The Flask service structure, route behavior, test conventions, and runtime configuration are adapted from the [IBM Skills Network CI/CD practice repository](https://github.com/ibm-developer-skills-network/wtecc-CICD_PracticeCode), authored by John J. Rofrano and contributors. The upstream Apache License 2.0 is included in [LICENSE](LICENSE); applicable source-file notices are retained.

## Submission Links

- [Repository README](https://github.com/pb1803/ci-cd-final-project/blob/main/README.md)
- [GitHub Actions workflow](https://github.com/pb1803/ci-cd-final-project/blob/main/.github/workflows/workflow.yml)
- [Tekton tasks](https://github.com/pb1803/ci-cd-final-project/blob/main/.tekton/tasks.yml)