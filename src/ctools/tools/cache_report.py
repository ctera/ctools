"""Edge Filer cache utilization report (read-only, Portal + remote access)."""

from __future__ import annotations

import csv
import logging
import time
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

from cterasdk.common import parse_base_object_ref
from cterasdk.exceptions import CTERAException, ObjectNotFoundException

from ..core.filer import get_filers, get_portal_name

logger = logging.getLogger(__name__)

DEVICE_INCLUDE = [
    "name",
    "portal",
    "deviceType",
    "version",
    "remoteAccessUrl",
    "deviceConnectionStatus",
    "deviceConnectionStatus.connected",
    "deviceReportedStatus.config.hostname",
]

CLOUD_EXTENDER = "/config/cloudsync/cloudExtender"
STATUS_VOLUMES = "/status/storage/volumes"
EVICTOR_PROC = "/proc/cloudsync/evictor"
EXECUTE_STORAGE_USED = "storageUsedBytes"
EXECUTE_LOGICAL_USED = "allFilesTotalUsedBytes"

FIELDS = [
    "tenant",
    "device_name",
    "volume_name",
    "volume_status",
    "total_gib",
    "used_gib",
    "free_gib",
    "usage_percent",
    "check_output",
]


def _as_float(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _fmt_num(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def format_check_output(
    row: dict,
    usage_warn_pct: float = 70.0,
    usage_crit_pct: float = 90.0,
    used_warn_pct: float = 80.0,
    used_crit_pct: float = 90.0,
) -> str:
    device = row.get("device_name") or "unknown"
    volume = row.get("volume_name") or "vol1"
    used = _as_float(row.get("used_gib"))
    free = _as_float(row.get("free_gib"))
    total = _as_float(row.get("total_gib"))
    usage_pct = _as_float(row.get("usage_percent"))

    if used is None or total is None or total <= 0:
        return ""

    if free is None:
        free = round(total - used, 2)
    if usage_pct is None:
        usage_pct = round(used / total * 100, 2)

    used_warn = round(total * used_warn_pct / 100, 2)
    used_crit = round(total * used_crit_pct / 100, 2)

    if usage_pct >= usage_crit_pct:
        exit_code = 2
        status_word = "critical"
    elif usage_pct >= usage_warn_pct:
        exit_code = 1
        status_word = "warning"
    else:
        exit_code = 0
        status_word = "ok"

    perf = (
        f"used_gib={_fmt_num(used)};{_fmt_num(used_warn)};{_fmt_num(used_crit)};0;{_fmt_num(total)}|"
        f"free_gib={_fmt_num(free)};;;0;{_fmt_num(total)}|"
        f"usage_pct={_fmt_num(usage_pct)};{_fmt_num(usage_warn_pct)};{_fmt_num(usage_crit_pct)}"
    )
    summary = (
        f"Volume status: {status_word}, "
        f"Used: {_fmt_num(used)} GiB / {_fmt_num(total)} GiB ({_fmt_num(usage_pct)}%)"
    )
    return f'{exit_code} "Volume {volume} on {device}" {perf} {summary}'


def enrich_rows_with_check_output(
    rows: list[dict],
    usage_warn_pct: float,
    usage_crit_pct: float,
    used_warn_pct: float,
    used_crit_pct: float,
) -> None:
    for row in rows:
        row["check_output"] = format_check_output(
            row,
            usage_warn_pct=usage_warn_pct,
            usage_crit_pct=usage_crit_pct,
            used_warn_pct=used_warn_pct,
            used_crit_pct=used_crit_pct,
        )


def retry_on_transient(func, retries: int = 3, delay: float = 2.0):
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return func()
        except (CTERAException, TimeoutError, ConnectionError, OSError) as exc:
            last_exc = exc
            logger.warning("Attempt %d/%d failed: %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(delay * attempt)
    raise last_exc


def empty_row(**overrides) -> dict:
    row = {key: "" for key in FIELDS}
    row.update(overrides)
    return row


def tenant_of(device) -> str:
    ref = getattr(device, "portal", None)
    if not ref:
        return ""
    try:
        return parse_base_object_ref(ref).name or ""
    except Exception as exc:  # noqa: BLE001
        logger.debug("Could not parse portal ref %r: %s", ref, exc)
        return str(ref)


def is_connected(device) -> bool:
    status = getattr(device, "deviceConnectionStatus", None)
    if status is None:
        return bool(getattr(device, "connected", False))
    connected = getattr(status, "connected", None)
    if connected is not None:
        return bool(connected)
    return str(status).lower() == "connected"


def to_gib(value):
    if value in (None, ""):
        return ""
    try:
        return round(float(value) / 1024 ** 3, 2)
    except (TypeError, ValueError):
        return ""


def volume_size_bytes(size_mb):
    if size_mb in (None, ""):
        return None
    try:
        return int(float(size_mb)) * 1024 * 1024
    except (TypeError, ValueError):
        return None


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def by_name(items):
    return {item.name: item for item in as_list(items) if getattr(item, "name", None)}


def read_targets(path: str) -> list[tuple[str, str | None]]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = {x.strip().lower().replace(" ", "_"): x for x in (reader.fieldnames or [])}
        device_col = next((headers[k] for k in ("device_name", "name", "filer", "device") if k in headers), None)
        tenant_col = next((headers[k] for k in ("tenant", "tenant_name", "portal") if k in headers), None)
        if not device_col:
            raise ValueError(f"{path} needs a device_name column")
        out = []
        for rec in reader:
            name = (rec.get(device_col) or "").strip()
            if not name:
                continue
            tenant = ((rec.get(tenant_col) or "").strip() or None) if tenant_col else None
            out.append((name, tenant))
        if not out:
            raise ValueError(f"No filers in {path}")
        return out


def resolve_output_path(path: str) -> str:
    """Use a writable path; bare filenames go under ~/Documents/CTools-reports."""
    raw = (path or "cache_report.csv").strip()
    target = Path(raw)
    if not target.is_absolute():
        target = Path.home() / "Documents" / "CTools-reports" / target.name
    target.parent.mkdir(parents=True, exist_ok=True)
    return str(target)


def close_remote(remote) -> None:
    if not remote:
        return
    for method_name in ("close", "logout"):
        method = getattr(remote, method_name, None)
        if not callable(method):
            continue
        try:
            method()
            return
        except Exception as exc:  # noqa: BLE001
            logger.debug("remote %s failed: %s", method_name, exc)


def collect_cache(remote, tenant: str, name: str) -> list[dict]:
    row = empty_row(tenant=tenant, device_name=name)
    try:
        enabled = remote.cache.is_enabled()
        logger.info("[SDK OK] cache.is_enabled device=%s enabled=%s", name, enabled)
    except Exception as exc:  # noqa: BLE001
        logger.warning("[SDK FAIL] cache.is_enabled device=%s: %s", name, exc)

    try:
        extender = remote.api.get(CLOUD_EXTENDER)
        logger.info(
            "[API OK] cloudExtender device=%s mode=%s",
            name,
            getattr(extender, "operationMode", ""),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("[API FAIL] cloudExtender device=%s: %s", name, exc)

    cache_used = None
    try:
        cache_used = remote.api.execute(CLOUD_EXTENDER, EXECUTE_STORAGE_USED)
        logger.info("[API OK] storageUsedBytes device=%s used=%s", name, cache_used)
    except Exception as exc:  # noqa: BLE001
        logger.warning("[API FAIL] storageUsedBytes device=%s: %s", name, exc)

    try:
        logical = remote.api.execute(CLOUD_EXTENDER, EXECUTE_LOGICAL_USED)
        logger.info("[API OK] allFilesTotalUsedBytes device=%s logical=%s", name, logical)
    except Exception as exc:  # noqa: BLE001
        logger.warning("[API FAIL] allFilesTotalUsedBytes device=%s: %s", name, logical)

    try:
        remote.api.get(EVICTOR_PROC)
        logger.info("[API OK] %s device=%s", EVICTOR_PROC, name)
    except Exception as exc:  # noqa: BLE001
        logger.warning("[API FAIL] evictor device=%s: %s", name, exc)

    configs = {}
    try:
        configs = by_name(remote.volumes.get())
        logger.info("[SDK OK] volumes.get device=%s count=%d", name, len(configs))
    except Exception as exc:  # noqa: BLE001
        logger.warning("[SDK FAIL] volumes.get device=%s: %s", name, exc)

    statuses = {}
    try:
        statuses = by_name(remote.api.get(STATUS_VOLUMES))
        logger.info("[API OK] %s device=%s count=%d", STATUS_VOLUMES, name, len(statuses))
    except Exception as exc:  # noqa: BLE001
        logger.warning("[API FAIL] %s device=%s: %s", STATUS_VOLUMES, name, exc)

    names = list(dict.fromkeys([*statuses, *configs]))
    if not names:
        return [row]

    rows = []
    for index, vol_name in enumerate(names):
        item = dict(row)
        cfg = configs.get(vol_name)
        st = statuses.get(vol_name)
        item["volume_name"] = vol_name
        item["volume_status"] = getattr(st, "status", "") or ""
        total_bytes = volume_size_bytes(getattr(cfg, "size", None) if cfg is not None else None)
        item["total_gib"] = to_gib(total_bytes)
        used_for_row = cache_used if index == 0 else None
        item["used_gib"] = to_gib(used_for_row) if index == 0 else ""
        if total_bytes is not None and used_for_row is not None:
            free = total_bytes - int(used_for_row)
            item["free_gib"] = to_gib(free)
            if total_bytes:
                item["usage_percent"] = round(int(used_for_row) / total_bytes * 100, 2)
        rows.append(item)
    return rows


def query_device(admin, tenant: str, filer) -> list[dict]:
    """Collect cache via portal devicecmdnew proxy — same device access as Status report."""
    name = getattr(filer, "name", None) or "<unknown>"
    if not tenant:
        logger.error("Missing tenant for device=%s", name)
        return [empty_row(tenant="", device_name=name)]
    try:
        admin.portals.browse(tenant)
        return retry_on_transient(lambda: collect_cache(filer, tenant, name))
    except Exception as exc:  # noqa: BLE001
        logger.error("Cache collect failed device=%s tenant=%s: %s", name, tenant, exc)
        return [empty_row(tenant=tenant, device_name=name)]


def all_filers(admin):
    return [(tenant_of(edge) or "", edge) for edge in admin.devices.filers(include=DEVICE_INCLUDE, allPortals=True)]


def filer_index(admin):
    index = {}
    for found_tenant, edge in all_filers(admin):
        key = (getattr(edge, "name", "") or "").lower()
        index.setdefault(key, []).append((found_tenant, edge))
    return index


def find_filer(admin, device_name: str, tenant: str | None, index=None):
    if tenant:
        try:
            return tenant, admin.devices.device(device_name, tenant=tenant, include=DEVICE_INCLUDE), ""
        except ObjectNotFoundException:
            return tenant, None, "not found"
        except CTERAException as exc:
            logger.warning("devices.device failed name=%s tenant=%s: %s", device_name, tenant, exc)
            return tenant, None, str(exc)
    catalog = index if index is not None else filer_index(admin)
    hits = catalog.get(device_name.lower(), [])
    if len(hits) == 1:
        found_tenant, edge = hits[0]
        return found_tenant, edge, ""
    if len(hits) > 1:
        logger.error("Ambiguous device name %s — supply tenant", device_name)
        return None, None, "ambiguous name — supply tenant"
    return None, None, "not found"


def collect_rows(
    admin,
    *,
    targets: Sequence[tuple[str, str | None]] | None,
    scan_all: bool,
    default_tenant: str | None,
) -> list[dict]:
    """Collect cache rows using an authenticated GlobalAdmin session (SSO already enabled)."""
    rows: list[dict] = []
    if targets is None:
        logger.info("Enumerating connected filers (get_filers — same as Status report)")
        filers = get_filers(admin, all_tenants=True)
        if not filers:
            logger.warning("No connected filers found")
            return rows
        for filer in filers:
            tenant_name = get_portal_name(filer)
            logger.info("Filer %s tenant=%s", filer.name, tenant_name)
            rows.extend(query_device(admin, tenant_name, filer))
        return rows

    needs_index = any(not (csv_tenant or default_tenant) for _, csv_tenant in targets)
    catalog = filer_index(admin) if needs_index else None
    for device_name, csv_tenant in targets:
        resolved_tenant = csv_tenant or default_tenant
        found_tenant, edge, lookup_error = find_filer(admin, device_name, resolved_tenant, index=catalog)
        if edge is None:
            logger.error(
                "Lookup failed device=%s tenant=%s: %s",
                device_name,
                resolved_tenant or "",
                lookup_error or "not found",
            )
            rows.append(
                empty_row(
                    tenant=resolved_tenant or found_tenant or "",
                    device_name=device_name,
                )
            )
            continue
        logger.info("Filer %s tenant=%s", device_name, found_tenant)
        rows.extend(query_device(admin, found_tenant or "", edge))
    return rows


def collect_rows_for_tenant(admin, tenant: str) -> list[dict]:
    rows: list[dict] = []
    logger.info("Enumerating connected filers for tenant %s", tenant)
    filers = get_filers(admin, all_tenants=False, tenant=tenant)
    if not filers:
        logger.warning("No connected filers found for tenant %s", tenant)
        return rows
    for filer in filers:
        rows.extend(query_device(admin, tenant, filer))
    return rows


def write_csv(rows: Iterable[dict], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def run_cache_report(
    session: Any,
    filename: str,
    tenant: Optional[str] = None,
    all_tenants: bool = True,
    input_csv: Optional[str] = None,
    usage_warn_pct: float = 70.0,
    usage_crit_pct: float = 90.0,
    used_warn_pct: float = 80.0,
    used_crit_pct: float = 90.0,
) -> None:
    """
    Generate edge filer cache utilization CSV.

    Args:
        session: Authenticated GlobalAdmin session (device SSO enabled)
        filename: Output CSV path
        tenant: Limit to one portal tenant when all_tenants is False
        all_tenants: When True and no input_csv, scan all portals
        input_csv: Optional CSV of device_name[,tenant] rows
    """
    logging.info("Starting cache report task.")
    filename = resolve_output_path(filename)

    if input_csv:
        targets = read_targets(input_csv)
        rows = collect_rows(
            session,
            targets=targets,
            scan_all=False,
            default_tenant=tenant,
        )
    elif tenant and not all_tenants:
        rows = collect_rows_for_tenant(session, tenant)
    else:
        rows = collect_rows(
            session,
            targets=None,
            scan_all=True,
            default_tenant=None,
        )

    enrich_rows_with_check_output(
        rows,
        usage_warn_pct=usage_warn_pct,
        usage_crit_pct=usage_crit_pct,
        used_warn_pct=used_warn_pct,
        used_crit_pct=used_crit_pct,
    )
    write_csv(rows, filename)
    with_metrics = sum(1 for row in rows if row.get("total_gib"))
    logging.info("Cache report saved to %s (%d rows, %d with volume data)", filename, len(rows), with_metrics)
    if not with_metrics:
        logging.warning(
            "No cache volume metrics were collected. If Status Report works for a filer but "
            "this report does not, check debug log for [API FAIL] lines for that device."
        )
    logging.info("Finished cache report task.")
