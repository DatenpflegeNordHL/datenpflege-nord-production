# Contact backend production inventory

The versioned `contact_api.py` is byte-for-byte identical to the production file at `/opt/dpn-contact/contact_api.py` as audited on 2026-08-25 (SHA-256 `4f969d53d0295c554bf51cc3e67606813b243aa0ade792d37d08b62304cc6c4f`).

Production topology:

- systemd unit: `dpn-contact.service`
- runtime user/group: `www-data:www-data`
- listen address: `127.0.0.1:8091`
- nginx route: exact `/api/contact` proxy to the loopback listener
- delivery provider: DeoMail HTTPS API
- secret source: root-owned `/etc/datenpflege-nord-contact.env`, mode `0600`
- rate limit: five accepted attempts per source IP per 600-second in-memory window
- request limits: nginx 64 KiB and application `Content-Length` maximum 65,536 bytes

## Safe migration/deployment procedure

This repository addition does not replace or restart the production service. For a future deployment:

1. Back up `/opt/dpn-contact/contact_api.py` and `/etc/systemd/system/dpn-contact.service`.
2. Run `python3 -m py_compile backend/contact_api.py` and the repository tests.
3. Install to a versioned release path, preserving `www-data` read access; never copy the environment file into the repository or release.
4. Update the systemd `ExecStart` path only after `systemd-analyze verify` succeeds.
5. Restart `dpn-contact.service`, then verify `/health` directly and a non-mailing public `GET /api/contact` response.
6. Retain the previous release path for immediate rollback. A real form submission must be a separately approved mail-delivery test.

The current in-memory limiter resets on service restart and does not coordinate across multiple processes. That is acceptable for the present single-process loopback deployment; a multi-process migration must move rate-limit state to a shared store or enforce it at the edge.
