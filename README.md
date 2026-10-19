# DayZ World64 experimental workaround

A temporary, exact-build workaround for **`Out of static buffer memory` in the World script module** of the Windows x64 DayZ dedicated server. Related report: [DZG-837 — Static memory issues](https://report.bistudio.com/issues/DZG-837).

The patch increases the server's World script arena from **32 MiB to 64 MiB**. It changes one byte in a separately generated executable copy. It does not remove the allocator's bounds checks. This is an experimental community workaround, not an official Bohemia Interactive fix or a general solution for every out-of-memory error.

**No game executables, DLLs or PBOs are distributed here.** You supply your own original server executable. The patcher uses only the Python standard library and refuses every input other than the exact original hash below. There is no force option.

## Supported input

| Property | Required value |
| --- | --- |
| Platform | Windows x64 dedicated server |
| File | DayZServer_x64.exe |
| File version | 1.30.164.078 |
| Product version | 1.30.164078.38 |
| Size | 24,849,464 bytes |
| Original SHA-256 | `67dea3d44a5956cc4f57e9ecce91a64c9e7ee9cdfff0de52a65e4cae46f7ff20` |
| Patched SHA-256 | `e5575fdeeeb4649432841f768d47f637a2ad34286eed11482d42601a85273ab6` |

The hash, not the displayed version alone, determines compatibility. Linux, other builds, clients and the diagnostic executable are unsupported inputs.

## Create the patched copy

Install Python 3.10 or newer. Download this repository using **Code → Download ZIP**, extract it, and open PowerShell in the extracted directory. Use paths appropriate to your installation:

```powershell
py -3 .\patch_world64.py --source "C:\DayZServer\DayZServer_x64.exe" --output ".\DayZServer_x64.world64.exe"
Get-FileHash .\DayZServer_x64.world64.exe -Algorithm SHA256
```

The output directory must already exist. The original is never written. Existing output or manifest files are refused. Success creates the new executable and `DayZServer_x64.world64.manifest.json`, containing hashes and the change description without local paths. If an operation fails, do not install partial output; choose a fresh output name after resolving the failure.

## Installation and rollback

1. First test on a separate instance with your actual modpack. Back up the original executable and your mission persistence, profiles and mod-owned storage before any deployment.
2. Stop the selected instance and disable its automatic relaunch temporarily in your manager. Confirm that its process has exited. Do not replace a running executable.
3. Verify the generated copy against the patched SHA-256 above. Keep the original backup outside any automatic update/replacement location.
4. Replace only the selected instance's `DayZServer_x64.exe` with the generated copy, using the original filename. Preserve the installation's ownership and access permissions; check them after copying. No launch parameter or client download is added by this workaround.
5. Start the instance normally with its existing security configuration. Check compilation, connections, gameplay, saves and a subsequent restart. Do not disable BattlEye or signature checks to make a production deployment work.
6. To roll back, stop the instance again and restore the original executable. Restoring the executable does not undo gameplay or persistence changes made while it ran; restore data backups separately only when necessary.

Game updates or Steam file verification can replace the executable. Never apply the byte offset to a different build, modify the accepted hash to bypass verification, or pin an outdated build solely to keep this workaround. An unsupported hash requires new analysis and testing.

## What we changed and why

Offline PE inspection and x64 disassembly traced the module capacity argument from module initialization into the script allocator. On this exact server build the observed capacities were GameLib 2 MiB, Game 32 MiB, World 32 MiB and Mission 32 MiB. These are separate arenas, not a single shared pool. Free machine RAM cannot automatically expand them.

At file offset `0xA4E72D`, the World initializer contains:

```text
Original: C7 44 24 20 00 00 00 02   mov dword ptr [rsp+0x20], 0x02000000
Patched:  C7 44 24 20 00 00 00 04   mov dword ptr [rsp+0x20], 0x04000000
```

Only file byte `0xA4E734` changes: `02` → `04`. This doubles the World capacity argument. GameLib, Game and Mission remain unchanged. The allocator still allocates and clears the requested region and maintains its capacity/end pointers and bounds checks. See [technical analysis](docs/TECHNICAL.md) for the trace and its limits.

The log prints capacity divided by 1,000: `33554 kB` corresponds to 32 MiB and `67108 kB` to 64 MiB. This is **script static arena usage**, not total process RAM. Expect an additional 32 MiB allocation for this arena; this is not a CPU, multicore or FPS optimization.

## Validation and limitations

A controlled native A/B test used the same synthetic PBO, parameters and supporting inputs with 140,000 generated methods. The original executable failed during World compilation with `Out of static buffer memory`. The patched copy reported **World 42318/67108 kB**, exceeded the old capacity, and successfully checked all 140,000 methods.

The test ran during early World initialization and deliberately exited before a full mission. It did not validate full gameplay, persistence, multiplayer or BattlEye. The test used `-noBE`; this is a test limitation, not an installation instruction. The original process was terminated after a timeout following the compilation error. The candidate completed without timeout or forced termination; its native exit code was -1, also seen in successful controls. Success was determined by explicit verification markers and absence of script errors/dumps, not exit code alone.

Separately, the operator reported successful server startup and a connection using an unmodified client after deploying the same patched executable. This is an operator report, not a recorded long-duration or multi-client stability test. See [sanitized validation record](docs/VALIDATION.json).

**The main unresolved risk is engine behavior on untested paths or under sustained load.** A crash may interrupt saves or lose progress. No exhaustive audit of all VM offset encodings, engine limits or persistence behavior has been completed. The modified executable no longer matches its original publisher's Authenticode signature. No guarantee of anti-cheat acceptance, hosting-provider acceptance, or production stability is made.

## Frequently asked questions

**Do players need a client patch or Workshop mod?** This workaround only modifies the dedicated server. It does not change the network protocol. One normal client connection was reported, but universal compatibility has not been established. Each client retains its own static arena limits; a client that reaches its own limit is not fixed by this server change.

**Why can the client start when the server fails?** Compiled content can differ because of server-only mods and preprocessing such as `SERVER`. An ordinary runtime `IsServer()` condition does not itself remove compiled code. Compare actual module logs and loaded inputs rather than assuming identical usage.

**Can a PBO alone do this?** This change targets a native executable capacity argument. It is not a script-only PBO fix and should not be advertised as one.

**Does this fix Game or Mission errors?** No. Only World changes. The mod named at the error location may simply be the point at which the arena becomes full, rather than the sole cause.

**Can I raise it further?** This project deliberately supports only the tested 64 MiB candidate. Larger values and changes to other modules require separate investigation.

## Testing the patcher

```powershell
py -3 -m unittest discover -s tests -v
```

These tests exercise refusal and file-preservation behavior without distributing the proprietary input. Generating a copy from the supported original and checking the expected output hash is a separate integration check. Unit tests do not establish game stability.

## Support this work

If this investigation and temporary workaround help your server, optional donations are welcome through **PayPal: gabrielrszj@icloud.com**. Donations support the time spent investigating, testing and documenting the work. The source remains freely available; donations do not buy a safety guarantee, priority support or an official fix.

## License and attribution

Original scripts and documentation in this repository are provided under the [MIT License](LICENSE). That license does not grant rights to DayZ or any third-party binary or asset. DayZ belongs to its respective rights holders. This project is independent and is not endorsed by Bohemia Interactive. Analysis used PE inspection and bounded disassembly, not recovered original source code.
