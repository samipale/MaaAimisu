# Third-Party Notices

This project incorporates or depends on the following third-party
components. The `LICENSE` file in this repository (PolyForm Noncommercial
1.0.0) applies **only** to the original code authored by samipale and does
**not** override, restrict, or modify the license terms of the components
listed below.

---

## 1. MaaPracticeBoilerplate — MIT License

Portions of this project are derived from [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate) licensed under the
MIT License.

```
MIT License

Copyright (c) 2024 MaaXYZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Framework Dependency — MaaFramework (LGPL-3.0)

This project uses [MaaFramework](https://github.com/MaaXYZ/MaaFramework),
which is licensed under the **GNU Lesser General Public License v3.0
(LGPL-3.0)**.

- Full license text: <https://www.gnu.org/licenses/lgpl-3.0.html>
- Source repository: <https://github.com/MaaXYZ/MaaFramework>

**Important:** The GNU Lesser General Public License, like the GPL, must be
reproduced in its entirety when included in a project — partial copies or
excerpts are not permitted by the Free Software Foundation. Rather than
reproducing a possibly-outdated or incomplete copy here, please:

1. Download the current official plain-text version directly from
   <https://www.gnu.org/licenses/lgpl-3.0.txt>, and
2. Save it in this repository as `COPYING.LESSER` (the conventional
   filename the FSF recommends), alongside the GPLv3 text it incorporates
   from <https://www.gnu.org/licenses/gpl-3.0.txt> (save as `COPYING`).

### Summary of your obligations under LGPL-3.0 (informational only — refer to the full license text for binding terms)

- You must retain LGPL-3.0's copyright and license notices for MaaFramework.
- If you modify MaaFramework itself, those modifications must also be
  released under LGPL-3.0.
- If you statically link MaaFramework into your own application, you must
  provide a way for users to relink your application against a modified
  version of MaaFramework (e.g., by providing object files, or by using
  dynamic linking instead).
- You may **not** impose additional restrictions (such as a
  "noncommercial-only" condition) on MaaFramework itself or on anyone's
  ability to use, modify, or redistribute it under LGPL-3.0. The
  NonCommercial term in this project's `LICENSE` file applies solely to
  samipale's own original code, and explicitly does not extend to
  MaaFramework.

---

## 3. GUI Shell — MFAAvalonia (GPL-3.0)

This project uses [MFAAvalonia](https://github.com/SweetSmellFox/MFAAvalonia)
as an unmodified, standalone GUI shell, licensed under the **GNU General
Public License v3.0 (GPL-3.0)**.

- Full license text: <https://www.gnu.org/licenses/gpl-3.0.html>
- Source repository: <https://github.com/SweetSmellFox/MFAAvalonia>

**Integration model:** MFAAvalonia's source code has not been modified.
It is used as a separate, independently-running shell program that loads
this project's task definitions, configuration files, and resource assets
(e.g., JSON pipeline files, images) at runtime through its documented
resource/plugin interface — it is not compiled together with, and does not
share internal data structures or private APIs with, this project's own
original code.

> ⚠️ **Legal note:** GPL-3.0 is a *strong* copyleft license — stronger than
> the LGPL-3.0 terms covering MaaFramework above. Whether a "plugin" or
> "resource pack" loaded by a GPL program counts as a separate work (safe)
> or a derivative work (which would require the loaded content itself to
> be GPL-3.0) is not always a bright-line legal question; it depends on how
> generic/documented the interface is versus how deeply it's coupled to
> the GPL program's internals. Treating configuration/data files (JSON
> task flows, images, resource packs) through a documented interface as
> described above is the commonly accepted "safe" pattern. If custom
> executable code is later written specifically against MFAAvalonia's
> internal plugin APIs (rather than just data/config), that determination
> should be revisited.

### Obligations when distributing MFAAvalonia (even unmodified)

- Include the full GPL-3.0 license text (see `COPYING` above — GPL-3.0 and
  LGPL-3.0 share the same underlying GPLv3 text).
- Preserve MFAAvalonia's original copyright notices.
- Provide a way for recipients to obtain MFAAvalonia's corresponding source
  code (a link to its public GitHub repository satisfies this).
- Do not represent MFAAvalonia itself as being under this project's
  PolyForm Noncommercial `LICENSE` — it remains GPL-3.0 and retains all
  freedoms (including commercial use) that GPL-3.0 grants for the
  MFAAvalonia component itself.

---

## Scope Reminder

| Component                 | License | Covered by this repo's `LICENSE` file? |
|---------------------------|---|---|
| Original code by samipale | PolyForm Noncommercial 1.0.0 | Yes |
| Code from MaaPracticeBoilerplate    | MIT License | No — governed by MIT above |
| MaaFramework              | LGPL-3.0 | No — governed by LGPL-3.0 above |
| MFAAvalonia               | GPL-3.0 | No — governed by GPL-3.0 above |
