import configparser
import json
import os

from src.utils.helpers.datatypes.list_helpers import ListHelpers

from .environment import TestEnvName
from .secret_manager import SecretsManager

INI_FILE_PATH = "config/"


class Config:
    """Singleton holding environment-specific test settings.

    Pass ``env_name`` on first call; subsequent calls return the cached instance.
    MOCK/LOCAL envs load from ``.env.<env_name>``; others from ``<env_name>.ini``.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, env_name: str | None = None):
        if not hasattr(self, "_initialized"):
            self._configParser = configparser.ConfigParser()

            self._set_env_name(env_name)
            self._setup()

            self._initialized = True

    @property
    def env_name(self) -> str:
        return self._env_name

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def some_secret(self) -> dict | None:
        return self._some_secret

    def _set_env_name(self, env_name) -> None:
        if not env_name:
            raise ValueError("ENV_NAME is not defined")

        if env_name not in ListHelpers.list_from_enum_values(TestEnvName):
            raise ValueError(
                f"Unknown env name: {env_name}. Should be one of {ListHelpers.list_from_enum_values(TestEnvName)}"
            )

        self._env_name = env_name

    def _setup(self) -> None:
        if self._env_name in (TestEnvName.MOCK, TestEnvName.LOCAL):
            self._load_from_env_file()
        else:
            self._load_from_ini()

    def _load_from_env_file(self) -> None:
        self._base_url = os.getenv("BASE_URL")
        # Not set for local/mock
        self._some_secret = None

    def _load_from_ini(self) -> None:
        self._configParser.read(f"{INI_FILE_PATH}{self._env_name}.ini")

        self._base_url = self._configParser.get(self._env_name, "base_url")

        secret_arn = json.loads(self._configParser.get(self._env_name, "some_secret"))["arn"]
        self._some_secret = SecretsManager().get_json_creds(secret_arn)
