"""Settings for gridworks-marketmaker."""

from gwbase.config import GNodeSettings
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from gwmm.sema.property_format import LeftRightDot, SpaceheatName


class GwmmSettings(GNodeSettings):
    """Reads from env (GWMM_*) and/or a `.env` file at the repo root.

    Inherits `rabbit: RabbitBrokerClient`, `g_node_path`, `log_level`
    (and the rest of `ServiceSettings`) from `GNodeSettings`.
    `service_alias` MUST match the g.node.gt.json Alias; `GridworksActor`
    enforces the binding at boot. The transport class is intrinsic to the
    maker's role and is passed up by `MarketMaker` itself.
    """

    service_alias: LeftRightDot = "d1.isone.me.versant.keene"
    service_name: str = "marketmaker"  # XDG path segment for logs/state

    # The one market product the maker clears: real-time energy, 60-minute
    # slots, gate closing 5 minutes before the slot (gw.market.product.name).
    market_product: SpaceheatName = "rt60gate5"

    # ISO-NE web services (https://webservices.iso-ne.com), basic auth,
    # and the pricing node whose 5-minute LMP opens each slot.
    isone_user: str
    isone_api_pass: SecretStr
    isone_location_id: str = "43790"

    # How long before the slot opens the maker asks ISO-NE for the price,
    # so the publish itself is at the top of the hour.
    fetch_lead_s: int = 20

    # Control-plane participants required by GridworksActor. Placeholders
    # on a dev rung; in prod the supervisor and time coordinator aliases.
    my_super_alias: str = "d1.super"
    my_time_coordinator_alias: str = "d1.time"

    model_config = SettingsConfigDict(
        env_prefix="GWMM_",
        env_nested_delimiter="__",
        extra="ignore",
    )
