# Handle PyPI Publish Request

This GitHub Action creates a pull request to upsert the given Python package to a GitHub-hosted PyPI repository.

> **Note:** This action works together with the [Publish to GitHub PyPI](https://github.com/bitovi/github-actions-publish-github-pypi) action to publish a Python package to a GitHub-hosted PyPI repository.

## Table of Contents
1. [Action Summary](#action-summary)
2. [Need help or have questions?](#need-help-or-have-questions)
3. [Pre-requisites](#pre-requisites)
4. [Basic Use](#basic-use)
5. [Inputs](#inputs)
6. [Contributing](#contributing)
7. [License](#license)


## Action Summary

This action performs the following steps to upsert a Python package to a GitHub-hosted PyPI repository:
1. Extract details from the `repository_dispatch` inputs
2. Generate/update files (e.g. `pypi/index.html` and `pypi/[package-name]/index.html`)
3. Commit changes to a new branch in the PyPI repository.
4. Create a pull request for review and merge.

> **Note:** This action does does not deploy the resulting PyPI index code anywhere. Essentially, you only need to host the `pypi` directory.  If you'd like to host it on GitHub Pages, you can use our [Static PyPI to GitHub Pages](https://github.com/bitovi/github-actions-static-pypi-to-github-pages) action.

If you would like to deploy other types of applications, check out our other actions:
| Action | Purpose |
| ------ | ------- |
| [Deploy Docker to EC2](https://github.com/marketplace/actions/deploy-docker-to-aws-ec2) | Deploys a repo with a Dockerized application to a virtual machine (EC2) on AWS |
| [Deploy Storybook to GitHub Pages](https://github.com/marketplace/actions/deploy-storybook-to-github-pages) | Builds and deploys a Storybook application to GitHub Pages. |
| [Deploy static site to AWS (S3/CDN/R53)](https://github.com/marketplace/actions/deploy-static-site-to-aws-s3-cdn-r53) | Hosts a static site in AWS S3 with CloudFront |
<br/>

**And more!**, check our [list of actions in the GitHub marketplace](https://github.com/marketplace?category=&type=actions&verification=&query=bitovi)

## Need help or have questions?

This project is supported by [Bitovi, A DevOps consultancy](https://www.bitovi.com/services/devops-consulting).

You can **get help or ask questions** on our:

- [Discord Community](https://discord.gg/zAHn4JBVcX)

Or, you can hire us for training, consulting, or development. [Set up a free consultation](https://www.bitovi.com/services/devops-consulting).


## Pre-requisites
- A GitHub repository to act as your PyPI.
- A GitHub repository with a Python package. To set up that repo, follow the instructions in the [publisher action](https://github.com/bitovi/github-actions-publish-github-pypi)

## Basic Use

For basic usage, create `.github/workflows/publish-handler.yaml` with the following to handle the publish trigger:

```yaml
name: Handle PyPI Publish triggers

on:
  workflow_dispatch:
    inputs:
      name:
        description: 'Name of the package'
        required: true
      version:
        description: 'Version of the package'
        required: true
      archive_url:
        description: 'URL to the archive of the package'
        required: true

jobs:
  build-and-commit:
    runs-on: ubuntu-latest

    # Allows this action to create PRs
    permissions:
      pull-requests: write
      contents: write

    steps:
      - name: Handle Python Package Publish
        uses: bitovi/github-actions-publish-github-pypi-handler@main
        with:
          name: ${{ inputs.name }}
          version: ${{ inputs.version }}
          archive_url: ${{ inputs.archive_url }}
          pypi_base_url: 'https://your-org.github.io/your-repo'
```

## Inputs

The following inputs can be used as `step.with` keys:

| Name                               | Type    | Description                                                                            |
|------------------------------------|---------|----------------------------------------------------------------------------------------|
| `github-token`                     | String  | (Required) The GitHub token to use for triggering the publish workflow in the PyPI repository |
| `checkout`                         | Boolean | (Optional) Whether to checkout the repository. Default is `true`                        |
| `python-version`                   | String  | (Required) The Python version to use. Default is `3.8`                                  |
| `name`                             | String  | (Required) Name of the package                                                          |
| `version`                          | String  | (Required) Version of the package                                                       |
| `archive_url`                      | String  | (Required) URL to the package archive                                                   |
| `pypi_base_url`                    | String  | (Required) Base URL of the PyPI repository                                              |
| `commit_branch`                    | String  | (Optional) Branch to commit the changes to. Default is `auto`                           |
| `pypi_root_dir`                    | String  | (Optional) Root directory of the PyPI repository. Default is `pypi`                     |
| `pypi-github-user-email`           | String  | (Optional) GitHub user email to use for committing the changes. Default is `github-actions[bot]@users.noreply.github.com` |
| `pypi-github-user-name`            | String  | (Optional) GitHub user name to use for committing the changes. Default is `github-actions[bot]` |

## Contributing

We would love for you to contribute to this action. [Issues](https://github.com/bitovi/github-actions-publish-github-pypi-handler/issues/new/choose) and Pull Requests are welcome!

## License

The scripts and documentation in this project are released under the MIT License.

# Provided by Bitovi

[Bitovi](https://www.bitovi.com/) is a proud supporter of Open Source software.

# We want to hear from you.

Come chat with us about open source in our Bitovi community [Discord](https://discord.gg/J7ejFsZnJ4Z)!