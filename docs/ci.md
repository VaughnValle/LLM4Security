# Continuous integration

`.github/workflows/ci.yml` runs on pushes, pull requests (including forks), merge
queue events, and manual dispatch. It uses GitHub-hosted Ubuntu 24.04 runners,
read-only repository permissions, pinned action revisions, and no repository
secrets. Superseded runs are cancelled. The README is unchanged by this setup.

| Check | What it verifies |
| --- | --- |
| Quality and lockfile | Locked dependency installation, Ruff lint/format, and Actionlint workflow validation |
| Tests (Python 3.12 / 3.13) | Unit tests, real Icarus fixture execution, MCP transport, JSON schemas, inference-wire tests, and coverage |
| Build and installed CLI smoke tests | Build wheel/sdist; install the wheel with EDA extras into an isolated environment; import packages and run all three CLI help commands outside the checkout |
| Docker EDA and deployment configuration | Validate both Compose manifests, build the EDA image, check artifact export, and execute all ten synthetic cases through MCP and Docker |
| CI passed | Fails unless every required job succeeds, including both Python versions |

The Python tests require at least 60% aggregate statement coverage across the
application packages. The initial local measurement was approximately 65%; this
includes unfinished scaffold modules. Coverage is reported, not a claim that the
remaining paths are validated. Increase the threshold as those paths gain tests.

The Docker suite uses a temporary external fixture checkout, not an upstream
GUIDE download. This exercises `GUIDE_ROOT` integration with project-owned tests
without depending on private machines or benchmark availability. Deliberately
faulty designs must produce the expected assertion failure; a compile failure,
timeout, or unexpected outcome fails the job. No LLM is involved in this CI run.

JUnit XML, coverage XML/HTML, Python distributions, and Docker case reports/logs/
waveforms are retained as workflow artifacts for 14 days. Test evidence is uploaded
even when a test fails. The artifact paths contain CI-generated fixtures and
reports, not developer `.env` files or private deployment data.

## Enable and require checks

1. Commit and push the workflow changes to the PR branch. An open PR should
   receive a new Actions run. If none appears, check that GitHub Actions is enabled
   under repository Settings → Actions → General. A first-time external
   contributor's run may require a maintainer to approve execution.
2. After the first successful run, configure the target branch's ruleset or
   branch protection to require the **CI passed** status check before merging.
   Select the check produced by this workflow; do not retain the old `phase1`
   check from the replaced basic workflow.
3. Keep the merge-queue trigger if using a merge queue. The overall status check
   deliberately fails when a dependency is skipped or cancelled.

The workflow file defines checks but does not enable Actions or change repository
rules. Those settings must be configured in GitHub. Weekly Dependabot PRs keep
the pinned GitHub Actions revisions up to date.

## Hardware acceptance remains separate

GitHub-hosted runners do not validate the R9700, ROCm inference, checkpoint
loading, Hermes behavior, or 64K context capacity. The large inference image is
not built and the model is not downloaded in this workflow. Compose validation
checks configuration syntax/interpolation; it does not verify GPU compatibility.

Continue the documented GPU and Hermes acceptance checks on the research guest
after changing the inference image, driver, checkpoint, or serving configuration.
Do not attach the private GPU VM as an unrestricted runner for public PR code.

References: [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
and [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
