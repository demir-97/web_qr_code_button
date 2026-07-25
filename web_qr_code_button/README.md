# QR Code Button

**A "Show QR Code" action for any record, turned on from Settings.**

Settings > Technical > QR Code Button: pick a model, save. A "Show QR Code"
action now appears in the gear (Actions) menu of every record of that
model, opening a popup with a full-size QR code ready to print, save or
scan.

## What's encoded

- By default: a link back to the record — scan it and the record opens.
- Optionally, pick a Char/Text field on the model (serial number,
  reference, asset tag, ...) and the QR code encodes that value instead —
  handy for asset labels, product tags, warehouse bins.

## Technical

The QR code is rendered by Odoo's own barcode engine (the same one behind
invoices' payment QR codes) — no external service, no new dependency.
Turning a rule on creates a small `ir.actions.server` bound to the chosen
model (`binding_type='action'`), which is how it appears in the model's
Actions menu without touching any view. Turning it off unbinds the action
without deleting it.

---
Author: Meisanqo — meisanqo@outlook.com
