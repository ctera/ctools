"""Unit tests for cache_report helpers (no live portal)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Project root contains ctools.py (entry script) which shadows the ctools package.
_root = Path(__file__).resolve().parents[1]
_src = str(_root / "src")
if _src not in sys.path:
    sys.path.insert(0, _src)
if str(_root) in sys.path:
    sys.path.remove(str(_root))

from ctools.tools.cache_report import (
    FIELDS,
    collect_cache,
    is_connected,
    read_targets,
    to_gib,
    CLOUD_EXTENDER,
    EVICTOR_PROC,
    EXECUTE_STORAGE_USED,
    STATUS_VOLUMES,
)


def test_to_gib():
    assert to_gib(1024 ** 3) == 1.0
    assert to_gib(None) == ""


def test_read_targets(tmp_path):
    path = tmp_path / "filers.csv"
    path.write_text("device_name,tenant\nvGateway-34f1,ZBportal\n", encoding="utf-8")
    assert read_targets(str(path)) == [("vGateway-34f1", "ZBportal")]


def test_is_connected_flag():
    status = MagicMock()
    status.connected = True
    device = MagicMock()
    device.deviceConnectionStatus = status
    assert is_connected(device) is True


def test_collect_cache_happy_path():
    remote = MagicMock()
    remote.cache.is_enabled.return_value = True
    extender = MagicMock()
    extender.operationMode = "CachingGateway"
    evictor = MagicMock()
    status_vol = MagicMock()
    status_vol.name = "vol1"
    status_vol.status = "ok"

    def get_by_path(path):
        return {
            CLOUD_EXTENDER: extender,
            EVICTOR_PROC: evictor,
            STATUS_VOLUMES: [status_vol],
        }[path]

    remote.api.get.side_effect = get_by_path
    remote.api.execute.side_effect = [5 * 1024 ** 3, 8 * 1024 ** 3]
    vol = MagicMock()
    vol.size = 1024 * 10
    vol.name = "vol1"
    remote.volumes.get.return_value = [vol]

    rows = collect_cache(remote, "ZBportal", "vGateway-34f1")
    assert len(rows) == 1
    assert set(rows[0]) == set(FIELDS)
    remote.api.execute.assert_any_call(CLOUD_EXTENDER, EXECUTE_STORAGE_USED)
