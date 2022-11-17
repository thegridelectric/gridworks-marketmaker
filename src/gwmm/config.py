"""Settings for an AtomicTNode, readable from environment and/or from env files."""

import pendulum
from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import SecretStr


DEFAULT_ENV_FILE = ".env"


class MarketPublic(BaseModel):
    """This class is the publicly available information about the GNodeFactory"""

    algod_address: str = "http://localhost:4001"
    universe: str = "dev"
    gnf_admin_addr: str = "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI"
    gnf_api_root: str = "http://localhost:8000"
    gwmm_api_root: str = "http://localhost:7999"


class AlgoApiSecrets(BaseModel):
    algod_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    kmd_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    gen_kmd_wallet_password: SecretStr = SecretStr("")


class VanillaSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: MarketPublic = MarketPublic()


class RabbitBrokerClient(BaseModel):
    """Settings for connecting to a Rabbit Broker"""

    url: SecretStr = SecretStr("amqp://smqPublic:smqPublic@localhost:5672/d1__1")


class Settings(BaseSettings):
    g_node_alias: str = "d1.isone.ver.keene"
    g_node_id: str = "5ac8c31d-bf46-4f81-a5f2-6b3d20810435"
    g_node_instance_id: str = "d3c217af-d51f-44fb-adb1-932760e9cf12"
    g_node_role_value: str = "MarketMaker"
    my_super_alias: str = "d1.super3"
    my_time_coordinator_alias = "d1.time"
    initial_time_unix_s = pendulum.datetime(
        year=2020, month=1, day=1, hour=5
    ).int_timestamp
    log_level: str = "INFO"
    universe_type_value: str = "Dev"
    rabbit: RabbitBrokerClient = RabbitBrokerClient()
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: MarketPublic = MarketPublic()

    class Config:
        env_prefix = "MM_"
        env_nested_delimiter = "__"


class SupervisorSettings(BaseSettings):
    g_node_alias: str = "d1.super3"
    g_node_id: str = "edae8366-538b-42bb-8035-a11b40e382a0"
    g_node_instance_id: str = "dcea4b86-f4ad-4c3d-a624-9c8bbe3e4863"
    g_node_role_value: str = "Supervisor"
    my_time_coordinator_alias = "d1.time"
    log_level: str = "INFO"
    universe_type_value: str = "Dev"
    rabbit: RabbitBrokerClient = RabbitBrokerClient()

    class Config:
        env_prefix = "SUPER_"
        env_nested_delimiter = "__"
