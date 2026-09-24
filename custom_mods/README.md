# Custom mods

Mods I run on top of G.A.M.M.A. that are **not** part of the modpack itself (they are not in `G.A.M.M.A/modpack_data/modlist.txt` or `modpack_maker_list.txt`). They're kept here so they can be looked up, edited and updated later.

## Layout

One folder per mod, laid out exactly as it's installed in Mod Organizer 2:

```
custom_mods/
  <Mod Name> - <Author>/
    gamedata/
      scripts/...
      configs/...
      textures/...
    NOTES.md        (optional)
```

`NOTES.md` (optional) holds: where the mod came from (link and version), what it does, where it sits in MO2 load order (e.g. "just below G.A.M.M.A. End of List"), and any changes I've made to it.

There's no size limit; upload the whole mod. Big binary files (`.dds`, `.ogg`, `.wav`, `.ogf`, `.omf`, `.db*`, `.xdb*`, `.7z`, `.zip`, `.rar`) are stored with Git LFS automatically (see `.gitattributes` in the repo root). Scripts and configs stay as normal text.

## How to upload

**GitHub Desktop or git (recommended, handles any size):**
1. Clone this repo (GitHub Desktop: *File → Clone repository*).
2. Copy the mod folder into `custom_mods/`.
3. Commit and push. Big files go through LFS on their own; GitHub Desktop includes LFS. With command-line git, run `git lfs install` once first.

**GitHub website (quick, for small mods):**
1. Open `custom_mods/` on GitHub → **Add file → Upload files**.
2. Drag the mod folder in → **Commit changes**.
3. The website refuses files over 25 MB. Use GitHub Desktop for those.

## Index

| Mod | Source | Version | Enabled | Notes |
|---|---|---|---|---|
| _(none yet)_ | | | | |
