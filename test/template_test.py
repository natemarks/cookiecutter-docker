"""Test variou executions of the cookiecutter
Each parametrize test case is a set of cookiecutter json overrides

"""
import logging
import os
import pytest
import testinfra  # pylint: disable=W0611
from cookiecutter.main import cookiecutter

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

PROJECT_DIR = os.getcwd()


@pytest.mark.parametrize(
    "ccinput",
    [
        (
            {
                "project_name": "fff",
                "image1": "first",
                "image2": "second",
                "ami_id": "ami-fff"
            }),
        (
            {
                "project_name": "ggg",
                "image1": "alpha",
                "image2": "bravo",
                "ami_id": "ami-ggg"
            }),
    ],
)
class TestClass:  # pylint: disable=R0903
    """Table test the cookiecutter options"""

    def test_(
        self, host, tmp_path, ccinput
    ):  # pylint: disable=R0201
        """Iterate on different cookiecutter json overrides"""
        role_dir=str(tmp_path) + "/" + "docker-" + ccinput["project_name"]
        os.chdir(tmp_path)
        log.info("tmpdir: %s", str(tmp_path))
        cookiecutter(
            PROJECT_DIR,
            no_input=True,
            extra_context=ccinput,
        )
        #  check env file
        env_example = host.file(role_dir + '/env.example')
        assert env_example.exists

        #  check image1 Dockerfile
        image1_dockerfile_path = '/'.join(
            [
                role_dir,
                ccinput["image1"],
                'Dockerfile'
            ])
        image1_dockerfile = host.file(image1_dockerfile_path)
        assert image1_dockerfile.exists

        #  check image1 Dockerfile
        image2_dockerfile_path = '/'.join(
            [
                role_dir,
                ccinput["image2"],
                'Dockerfile'
            ])
        image2_dockerfile = host.file(image2_dockerfile_path)
        assert image2_dockerfile.exists
