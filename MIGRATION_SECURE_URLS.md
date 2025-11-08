# Secure URL Migration (Phase 2 Completion)

## Scope
Converted priority resources (Bills, Payments, Issues, Notifications, Contracts, HouseRenter timeline) to hashid-based paths as canonical. Integer-ID routes for bills & payments deprecated and replaced by hashid aliases retaining legacy route names for reverse() compatibility.

## Changes
- Updated `sms/utils/hashid_converter.py` regex to respect `HASHIDS_MIN_LENGTH` (default 8) ensuring consistency.
- Deprecated integer bill/payment routes in `sms/urls.py` (commented for reference) and added hashid paths with both *secure* and *legacy* names.
- Added contract-related secure routes (`contract_detail`, `house_contracts`) with hashid IDs.
- Added corresponding views (`contract_detail`, `house_contracts`) and minimal templates.
- Added legacy name aliases for issue/notification secure routes allowing existing reverse calls to continue working.

## Backward Compatibility
Old route names (e.g., `bill_detail`, `update_bill`, `confirm_payment`) now point to hashid paths. Integer issue routes retained temporarily with `_int_deprecated` suffix to aid transition for any stored plain integer URLs. Plan to remove after logs show negligible usage.

## Next Steps
1. Instrument access logs (outside code) to detect any remaining integer URL hits.
2. Remove deprecated integer issue route patterns after confirmation.
3. Consider tightening converter regex further (e.g., require at least one letter) once all legacy integer-based hashes are phased out.
4. Update any external clients / API docs to reflect hashid usage.

## Testing Checklist
- Navigate bill detail/update/payment confirm/delete via secure URLs.
- Generate PDF still reachable at `/sms/bill/<hashid>/pdf/`.
- Notification read + issue modal uses hashid route.
- Contract listing and detail pages render correctly for authorized owner/staff; unauthorized users receive 403.

## Rollback Plan
Revert `sms/urls.py` to previous commit and remove new templates/views; restore integer routes if critical issue arises. No database schema changes were made.

---
Generated: Phase 2 – November 8, 2025
