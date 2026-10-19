# Beginner guide — Windows server

This experimental workaround addresses **Out of static buffer memory in World** on one exact Windows x64 DayZ dedicated-server build. It is not a general crash fix, a client update or an official Bohemia patch.

You will **download our tool → select your original executable → generate a copy → stop your server → install the copy → check the logs**. The wizard only creates a copy; it does not install, start or stop anything on your host.

## 1. Download and extract

**[Download the ZIP](https://github.com/jovemgeek/dayz-world64-workaround/archive/refs/heads/main.zip)**. Right-click it and choose **Extract All**. Open the extracted folder. Do not run from inside the ZIP or download only the BAT: it needs the Python files beside it.

## 2. Install Python once

Install a stable Python 3.10 or newer from the [official Windows download page](https://www.python.org/downloads/windows/), including the **py launcher** and **Tcl/Tk**. Skip this step if you already have these. No extra Python packages or changes to Windows security settings are needed.

## 3. Generate your copy

1. Double-click **START-HERE.bat** in the extracted folder. Windows may display it as **START-HERE** if extensions are hidden.
2. Read the introduction and click **OK**.
3. Select your **original DayZServer_x64.exe**. Do not select the client executable or an already patched file.
4. Choose an output location, such as Downloads. A new **World64-...** folder will be created there.
5. Wait for **COPY CREATED AND VERIFIED**. The message gives the full output path.

The new folder contains `DayZServer_x64.exe` (your patched copy) and `DayZServer_x64.manifest.json` (the verification record). Your original stays unchanged. Both hashes are checked automatically. Never install output from a failed attempt.

For a remote host, download the original executable from the exact server instance, generate the copy on your PC, and upload the result. Do not mix builds from your PC and host.

## 4. Back up and stop

Keep a separate original executable backup, for example `DayZServer_x64.original.exe`. Back up **profiles**, **mpmissions** and additional mod-owned storage. Stop the correct instance normally through your manager so it can save player/world state. Prevent automatic relaunch during replacement and wait for its process to exit.

## 5. Install

Replace only **DayZServer_x64.exe** in that stopped instance's main directory with the generated file from **World64-...**. Keep the installed filename exactly **DayZServer_x64.exe** and preserve access permissions.

Do not put it in `addons` or the client game directory. Do not add anything to `-mod` or `-serverMod`: this is not a Workshop PBO. Keep your current mod lists and server dependencies. If your provider does not permit executable replacement, ask its support; this guide does not bypass that restriction.

## 6. Start and verify

Start normally through your manager with the existing security settings. In the new logs, usually under `profiles` or the panel's log area, look for:

```text
Module: World; ... used XXXXX/67108 kB ... of static memory
```

**/67108 kB** is the new capacity; **/33554 kB** is the old capacity. The used amount varies. Some logging modes do not print this line: check the installed executable hash or ask an administrator instead. A missing line alone does not prove failure.

Check World and Mission compilation, online status, a player connection, gameplay and persistence after a normal stop/restart. An open server window alone does not prove these checks. Observe the first operating cycles; long-term stability is not guaranteed.

For `Unknown type`, `Can't find variable` or missing-dependency messages, inspect the first error and loaded mod list. Extra memory does not install a missing mod or fix its code.

## Undo the change

Stop the instance and automatic relaunch. Restore the original backup as **DayZServer_x64.exe**, then start normally. Restoring the executable does not undo player/world changes. Restore data backups separately only if necessary.

## Troubleshooting

| Message or symptom | Next step |
| --- | --- |
| Python prompt | Install Python 3.10+ with py launcher and Tcl/Tk, then reopen the BAT. |
| Unsupported executable | Wrong build, client or modified file. Use the supported original; never change hashes to force it. |
| Output/manifest already exists | For command-line mode, choose a new output name. The wizard creates a fresh folder automatically. |
| Access denied | Generate in a writable folder; use authorized host access or provider support for installation. |
| Still /33554 kB | Check the instance path and whether an automatic update restored the original EXE. |
| Another module is out of memory | Only World changes. |
| A new update is unsupported | Another build requires fresh analysis. Never reuse the offset blindly. |

## Supported file and download policy

Input: Windows x64 dedicated server, product version **1.30.164078.38**, **24,849,464 bytes**, with the exact [hashes in the README](../README.md#supported-input). The tool verifies these automatically.

A ready-patched game download would be convenient, but the [DayZ Server EULA](https://store.steampowered.com/eula/223350_eula_0) restricts redistribution and modification/reverse engineering. We have not obtained Bohemia's authorization. Shipping only our patcher does not establish authorization under that license. No game executable is distributed here.

The modified file no longer matches its publisher signature. Anti-cheat/provider acceptance and sustained stability are not guaranteed. Read the [technical findings and validation limits](../README.md#validation-and-limitations).

If this work helps, optional donations are welcome through **PayPal: gabrielrszj@icloud.com**. The tools remain free; donations do not purchase a stability guarantee.
