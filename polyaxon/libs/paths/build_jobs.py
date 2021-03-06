import logging

from db.models.repos import ExternalRepo

_logger = logging.getLogger('polyaxon.jobs.utils')


def get_job_repo_path(job, project):
    job_spec = job.specification
    if job_spec.build.git:  # We need to fetch the repo first
        try:
            repo = ExternalRepo.objects.get(project=project,
                                            git_url=job_spec.build.git)
        except ExternalRepo.DoesNotExist:
            _logger.error(
                'Something went wrong, '
                'the external repo `%s` was not found', job_spec.build.git)
            raise ValueError('Repo was not found for `{}`.'.format(job_spec.build.git))

        repo_path = repo.path
    else:
        repo_path = project.repo.path
    return repo_path
